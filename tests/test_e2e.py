import pytest
from conversation import get_student_reply
from models import Task

@pytest.fixture
def mock_task():
    return Task(
        id="test-task",
        student_name="Test-Schüler",
        situation="Test Situation",
        problem_statement="1+1",
        correct_solution="2",
        student_solution="3",
        grade_level="1",
        error_pattern={
            "name": "Test Error",
            "description": "Always says 3",
            "system_prompt": "Antworte immer mit '3' und beharre darauf, dass 1+1=3 ist."
        },
        diagnosis_options=[]
    )

def test_student_response_consistency(mock_task):
    """Verifies that the student (LLM) follows the error pattern."""
    messages = [{"role": "user", "content": "Wie viel ist 1 + 1?"}]
    response = get_student_reply(messages, mock_task)
    
    # We check if '3' is in the answer
    assert "3" in response.student_response
    assert response.internal_thought is not None
