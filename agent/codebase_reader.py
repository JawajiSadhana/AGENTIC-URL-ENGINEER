import os

def read_existing_codebase():
    files = []
    for root, dirs, filenames in os.walk("."):
        for name in filenames:
            if name.endswith(".py"):
                files.append(os.path.join(root, name).replace("\\", "/"))
    return {"files": files}
