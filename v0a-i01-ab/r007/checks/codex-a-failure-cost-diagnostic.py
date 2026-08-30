import importlib.util, json, traceback
from dataclasses import replace, asdict
from pathlib import Path

def main():
    spec = importlib.util.spec_from_file_location("independent_prior", Path(__file__).with_name("codex-a-adversarial-v5.py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    fixture = replace(module.FIXTURE_A, script=(module.replay.ScriptedAction("preflop", 3, "call"),))
    try:
        module.measured_native_control(fixture, "diagnostic-failure-cost", "event_order")
    except AssertionError as error:
        item = error.__traceback__
        while item is not None:
            if item.tb_frame.f_code.co_name == "measured_native_control":
                values = item.tb_frame.f_locals
                print(json.dumps({"expected_costs": values["totals"],
                    "receipt": asdict(values["outcome"].receipt),
                    "terminal": values["terminal"], "operation_calls": values["calls"]},
                    default=str), flush=True)
            item = item.tb_next
        raise
