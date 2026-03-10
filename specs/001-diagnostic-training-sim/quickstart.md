# Quickstart: Diagnostisches Gesprächstraining

**Feature**: 001-diagnostic-training-sim

## Prerequisites

- Python 3.11+
- OpenAI API key (for Whisper; also for LLM if using OpenAI provider)
- Anthropic API key (only if using `LLM_PROVIDER=anthropic`)

## Setup

```bash
# Install dependencies
pip install streamlit openai instructor pydantic anthropic

# Set API keys
export OPENAI_API_KEY="your-key-here"           # Required (Whisper always uses OpenAI)
# export ANTHROPIC_API_KEY="your-key-here"      # Only if LLM_PROVIDER=anthropic

# Optional: switch LLM provider (default: openai)
# export LLM_PROVIDER=anthropic
# export LLM_MODEL=claude-sonnet-4-6

# Run the app
streamlit run app.py
```

## Usage

1. Open `http://localhost:8501` in a desktop browser (Chrome/Firefox recommended)
2. The math task with the student's incorrect solution is displayed in the sidebar
3. Use the chat input to type a question or click the mic button to record one
4. The simulated student responds — continue the diagnostic conversation
5. Click "Gespräch beenden" when ready to diagnose
6. Enter your diagnosis of the student's error pattern
7. Review the conversation summary

## Project Structure

```
app.py                   # Streamlit app entry point, page layout, UI flow
models.py                # Pydantic models (instructor response models + data structures)
conversation.py          # LLM conversation logic via instructor
llm_provider.py          # LLM provider abstraction (switchable via env var)
transcription.py         # Whisper API integration
data/
└── tasks.json           # Predefined math tasks with error patterns
```

## Key Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENAI_API_KEY` | Yes | OpenAI API key (always required for Whisper; also for LLM if provider is openai) |
| `ANTHROPIC_API_KEY` | Conditional | Required only if `LLM_PROVIDER=anthropic` |
| `LLM_PROVIDER` | No | LLM provider: `openai` (default) or `anthropic` |
| `LLM_MODEL` | No | LLM model name (default: provider-specific, e.g. `gpt-4o-mini` for openai) |
