import streamlit as st
import json
import os
from models import Task, StudentResponse
from conversation import get_student_reply
from transcription import transcribe_audio

# --- Helper Functions ---
def load_tasks(file_path="data/tasks.json"):
    if not os.path.exists(file_path):
        st.error(f"Tasks file not found at {file_path}")
        return []
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        return [Task(**t) for t in data]

def init_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "conversation_ended" not in st.session_state:
        st.session_state.conversation_ended = False
    if "diagnosis" not in st.session_state:
        st.session_state.diagnosis = None
    if "tasks" not in st.session_state:
        st.session_state.tasks = load_tasks()
    if "current_task_index" not in st.session_state:
        st.session_state.current_task_index = 0
    if "audio_mode" not in st.session_state:
        st.session_state.audio_mode = False
    if "last_processed_audio" not in st.session_state:
        st.session_state.last_processed_audio = None
    if "audio_version" not in st.session_state:
        st.session_state.audio_version = 0

def save_session_data(task: Task, messages: list, diagnosis: dict):
    """Saves the conversation and diagnosis to a JSON file in data/."""
    import datetime
    import uuid
    
    # Ensure data directory exists
    os.makedirs("data/sessions", exist_ok=True)
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    session_id = str(uuid.uuid4())[:8]
    filename = f"data/sessions/session_{timestamp}_{session_id}.json"
    
    payload = {
        "timestamp": timestamp,
        "session_id": session_id,
        "task_id": task.id,
        "student_name": task.student_name,
        "messages": messages,
        "diagnosis": diagnosis
    }
    
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    return filename

# --- UI Components ---
def render_header(task: Task):
    """US3: Header with context and math problem."""
    st.markdown(f"### 🏫 Unterrichtssituation: {task.grade_level}")
    st.info(task.situation)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Aufgabe:**")
        # Use a subheader or container for better visibility and automatic text wrapping
        st.info(task.problem_statement)
        st.markdown(f"*Richtige Lösung: {task.correct_solution}*")
    with col2:
        st.markdown("**Schülerlösung (Lukas/Julia):**")
        st.error(task.student_solution)

def render_chat_history():
    """US1: Renders teacher and student messages."""
    for msg in st.session_state.messages:
        role = "user" if msg["role"] == "user" else "assistant"
        # Display name in chat bubble: 'Lehrkraft' vs 'Schüler'
        avatar = "👨‍🏫" if role == "user" else "👦"
        with st.chat_message(role, avatar=avatar):
            # Display logic for teacher messages
            if role == "user" and msg.get("is_audio"):
                st.write("🎤 *Sprachnachricht*")
                with st.expander("Transkription (Debug)"):
                    st.write(msg["content"])
            else:
                st.write(msg["content"])
                
            # Debug/Internal Thought view (expander) for students
            if role == "assistant" and msg.get("internal_thought"):
                with st.expander("Gedankengang (nur Debugging)"):
                    st.caption(msg["internal_thought"])

def handle_input(prompt_text=None, audio_data=None, task=None):
    """US1: Process text or audio input, then get LLM reply."""
    user_text = prompt_text
    
    if audio_data:
        try:
            with st.spinner("Transkribiere Audio..."):
                user_text = transcribe_audio(audio_data)
        except Exception as e:
            st.error(str(e))
            return # Abort if transcription fails
            
    if user_text:
        # 1. Add teacher message
        msg = {"role": "user", "content": user_text}
        if audio_data is not None:
            msg["is_audio"] = True
        st.session_state.messages.append(msg)
        
        # 2. Get student reply with 'thinking' indicator
        with st.chat_message("assistant", avatar="👦"):
            with st.spinner("Schüler denkt nach..."):
                reply: StudentResponse = get_student_reply(st.session_state.messages, task)
                st.write(reply.student_response)
                
                # 3. Save student message
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": reply.student_response,
                    "internal_thought": reply.internal_thought
                })
        
        # We don't call st.rerun() here to avoid loop issues with audio_input
        # Streamlit will naturally update the UI after this function completes

def main():
    st.set_page_config(page_title="Diagnostisches Gesprächstraining", layout="centered")
    init_session_state()
    
    if not st.session_state.tasks:
        st.warning("Keine Aufgaben geladen. Bitte überprüfe data/tasks.json.")
        return

    # --- Sidebar: Task Selector (US3 Enhancement) ---
    with st.sidebar:
        st.title("⚙️ Einstellungen")
        task_names = [f"{t.grade_level}: {t.error_pattern.name}" for t in st.session_state.tasks]
        
        # Selectbox to switch tasks
        new_task_index = st.selectbox(
            "Szenario wählen:", 
            range(len(task_names)), 
            format_func=lambda i: task_names[i],
            index=st.session_state.current_task_index
        )
        
        # Reset conversation if task changes
        if new_task_index != st.session_state.current_task_index:
            st.session_state.current_task_index = new_task_index
            st.session_state.messages = []
            st.session_state.conversation_ended = False
            st.session_state.diagnosis = None
            st.session_state.last_processed_audio = None
            st.rerun()
            
        st.divider()
        if st.button("Gespräch zurücksetzen"):
            st.session_state.messages = []
            st.session_state.conversation_ended = False
            st.session_state.diagnosis = None
            st.session_state.last_processed_audio = None
            st.rerun()

    task = st.session_state.tasks[st.session_state.current_task_index]
    
    # --- 1. Header (Context) ---
    render_header(task)
    st.divider()
    
    # --- Custom CSS for Red 'End Chat' Button ---
    st.markdown("""
        <style>
        /* Targeting the primary button class which we will apply to the 'End Chat' button */
        .stButton > button.st-emotion-cache-19rxjzo.ef3psqc12 {
            background-color: #ff4b4b;
            color: white;
            border-color: #ff4b4b;
        }
        /* More robust selector targeting 'primary' buttons and overriding their style to red */
        div[data-testid="stButton"] button[kind="primary"] {
            background-color: #ff4b4b;
            color: white;
            border-color: #ff4b4b;
        }
        div[data-testid="stButton"] button[kind="primary"]:hover {
            background-color: #ff3333;
            color: white;
            border-color: #ff3333;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # --- 2. Chat Area ---
    render_chat_history()
    
    # --- 3. Input Strategy (US1) ---
    if not st.session_state.conversation_ended:
        # Use key to let Streamlit manage the state directly and avoid toggle lag
        st.toggle("🎙️ Spracheingabe nutzen", key="audio_mode")
        
        if st.session_state.audio_mode:
            # Use a dynamic key to force a reset of the widget after each recording
            audio_widget_key = f"audio_input_{st.session_state.audio_version}"
            audio_file = st.audio_input("Frage den Schüler...", key=audio_widget_key)
            
            if audio_file:
                # Create a unique ID for the current audio file
                audio_id = f"{audio_file.name}_{audio_file.size}"
                if st.session_state.last_processed_audio != audio_id:
                    st.session_state.last_processed_audio = audio_id
                    handle_input(audio_data=audio_file.getvalue(), task=task)
                    # Increment the version to clear the widget on next rerun
                    st.session_state.audio_version += 1
                    st.rerun() # Single rerun to refresh chat view after processing
        else:
            # Use text_area + button for multi-line support instead of single-line chat_input
            with st.container():
                placeholder_text = f"Hallo {task.student_name}, ..."
                prompt = st.text_area("Deine Frage an den Schüler:", placeholder=placeholder_text, height=100)
                
                # US1 & US2: Place 'Send' and 'End' buttons side-by-side
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Frage senden", use_container_width=True):
                        if prompt:
                            handle_input(prompt_text=prompt, task=task)
                            st.rerun()
                with col2:
                    if st.button("Diagnose abgeben (Chat beenden)", use_container_width=True, type="primary"):
                        st.session_state.conversation_ended = True
                        st.rerun()

        # In audio mode, we still show the diagnosis button below the audio input
        if st.session_state.audio_mode:
            st.divider()
            if st.button("Diagnose abgeben (Chat beenden)", use_container_width=True, type="primary"):
                st.session_state.conversation_ended = True
                st.rerun()
                
    # --- 4. Diagnosis (US2) ---
    if st.session_state.conversation_ended:
        st.divider()
        st.subheader("🎓 Diagnoseabgabe")
        
        if st.session_state.diagnosis is None:
            with st.form("diagnosis_form"):
                st.write("Welche Fehlvorstellung hast du bei Lukas erkannt?")
                
                # Single-Choice Options (US2)
                options = [opt.label for opt in task.diagnosis_options]
                selected_label = st.radio("Fehlvorstellung wählen:", options)
                
                # Free-text Field (US2)
                free_text = st.text_area("Beschreibe den Gedankengang des Schülers in eigenen Worten:", placeholder="Lukas denkt, dass...")
                
                submitted = st.form_submit_button("Diagnose einreichen")
                if submitted:
                    st.session_state.diagnosis = {
                        "selected": selected_label,
                        "text": free_text
                    }
                    # Save session data (US2 Extension: Persistence)
                    try:
                        saved_path = save_session_data(task, st.session_state.messages, st.session_state.diagnosis)
                        st.success(f"💾 Konversation gespeichert in {saved_path}")
                    except Exception as e:
                        st.error(f"⚠️ Fehler beim Speichern: {str(e)}")
                    st.rerun()
        else:
            # Final Summary (US2)
            st.success("✅ Diagnose erfolgreich abgegeben!")
            st.markdown(f"**Deine Wahl:** {st.session_state.diagnosis['selected']}")
            st.markdown(f"**Deine Begründung:** {st.session_state.diagnosis['text']}")
            
            # Show if correct (pedagogical feedback)
            correct_opt = next((opt for opt in task.diagnosis_options if opt.label == st.session_state.diagnosis['selected']), None)
            if correct_opt and correct_opt.is_correct:
                st.info("💡 **Feedback:** Deine Wahl entspricht dem hinterlegten Fehlermuster.")
            else:
                st.warning("💡 **Feedback:** Das hinterlegte Fehlermuster war ein anderes.")
                
            if st.button("Training neustarten / Nächste Aufgabe"):
                # Reset session state for next round
                st.session_state.messages = []
                st.session_state.conversation_ended = False
                st.session_state.diagnosis = None
                # Cycle task
                st.session_state.current_task_index = (st.session_state.current_task_index + 1) % len(st.session_state.tasks)
                st.rerun()

if __name__ == "__main__":
    main()
