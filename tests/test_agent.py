import pytest
from agent.planner import create_plan

def test_planner_returns_tasks():
    plan = create_plan("build url shortener")
    assert len(plan["tasks"]) > 5
    assert any("file_write" in t for t in plan["tasks"])
    assert plan["is_ambiguous"] == False

def test_validator_blocks_dangerous():
    from agent.validator import validate
    with pytest.raises(ValueError):
        validate("file_write: rm -rf /")