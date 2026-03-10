import os
import instructor
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def get_instructor_client():
    """
    Returns a patched instructor client based on environment variables.
    Defaults to OpenAI.
    """
    provider = os.getenv("LLM_PROVIDER", "openai").lower()
    model = os.getenv("LLM_MODEL", "gpt-4o-mini")
    
    if provider == "openai":
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        return instructor.from_openai(client), model
    
    # Fallback/Additional providers can be added here
    # e.g., anthropic, google, etc.
    raise ValueError(f"Unsupported LLM_PROVIDER: {provider}")

def get_transcription_client():
    """
    Returns a standard OpenAI client for transcription (Whisper).
    """
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
