"""Standalone: cost of running an allocation-heavy loop under tracemalloc.
No project code. Shaped like eval_bridge.hand_totals' inner loop (990 villains,
a strengths list plus a couple of small tuples/lists per villain)."""
import time, tracemalloc

def workload(villains=990):
    total = 0
    for v in range(villains):
        strengths = [ (v * i) % 7919 for i in range(7) ]
        a = tuple(sorted(strengths))
        b = [a[0] - a[-1], a[1] + a[2]]
        total += b[0] + b[1]
    return total

def timed(use_tracemalloc, reps=200):
    best = None
    for _ in range(reps):
        if use_tracemalloc:
            tracemalloc.start()
        t = time.perf_counter()
        workload()
        if use_tracemalloc:
            tracemalloc.get_traced_memory()
            tracemalloc.stop()
        dt = time.perf_counter() - t          # as measure() does: clock read AFTER stop
        best = dt if best is None else min(best, dt)
    return best

plain = timed(False)
traced = timed(True)
print(f"python           {__import__('sys').version.split()[0]}")
print(f"plain    best-of-200: {plain*1000:8.3f} ms")
print(f"traced   best-of-200: {traced*1000:8.3f} ms")
print(f"inflation factor    : {traced/plain:8.2f}x")
print(f"overhead per call   : {(traced-plain)*1000:8.3f} ms")
