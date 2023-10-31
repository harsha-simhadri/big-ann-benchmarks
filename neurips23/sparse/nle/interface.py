from pyterrier_pisa import _pisathon
from enum import Enum
import numpy as np
import json
import sys
from pathlib import Path
import tempfile
import os
import more_itertools
from warnings import warn
from collections import Counter, defaultdict
import functools
import ir_datasets
import time 
import operator
import itertools
import copy
from multiprocessing import cpu_count

_logger = ir_datasets.log.easy()

def sort_dict_by_value_descending(dict_):
    if isinstance(dict_,dict):
      return sorted(dict_.items(), key=operator.itemgetter(1), reverse=True)  
    else:
      return sorted(dict_, key=operator.itemgetter(1), reverse=True)  
def prune_by_size(dict_, size_to_prune):
  if size_to_prune <= 0:
    return dict_
  else:
    return {str(key): value for idx, (key, value) in enumerate(sort_dict_by_value_descending(dict_)) if idx < size_to_prune}    

def prune_by_size_no_sort(dict_, size_to_prune):
  if size_to_prune <= 0:
    return dict_
  else:
    return {str(key): value for (key, value) in dict_[:size_to_prune]}    


def numbers_to_letters(str_):
  return str(str_)
  new_str = ""
  for letter in str(str_):
    new_str += chr(65+int(letter))
  return new_str

class PisaIndexingMode(Enum):
  create = 'create'
  overwrite = 'overwrite'

class PisaStemmer(Enum):
  """
  Represents a built-in stemming function from PISA
  """
  none = 'none'
  porter2 = 'porter2'
  krovetz = 'krovetz'


class PisaScorer(Enum):
  """
  Represents a built-in scoring function from PISA
  """
  bm25 = 'bm25'
  dph = 'dph'
  pl2 = 'pl2'
  qld = 'qld'
  quantized = 'quantized'
  saturated_tf = 'saturated_tf'

class PisaIndexEncoding(Enum):
  """
  Represents a built-in index encoding type from PISA.
  """
  ef = 'ef'
  single = 'single'
  pefuniform = 'pefuniform'
  pefopt = 'pefopt'
  block_optpfor = 'block_optpfor'
  block_varintg8iu = 'block_varintg8iu'
  block_streamvbyte = 'block_streamvbyte'
  block_maskedvbyte = 'block_maskedvbyte'
  block_interpolative = 'block_interpolative'
  block_qmx = 'block_qmx'
  block_varintgb = 'block_varintgb'
  block_simple8b = 'block_simple8b'
  block_simple16 = 'block_simple16'
  block_simdbp = 'block_simdbp'


class PisaQueryAlgorithm(Enum):
  """
  Represents a built-in query algorithm
  """
  wand = 'wand'
  block_max_wand = 'block_max_wand'
  block_max_maxscore = 'block_max_maxscore'
  block_max_ranked_and = 'block_max_ranked_and'
  ranked_and = 'ranked_and'
  ranked_or = 'ranked_or'
  maxscore = 'maxscore'


class PisaStopwords(Enum):
  """
  Represents which set of stopwords to use during retrieval
  """
  terrier = 'terrier'
  none = 'none'


PISA_INDEX_DEFAULTS = {
  'stemmer': PisaStemmer.none,
  'index_encoding': PisaIndexEncoding.block_simdbp,
  'query_algorithm': PisaQueryAlgorithm.wand,
  'stops': PisaStopwords.none,
}


def log_level(on=True):
  _pisathon.log_level(1 if on else 0)


class PisaIndex():
  def __init__(self,
      path: str, threads: int = 8, overwrite=False, scale=100):
    self.path = path
    stemmer = PisaStemmer('none')
    stops = PISA_INDEX_DEFAULTS['stops']
    self.stemmer = stemmer
    self.threads = threads
    self.overwrite = overwrite
    self.stops = stops
    self.scale = 100
    self.index_encoding = PISA_INDEX_DEFAULTS['index_encoding']
    self.n_cores = 8

  def generate_forward(self):
    _pisathon.generate_fwd(self.path+"/inv")

  def load_forward(self):
    _pisathon.prepare_fwd(self.path+"/inv.fwd")

  def load_inv(self,index2, k, k1, k2, 
  query_algorithm="rescored_wand",
  scorer=PisaScorer.saturated_tf,bm25_k1=100,**retr_args):
    print(bm25_k1)
    _pisathon.prepare_index(self.path, encoding=self.index_encoding.value, scorer_name=PisaScorer.saturated_tf.value,bm25_k1=bm25_k1)
    _pisathon.prepare_inv(index_dir=self.path,
          index_dir_full=index2.path,
          scorer_name=scorer.value,
          stemmer='',
          k=k,
          threads=self.n_cores,
          stop_fname='',
          query_weighted=1,
          pretokenised=True,
          bm25_k1=bm25_k1,)


  def index(self, it,t=0):
    print("Indexing with {}".format(t))
    mode = PisaIndexingMode.overwrite if self.overwrite else PisaIndexingMode.create
    lexicon = {}
    path = Path(self.path)
    if not self.overwrite:
        if os.path.isfile(path/'fwd.documents'):
            raise Exception("Trying to overwrite index outside overwrite mode")
    with (path/'fwd.documents').open('wt') as f_docs, (path/'fwd.terms').open('wt') as f_lex:
      docid = 0
      for bidx, batch in enumerate(it):
        _logger.info(f'inverting batch {bidx}: documents [{docid},{docid+batch.shape[0]})')
        inv_did = defaultdict(list)
        inv_score = defaultdict(list)
        lens = []
        for i in range(batch.shape[0]):
          _, col = batch[i].nonzero()
          values = [float(batch[i,j]) for j in col]
          pre_dict = {c: v for c,v in zip(col,values)}
          the_dict = prune_by_size(pre_dict,t)
          l = 0
          f_docs.write(str(docid)+'\n')
          for term, score in the_dict.items():
            term = numbers_to_letters(str(term))
            score = int(score * self.scale)
            if score <= 0:
              continue
            l += score
            if term not in lexicon:
              lexicon[term] = len(lexicon)
              f_lex.write(term+'\n')
            inv_did[lexicon[term]].append(docid)
            inv_score[lexicon[term]].append(int(score))
          lens.append(l)
          docid += 1
        with (path/f'inv.batch.{bidx}.docs').open('wb') as f_did, (path/f'inv.batch.{bidx}.freqs').open('wb') as f_score, (path/f'inv.batch.{bidx}.sizes').open('wb') as f_len:
          f_did.write(np.array([1, batch.shape[0]], dtype=np.uint32).tobytes())
          for i in range(len(lexicon)):
            l = len(inv_did[i])
            f_did.write(np.array([l] + inv_did[i], dtype=np.uint32).tobytes())
            f_score.write(np.array([l] + inv_score[i], dtype=np.uint32).tobytes())
          f_len.write(np.array([len(lens)] + lens, dtype=np.uint32).tobytes())
    _pisathon.merge_inv(str(path/'inv'), bidx+1, len(lexicon))
    for i in range(bidx+1):
      (path/f'inv.batch.{i}.docs').unlink()
      (path/f'inv.batch.{i}.freqs').unlink()
      (path/f'inv.batch.{i}.sizes').unlink()
    (path/'inv.docs').rename(path/'inv.docs.tmp')
    (path/'inv.freqs').rename(path/'inv.freqs.tmp')
    in_docs = np.memmap(path/'inv.docs.tmp', mode='r', dtype=np.uint32)
    in_freqs = np.memmap(path/'inv.freqs.tmp', mode='r', dtype=np.uint32)
    with (path/'fwd.terms').open('wt') as f_lex, (path/'inv.docs').open('wb') as f_docs, (path/'inv.freqs').open('wb') as f_freqs:
      f_docs.write(in_docs[:2].tobytes())
      in_docs = in_docs[2:]
      offsets_lens = []
      i = 0
      while i < in_docs.shape[0]:
        offsets_lens.append((i, in_docs[i]+1))
        i += in_docs[i] + 1
      for term in _logger.pbar(sorted(lexicon), desc='re-mapping term ids'):
        f_lex.write(f'{term}\n')
        i = lexicon[term]
        start, l = offsets_lens[i]
        f_docs.write(in_docs[start:start+l])
        f_freqs.write(in_freqs[start:start+l])
    del in_docs # close mmap
    del in_freqs # close mmap
    (path/'inv.docs.tmp').unlink()
    (path/'inv.freqs.tmp').unlink()
    _pisathon.build_binlex(str(path/'fwd.documents'), str(path/'fwd.doclex'))
    _pisathon.build_binlex(str(path/'fwd.terms'), str(path/'fwd.termlex'))
    _pisathon.prepare_index(self.path, encoding=self.index_encoding.value, scorer_name=PisaScorer.quantized.value)
    _pisathon.prepare_index(self.path, encoding=self.index_encoding.value, scorer_name=PisaScorer.saturated_tf.value,bm25_k1=100)

  def retrieve(self, index2, queries, k, k1, k2, 
  query_algorithm="rescored_wand",
  scorer=PisaScorer.saturated_tf,bm25_k1=100,**retr_args):
    _pisathon.prepare_index(self.path, encoding=self.index_encoding.value, scorer_name=PisaScorer.saturated_tf.value,bm25_k1=bm25_k1)
    _pisathon.prepare_index(index2.path, encoding=self.index_encoding.value, scorer_name=PisaScorer.saturated_tf.value,bm25_k1=bm25_k1)
    inp = []
    queries = queries.tolil()
    result = ( (r, ( (str(c),float(int(100*v))) for c,v in zip(b[0],b[1]))) for r,b in enumerate(zip(queries.rows,queries.data)))
    result = ( (r, sorted(c, key=operator.itemgetter(1), reverse=True)  ) for r,c in result)
    inp = tuple((r, prune_by_size_no_sort(c,k1), prune_by_size_no_sort(c,k2) ) for r,c in result)
    with tempfile.TemporaryDirectory() as d:
      shape = (queries.shape[0] * k,)
      result_qidxs = np.ascontiguousarray(np.empty(shape, dtype=np.int32))
      result_docnos = np.ascontiguousarray(np.empty(shape, dtype=object))
      result_ranks = np.ascontiguousarray(np.empty(shape, dtype=np.int32))
      result_scores = np.ascontiguousarray(np.empty(shape, dtype=np.float32))
      size = _pisathon.retrieve(
        index_dir=self.path,
        encoding=self.index_encoding.value,
        algorithm=query_algorithm,
        scorer_name=scorer.value,
        stemmer='',
        queries=inp,
        k=k,
        threads=8,
        stop_fname='',
        query_weighted=1,
        pretokenised=True,
        result_qidxs=result_qidxs,
        result_docnos=result_docnos,
        result_ranks=result_ranks,
        result_scores=result_scores,
        bm25_k1=bm25_k1,
        **retr_args)

    if size < queries.shape[0] * k:
      print("DID NOT DO THINGS RIGHT")
      print(size)
      raise Exception("LEL")
    result = dict()
    qidxs = np.argsort(result_qidxs.reshape(-1,k)[:,0])
    docnos = result_docnos.reshape(-1,k).astype(np.int32)[qidxs]
    return docnos
