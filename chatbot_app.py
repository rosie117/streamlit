import streamlit as st

st.set_page_config(page_title="Quiz Challenge", layout="centered")

# ✅ Audio
SUCCESS_SOUND = "https://actions.google.com/sounds/v1/cartoon/clang_and_wobble.ogg"
FAIL_SOUND = "https://actions.google.com/sounds/v1/cartoon/wood_plank_flicks.ogg"

def play_sound(url):
    st.markdown(
        f"""
        <audio autoplay>
            <source src="{url}" type="audio/mpeg">
        </audio>
        """,
        unsafe_allow_html=True,
    )

# ✅ Topic-based question banks
TOPIC_QUESTIONS = {
    "Astronomy": [
        {"question": "Which planet is known as the Red Planet?", "options": ["Earth", "Mars", "Venus"], "answer": "Mars"},
        {"question": "How many moons does Earth have?", "answer": "1"},
    ],
    "History": [
        {"question": "In which year did World War II end?", "options": ["1943", "1945", "1950"], "answer": "1945"},
        {"question": "Who was the first president of the United States?", "answer": "George Washington"},
    ],
    "Entertainment": [
        {"question": "When was Lkr born?", "options": ["2000", "2001", "2002", "2003"], "answer": "2002"},
        {"question": "Who is shown in this photo?", "options": ["Xiao Wang", "Lkr", "Zhang San"], "answer": "Lkr", "image": "profile photo.jpg"},
    ]
}

# ✅ Initialize state
if "started" not in st.session_state:
    st.session_state.started = False
if "topic" not in st.session_state:
    st.session_state.topic = None
if "questions" not in st.session_state:
    st.session_state.questions = []
if "step" not in st.session_state:
    st.session_state.step = 0
if "failed" not in st.session_state:
    st.session_state.failed = False
if "completed" not in st.session_state:
    st.session_state.completed = False
if "history" not in st.session_state:
    st.session_state.history = []

def restart():
    st.session_state.started = False
    st.session_state.topic = None
    st.session_state.questions = []
    st.session_state.step = 0
    st.session_state.failed = False
    st.session_state.completed = False
    st.session_state.history = []

# ✅ Title and Instructions
st.title("🧠 Quiz Challenge Game")
st.caption("You must answer all questions correctly to win.")

# ✅ Topic Selection
if not st.session_state.started:
    st.subheader("Select a topic to begin:")
    topic = st.radio("Choose your challenge topic:", list(TOPIC_QUESTIONS.keys()), key="topic_selector")
    if st.button("Start"):
        st.session_state.topic = topic
        st.session_state.questions = TOPIC_QUESTIONS[topic]
        st.session_state.started = True
        st.rerun()
    st.stop()

# ✅ Display chat history
for entry in st.session_state.history:
    st.chat_message("assistant").markdown(entry["question"])
    if entry.get("image"):
        st.image(entry["image"], caption="Reference Image", use_container_width=True)
    st.chat_message("user").markdown(entry["user_answer"])

# ✅ Game in progress
if not st.session_state.failed and not st.session_state.completed:
    curr = st.session_state.step
    q = st.session_state.questions[curr]

    with st.chat_message("assistant"):
        st.markdown(q["question"])
        if q.get("image"):
            st.image(q["image"], caption="Reference Image", use_container_width=True)
        if "options" in q:
            st.markdown("Options: " + ", ".join(q["options"]))

    user_input = st.chat_input("Your answer:")

    if user_input:
        # Record
        st.session_state.history.append({
            "question": q["question"],
            "user_answer": user_input,
            "image": q.get("image")
        })

        # Check answer
        if user_input.strip() == q["answer"]:
            st.session_state.step += 1
            if st.session_state.step >= len(st.session_state.questions):
                st.session_state.completed = True
                play_sound(SUCCESS_SOUND)
                st.chat_message("assistant").success("🎉 Congratulations! You completed the challenge!")
                st.chat_message("assistant").button("Restart", on_click=restart)
            else:
                st.rerun()
        else:
            st.session_state.failed = True
            play_sound(FAIL_SOUND)
            st.chat_message("assistant").error("❌ Incorrect answer. Game over.")
            st.chat_message("assistant").button("Restart", on_click=restart)

# ✅ Restart if done or failed
elif st.session_state.failed or st.session_state.completed:
    if st.button("Restart"):
        restart()
