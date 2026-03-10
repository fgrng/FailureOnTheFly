from pydantic import BaseModel, Field
from typing import List, Optional

class ErrorPattern(BaseModel):
    name: str
    description: str
    system_prompt: str

class DiagnosisOption(BaseModel):
    label: str
    description: str
    is_correct: bool

class Task(BaseModel):
    id: str
    student_name: str
    situation: str
    problem_statement: str
    correct_solution: str
    student_solution: str
    grade_level: str
    error_pattern: ErrorPattern
    diagnosis_options: List[DiagnosisOption]

class StudentResponse(BaseModel):
    """The structured response from the simulated student."""
    student_response: str = Field(description="The visible text the student says in the chat.")
    internal_thought: Optional[str] = Field(
        default=None, 
        description="Internal reasoning or state of mind of the student (not shown to the teacher)."
    )

class DiagnosisSubmission(BaseModel):
    """The final diagnosis submitted by the teacher."""
    selected_option: str
    free_text: str
