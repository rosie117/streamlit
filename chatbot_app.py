import streamlit as st
import streamlit.components.v1 as components
import base64
import time

st.set_page_config(page_title="Quiz Challenge", layout="centered")

# ✅ 自动播放本地 mp3 音效
def play_sound_local(filepath: str):
    with open(filepath, "rb") as f:
        audio_base64 = base64.b64encode(f.read()).decode()
    audio_tag = f"""
        <audio autoplay>
            <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
        </audio>
    """
    components.html(audio_tag, height=0, width=0)

# ✅ 题库设置
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
        {"question": "🧩 Q4: Which two tracks are typically offered in CUHK’s MSc in Marketing program?", "options": ["Big Data Marketing / Managerial Marketing", "FinTech and Blockchain", "Public Health / Biotech Management", "Brand & Advertising / Customer Analytics"], "answer": "Brand & Advertising / Customer Analytics"},
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

# ✅ 欢迎界面
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

# ✅ 展示历史记录
for entry in st.session_state.history:
    st.chat_message("assistant").markdown(entry["question"])
    if entry.get("image"):
        st.image(entry["image"], caption="Reference Image", use_container_width=True)
    st.chat_message("user").markdown(entry["user_answer"])

# ✅ 游戏进行中
if not st.session_state.failed and not st.session_state.completed:
    curr = st.session_state.step

    # ✅ 防止越界访问
    if curr >= len(st.session_state.questions):
        st.session_state.completed = True
        st.rerun()

    q = st.session_state.questions[curr]

    with st.chat_message("assistant"):
        st.markdown(q["question"])
        if q.get("image"):
            st.image(q["image"], caption="Reference Image", use_container_width=True)

    # 选择题
    if "options" in q:
        selected_option = st.radio("Choose your answer:", q["options"], key=f"q_{curr}")
        if st.button("Submit Answer", key=f"submit_{curr}"):
            st.session_state.history.append({
                "question": q["question"],
                "user_answer": selected_option,
                "image": q.get("image")
            })
            if selected_option == q["answer"]:
                play_sound_local("success.mp3")
                time.sleep(0.8)
                st.session_state.step += 1
                st.rerun()
            else:
                play_sound_local("fail.mp3")
                st.session_state.failed = True
                st.chat_message("assistant").error("❌ Incorrect answer. Game over.")
                st.chat_message("assistant").button("Restart", on_click=restart)
    else:
        # 填空题
        user_input = st.chat_input("Your answer:")
        if user_input:
            st.session_state.history.append({
                "question": q["question"],
                "user_answer": user_input,
                "image": q.get("image")
            })
            if user_input.strip() == q["answer"]:
                play_sound_local("success.mp3")
                time.sleep(0.8)
                st.session_state.step += 1
                st.rerun()
            else:
                play_sound_local("fail.mp3")
                st.session_state.failed = True
                st.chat_message("assistant").error("❌ Incorrect answer. Game over.")
                st.chat_message("assistant").button("Restart", on_click=restart)

# ✅ 通关或失败
if st.session_state.completed:
    play_sound_local("success-trumpets.mp3")
    st.balloons()
    st.chat_message("assistant").success("🎉 Congratulations! You completed the challenge!")
    st.chat_message("assistant").button("Restart", on_click=restart)

elif st.session_state.failed:
    # 音效已播放，显示按钮
    pass
