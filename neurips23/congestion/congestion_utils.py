import os
import multiprocessing


def bind_to_core(core_id):
    """
    Bind the current process to a specific CPU core.

    Args:
        core_id (int): The ID of the core to bind to. Use -1 for default OS scheduling.

    Returns:
        int: The core ID the process is bound to, or -1 if OS scheduling is used.
    """
    if core_id == -1:  # OS scheduling
        return -1
    max_cpus = os.cpu_count()
    if max_cpus is None:
        raise RuntimeError("Could not determine the number of CPUs.")
    cpu_id = core_id % max_cpus
    try:
        pid = os.getpid()
        os.sched_setaffinity(pid, {cpu_id})  # Set CPU affinity
        return cpu_id
    except AttributeError:
        raise NotImplementedError("sched_setaffinity is not available on this system.")
    except Exception as e:
        print(f"Error: {e}")
        return -1


if __name__ == "__main__":
    core = bind_to_core(0)
    if core != -1:
        print(f"Process is bound to core {core}")
    else:
        print("OS scheduling is used (not bound to a specific core).")