import streamlit as st

st.set_page_config(page_title="Quiz Challenge", layout="centered")

# ✅ 音效链接
SUCCESS_SOUND = "https://actions.google.com/sounds/v1/cartoon/clang_and_wobble.ogg"
FAIL_SOUND = "https://actions.google.com/sounds/v1/cartoon/wood_plank_flicks.ogg"
CORRECT_SOUND = "https://actions.google.com/sounds/v1/cartoon/concussive_drum_hit.ogg"

def play_sound(url):
    st.markdown(
        f"""
        <audio autoplay>
            <source src="{url}" type="audio/mpeg">
        </audio>
        """,
        unsafe_allow_html=True,
    )

# ✅ 新问题列表
TOPIC_QUESTIONS = {
    "Hong Kong General": [
        {"question": "🔍 Q1: In Hong Kong, people usually drive on the __________ side of the road.", "answer": "left"},
        {"question": "🔍 Q2: The __________ is one of the most commonly used public transport cards in Hong Kong.", "answer": "Octopus Card"},
        {"question": "🔍 Q3: The MTR system in Hong Kong stands for __________.", "answer": "Mass Transit Railway"},
        {"question": "🔍 Q4: The famous shopping district known for luxury brands and the Star Ferry terminal is called __________.", "answer": "Tsim Sha Tsui"},
        {"question": "🔍 Q5: The public university in Hong Kong located in Sha Tin and known for its spacious campus is __________.", "answer": "CUHK"},
    ],
    "CUHK MSc Marketing": [
        {"question": "🧩 Q1: In which year was CUHK’s MSc in Marketing program established?", "options": ["2001", "2008", "2011", "2018"], "answer": "2008"},
        {"question": "🧩 Q2: Which faculty hosts the MSc in Marketing program at CUHK?", "options": ["Faculty of Arts", "Faculty of Business Administration", "Faculty of Education", "Faculty of Law"], "answer": "Faculty of Business Administration"},
        {"question": "🧩 Q3: Which statement about the CUHK MSc in Marketing program is true?", "options": ["It is taught entirely in Cantonese.", " It accepts only applicants with a business undergraduate degree.", "It offers training in digital marketing and analytics.", "It does not allow international students."], "answer": "It offers training in digital marketing and analytics."},
        {"question": "🧩 Q4: Which two tracks are typically offered in CUHK’s MSc in Marketing program?", "options": ["Big Data Marketing / Managerial Marketing ", "FinTech and Blockchain", "Public Health / Biotech Management", " Brand & Advertising / Customer Analytics"], "answer": "Brand & Advertising / Customer Analytics"},
        {"question": "🧩 Q5: Who is the instructor of the “Machine Learning in Marketing” course in CUHK’s MSc in Marketing program?", "options": ["Professor Chenxi Liao", "Professor Francisco", "Professor Jingbo Wang", "Professor Stephen Hawking"], "answer": "Professor Jingbo Wang"},
    ]
}

# ✅ 状态初始化
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

# ✅ 标题和简介
st.title("🎯 MKTers' Game Challenge")
st.markdown("""
**Welcome to the MKTers' Game!💡**

In this game, you'll choose from two tracks, each containing 5 carefully crafted questions.

**Game Rules:**
- Each track includes 5 questions;
- You must answer ❗️all questions correctly❗️ to complete the challenge;
- If you get even one wrong, the game ends immediately;
- Every attempt is a fresh start — stay sharp!

**Good luck, and enjoy the challenge!❤️‍🔥**
""")

# ✅ 选择话题
if not st.session_state.started:
    st.subheader("Select a topic to begin:")
    topic = st.radio("Choose your challenge topic:", list(TOPIC_QUESTIONS.keys()), key="topic_selector")
    if st.button("Start"):
        st.session_state.topic = topic
        st.session_state.questions = TOPIC_QUESTIONS[topic]
        st.session_state.started = True
        st.rerun()
    st.stop()

# ✅ 显示答题历史
for entry in st.session_state.history:
    st.chat_message("assistant").markdown(entry["question"])
    if entry.get("image"):
        st.image(entry["image"], caption="Reference Image", use_container_width=True)
    st.chat_message("user").markdown(entry["user_answer"])

# ✅ 游戏进行中
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
        st.session_state.history.append({
            "question": q["question"],
            "user_answer": user_input,
            "image": q.get("image")
        })

        if user_input.strip() == q["answer"]:
            play_sound(CORRECT_SOUND)
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

# ✅ 已完成或失败后的重启选项
elif st.session_state.failed or st.session_state.completed:
    if st.button("Restart"):
        restart()
