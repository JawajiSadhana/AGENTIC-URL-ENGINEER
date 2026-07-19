import json
import os
from planner import create_plan
from executor import execute_task
from datetime import datetime

def log_trace(step, detail):
    os.makedirs("../logs", exist_ok=True)  # .. se upar jao
    trace = {"timestamp": datetime.now().isoformat(), "step": step, "detail": detail}
    with open("../logs/traces.jsonl", "a") as f:  # .. add kiya
        f.write(json.dumps(trace) + "\n")

def run(requirement: str):
    print(f"\nAgent received requirement: {requirement}")
    log_trace("INPUT", requirement)

    plan = create_plan(requirement)
    print(f"\nAgent Plan: {len(plan['tasks'])} tasks found")
    for i, t in enumerate(plan['tasks'], 1):
        print(f"{i}. {t}")
    print(f"\nRisks: {plan['risks']}")

    if plan['is_ambiguous']:
        print(f"\nAgent Question: {plan['questions'][0]}")
        return

    approval = input("\nApprove this plan? [y/n]: ")
    if approval.lower()!= 'y':
        print("Aborted.");
        return

    for task in plan['tasks']:
        print(f"\nExecuting: {task}")
        result = execute_task(task)
        print(f"Result: {result}")
        log_trace("EXECUTE", {"task": task, "result": result})

    print("\nAgent Finished. All tasks completed.")