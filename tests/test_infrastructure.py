import pytest
import os
import json
from models import Task, StudentResponse
from app import load_tasks

def test_pydantic_models():
    """Validates the basic Pydantic structure for responses."""
    resp = StudentResponse(student_response="Hallo Lehrer!")
    assert resp.student_response == "Hallo Lehrer!"
    assert resp.internal_thought is None

def test_load_tasks():
    """Checks if the data/tasks.json can be loaded into Task objects."""
    # We load from the actual file
    tasks = load_tasks("data/tasks.json")
    assert len(tasks) > 0
    assert isinstance(tasks[0], Task)
    # Check for IDs from our earlier file creation
    assert tasks[0].id == "math-001-equals-sign"

def test_env_vars_presence():
    """Ensures necessary environment variables are documented."""
    # We check if .env or a provided env is present
    assert os.path.exists(".env") or os.getenv("OPENAI_API_KEY") is not None
