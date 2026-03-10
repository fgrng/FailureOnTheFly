import os
import io
from llm_provider import get_transcription_client

def transcribe_audio(audio_data):
    """
    Transcribes audio bytes using OpenAI Whisper API.
    
    Args:
        audio_data: Bytes-like object (e.g., WAV from Streamlit st.audio_input)
        
    Returns:
        Transcribed text as string.
    """
    client = get_transcription_client()
    
    # OpenAI Whisper API requires a filename-like object
    buffer = io.BytesIO(audio_data)
    buffer.name = "audio.wav"
    
    try:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=buffer,
            language="de"
        )
        return transcript.text
    except Exception as e:
        # Raise the error so the caller can decide how to handle it
        raise RuntimeError(f"Transkriptionsfehler: {str(e)}")
