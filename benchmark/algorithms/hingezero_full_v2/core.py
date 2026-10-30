import numpy as np
AUTHOR = 'David Duffy'
HZ_ALPHA = 4.5
HZ_EPS = 0.1
HZ_LAMBDA = 0.02
HZ_STEPS = 8
HZ_TOP = 256

def _unit(x):
    x = np.asarray(x, np.float32)
    x = np.nan_to_num(x, nan=0.0, posinf=0.0, neginf=0.0)
    if x.ndim == 1:
        norm = float(np.linalg.norm(x))
        return x / norm if norm > 1e-12 else np.zeros_like(x)
    norm = np.linalg.norm(x, axis=1, keepdims=True)
    return np.divide(x, norm, out=np.zeros_like(x), where=norm > 1e-12)

def _cos_rows(A, q):
    return _unit(A) @ _unit(q)

def hinge_phi(h, alpha=HZ_ALPHA):
    return np.tanh(h) + alpha * np.tanh(2.0 * h)

class HingeZeroState:

    def __init__(self, candidate_index, state):
        self.candidate_index = int(candidate_index)
        self.state = np.asarray(state, np.float32).copy()

class HingeZeroWitness:

    def __init__(self, memories, evidence):
        self._raw_memories = np.asarray(memories, np.float32).copy()
        self.memories = _unit(memories)
        if self.memories.ndim != 2 or len(self.memories) == 0:
            raise ValueError('HingeZero requires a nonempty candidate memory bank')
        self.evidence = np.nan_to_num(np.asarray(evidence, np.float32), nan=0.0, posinf=0.0, neginf=0.0)
        if self.evidence.shape != (len(self.memories),):
            raise ValueError('Candidate memory and evidence counts differ')
        self.field_ids = np.argsort(-self.evidence, kind='stable')[:min(HZ_TOP, len(self.memories))]
        self.field_memories = self.memories[self.field_ids]

    def _stored_index(self, state):
        if isinstance(state, HingeZeroState):
            i = state.candidate_index
            if 0 <= i < len(self.memories) and np.array_equal(state.state, self.memories[i]):
                return i
            return None
        x = np.asarray(state, np.float32)
        if x.shape != (self.memories.shape[1],):
            raise ValueError('HingeZero query dimension differs from candidate memories')
        exact = np.flatnonzero(np.all(self.memories == x, axis=1))
        if len(exact):
            return int(exact[np.argmax(self.evidence[exact])])
        return None

    def query_from_evidence(self):
        weights = np.maximum(self.evidence[self.field_ids].astype(np.float64), 0.0)
        total = float(weights.sum())
        if total <= 1e-12:
            weights = np.full(len(self.field_ids), 1.0 / len(self.field_ids), np.float64)
        else:
            weights /= total
        return _unit(weights.astype(np.float32) @ self.field_memories)

    def refine(self, state):
        stored = self._stored_index(state)
        if stored is not None:
            return self.memories[stored].copy()
        x = state.state if isinstance(state, HingeZeroState) else state
        x = _unit(np.asarray(x, np.float32))
        if np.linalg.norm(x) <= 1e-12:
            x = self.query_from_evidence()
        for _ in range(HZ_STEPS):
            h = self.field_memories @ x
            response = hinge_phi(h)
            field = self.field_memories.T @ response
            field /= float(np.sum(np.abs(response))) + 1e-12
            x = _unit((1.0 - HZ_LAMBDA) * x + HZ_EPS * field)
        return x

    def observe(self, state, scores=None):
        stored = self._stored_index(state)
        if stored is not None:
            return HingeZeroState(stored, self.memories[stored])
        if scores is None:
            scores = _cos_rows(self.memories, self.refine(state))
        scores = np.asarray(scores, np.float64)
        if scores.shape != (len(self.memories),):
            raise ValueError('Watcher scores differ from candidate memory count')
        scores = np.nan_to_num(scores, nan=-1e+30, posinf=1e+30, neginf=-1e+30)
        i = int(np.argmax(scores))
        return HingeZeroState(i, self.memories[i])

    def hypotheses(self, state, scores):
        locked = self.observe(state, scores)
        order = np.argsort(-np.asarray(scores), kind='stable')
        order = np.r_[locked.candidate_index, order[order != locked.candidate_index]]
        return (order, locked)

    def accepts(self, state):
        return isinstance(state, HingeZeroState) and self._stored_index(state) is not None

    def verify(self, locked):
        if not self.accepts(locked):
            return False
        again = self.observe(locked)
        return self.accepts(again) and again.candidate_index == locked.candidate_index and np.array_equal(again.state, locked.state)

    def append_memories(self, memories, evidence=None):
        new = np.asarray(memories, np.float32)
        if new.ndim == 1:
            new = new[None, :]
        if new.ndim != 2 or new.shape[1] != self.memories.shape[1] or len(new) == 0:
            raise ValueError('New memories must be a nonempty matrix with the existing dimension')
        new_evidence = np.zeros(len(new), np.float32) if evidence is None else np.asarray(evidence, np.float32)
        if new_evidence.shape != (len(new),):
            raise ValueError('New memory and evidence counts differ')
        previous = len(self.memories)
        combined = np.vstack((self._raw_memories, new))
        scores = np.concatenate((self.evidence, new_evidence))
        replacement = type(self)(combined, scores)
        if not np.array_equal(self.memories, replacement.memories[:previous]):
            raise RuntimeError('Appending memories changed an existing stored state')
        self.__dict__.update(replacement.__dict__)
        return np.arange(previous, len(self.memories), dtype=np.int64)

def hz_recall(W, x0, steps=2, alpha=0.25, eps=0.1, lam=0.02):
    W = np.asarray(W, np.float64)
    x = np.asarray(x0, np.float64).copy()
    if x.ndim != 1 or W.shape != (len(x), len(x)):
        raise ValueError('W must be a square matrix matching the state dimension')
    for _ in range(steps):
        h = W @ x
        x = (1.0 - lam) * x + eps * hinge_phi(h, alpha)
    return x

class HingeZeroRetainingLoop:

    def __init__(self, witness, initial_state, drift_boundary=0.15, commit_margin=0.1):
        if not witness.verify(initial_state):
            raise ValueError('Initial checkpoint must be an accepted stored state')
        if not 0.0 <= drift_boundary <= 2.0 or commit_margin < 0.0:
            raise ValueError('Invalid retention thresholds')
        self.witness = witness
        self.checkpoint = HingeZeroState(initial_state.candidate_index, initial_state.state)
        self.working = self.checkpoint.state.copy()
        self.drift_boundary = float(drift_boundary)
        self.commit_margin = float(commit_margin)

    def step(self, cue=None, disturbance=None):
        if cue is not None and disturbance is not None:
            raise ValueError('Supply either a new cue or a working-state disturbance')
        committed = rolled_back = False
        margin = None
        drift = 0.0
        if cue is not None:
            refined = self.witness.refine(cue)
            scores = self.witness.memories @ refined
            order = np.argsort(-scores, kind='stable')
            margin = float(scores[order[0]] - scores[order[1]]) if len(order) > 1 else float('inf')
            proposal = self.witness.observe(cue, scores)
            if margin >= self.commit_margin:
                if not self.witness.verify(proposal):
                    raise RuntimeError('Proposed state failed witness verification')
                self.checkpoint = HingeZeroState(proposal.candidate_index, proposal.state)
                committed = True
            self.working = self.checkpoint.state.copy()
        else:
            if disturbance is not None:
                disturbance = np.asarray(disturbance, np.float32)
                if disturbance.shape != self.working.shape:
                    raise ValueError('Disturbance dimension differs from the working state')
                self.working = _unit(self.working + disturbance)
            drift = 1.0 - float(self.working @ self.checkpoint.state)
            if drift > self.drift_boundary:
                self.working = self.checkpoint.state.copy()
                rolled_back = True
            else:
                self.working = self.witness.refine(self.working)
        if not self.witness.verify(self.checkpoint):
            raise RuntimeError('Retained checkpoint failed witness verification')
        return {'state': HingeZeroState(self.checkpoint.candidate_index, self.checkpoint.state), 'committed': committed, 'rolled_back': rolled_back, 'margin': margin, 'drift': drift}
