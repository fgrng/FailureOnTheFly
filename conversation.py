from llm_provider import get_instructor_client
from models import StudentResponse, Task

def get_student_reply(messages, task: Task):
    """
    Calls the LLM via instructor to get a structured student response.
    
    Args:
        messages: List of message dictionaries (role/content)
        task: Current Task object (contains system prompt)
        
    Returns:
        StudentResponse object.
    """
    client, model = get_instructor_client()
    
    # Prepare system message based on task error pattern
    system_msg = {
        "role": "system",
        "content": task.error_pattern.system_prompt
    }
    
    # Send all messages (system + history) to the instructor client
    all_messages = [system_msg] + messages
    
    try:
        response = client.chat.completions.create(
            model=model,
            response_model=StudentResponse,
            messages=all_messages,
            # For robustness, we might want to cap the context or add specific instructions
        )
        return response
    except Exception as e:
        # Standard fallback if LLM fails
        return StudentResponse(
            student_response=f"Ups, ich glaube ich hab dich nicht ganz verstanden... ({str(e)})",
            internal_thought="API Error occurred"
        )
