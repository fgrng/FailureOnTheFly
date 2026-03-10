# Data Model: FailureOnTheFly

**Date**: 2026-03-10
**Feature**: 001-diagnostic-training-sim

## Task Definition (`tasks.json`)

A single JSON file containing predefined math tasks. For the prototype, exactly one task.

```json
{
  "situation": "Du gehst durch die Klasse und schaust dir die Hefte an...",
  "problem_statement": "Berechne 348 + 275",
  "correct_solution": "623",
  "student_solution": "5113",
  "grade_level": "Klasse 3",
  "error_pattern": {
    "name": "Stellenwertfehler bei Addition",
    "description": "Der Schüler addiert jede Stelle einzeln ohne Übertrag",
    "system_prompt": "Du bist ein Schüler der 3. Klasse, der..."
  },
  "diagnosis_options": [
    {"label": "Stellenwertfehler", "description": "Addiert stellenweise ohne Übertrag", "is_correct": true},
    {"label": "Operatorverwechslung", "description": "Verwechselt Addition mit anderer Rechenart", "is_correct": false},
    {"label": "Zahlendreher", "description": "Vertauscht Ziffern beim Abschreiben", "is_correct": false}
  ]
}
```

No IDs, no foreign keys, no separate entities — it's a single JSON object loaded at startup.

## Session State (`st.session_state`)

All runtime state lives in Streamlit's session state. No persistence, no database.

```python
st.session_state.messages       # list[dict] with keys: role, content, internal_thought (optional)
st.session_state.conversation_ended  # bool — True after "Ich bin jetzt so weit"
st.session_state.diagnosis      # dict or None — {selected_option: str, text: str}
st.session_state.task           # dict — the loaded task from tasks.json
```

### Message format

Messages passed to instructor use only `role` and `content`. The `internal_thought` field is stored alongside for debugging but not sent back to the LLM.

```python
{"role": "user", "content": "Wie hast du das gerechnet?"}
{"role": "assistant", "content": "Ich hab einfach 3+2, 4+7, 8+5 gerechnet", "internal_thought": "Ich weiß nicht was ein Übertrag ist"}
```

## StudentResponse (Instructor Model)

The Pydantic model returned by instructor from the LLM.

| Field | Type | Description |
|-------|------|-------------|
| student_response | text | The text displayed in the chat UI as the student's reply |
| internal_thought | text (optional) | What the student thinks but doesn't say — for debugging simulation quality |
