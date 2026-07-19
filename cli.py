import sys
from agent.orchestrator import run

if __name__ == "__main__":
    req = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else input("Requirement: ")
    run(req)