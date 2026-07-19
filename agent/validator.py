def validate(task: str):
    dangerous = ["rm -rf", "DROP TABLE", "os.system"]
    if any(d in task for d in dangerous): raise ValueError(f"BLOCKED: {task}")
    return True