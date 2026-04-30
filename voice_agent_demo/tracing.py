from contextlib import contextmanager
from time import perf_counter

from voice_agent_demo.models import StageTrace


@contextmanager
def stage_timer(stage, traces, **metadata):
    started = perf_counter()
    try:
        yield
    finally:
        elapsed_ms = round((perf_counter() - started) * 1000, 3)
        traces.append(StageTrace(stage=stage, latency_ms=elapsed_ms, metadata=metadata))

