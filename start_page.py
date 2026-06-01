import streamlit as st
import base64
import os
from Get_user_input import *
from streamlit_find import *
# הגדרות עמוד כלליות
st.set_page_config(page_title="Learny", layout="wide")


def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return ""


img_base64 = get_base64_image("wave_bg.png")

# ── CSS כללי לעמוד הבית ולרקע ───────────────────────────────────────
st.markdown(
    f"""
    <style>
        /* הגדרת רקע הגלים */
        .stApp {{
            background-image: url("data:image/png;base64,{img_base64}");
            background-size: 100% auto !important;
            background-position: bottom center !important;
            background-repeat: no-repeat !important;
            background-attachment: fixed !important;
        }}

        /* תיקון צבע טקסט כללי כדי שיהיה קריא */
        h1, h2, h3, p, label, .stMarkdown {{
            color: #262730 !important;
        }}

        /* יישור לימין (RTL) */
        html, body, [data-testid="stAppViewContainer"] {{
            direction: rtl;
            text-align: right;
        }}
    </style>
    """,
    unsafe_allow_html=True
)

# ── ניהול מצב (Session State) ────────────────────────────────────────
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'user_id' not in st.session_state:
    st.session_state.user_id = ""

# ── ניתוב עמודים ─────────────────────────────────────────────────────
main_container = st.container()
with main_container:
    # --- מסך בית ---
    if st.session_state.page == 'home':
        col_right, col_left = st.columns([1, 1], gap="large")
        with col_right:
            st.markdown("<h1>ברוכים הבאים ל-Learny</h1>", unsafe_allow_html=True)
            if st.button("Sign In", use_container_width=True):
                st.session_state.page = 'login'
                st.rerun()
            if st.button("Register", use_container_width=True):
                st.session_state.page = 'input'
                st.rerun()
        with col_left:
            if os.path.exists("Untitled design.png"):
                st.image("Untitled design.png", use_container_width=True)

    # --- מסך הרשמה ---
    elif st.session_state.page == 'input':
        if st.button("⬅ חזרה לתפריט"):
            st.session_state.page = 'home'
            st.rerun()
        get_user_input()

    # --- מסך התחברות ---
    elif st.session_state.page == 'login':
        if st.button("⬅ חזרה לתפריט"):
            st.session_state.page = 'home'
            st.rerun()
        with open("sign_up.py", encoding="utf-8") as f:
            exec(f.read())

    # --- מסך חיפוש לתלמידים ---
    elif st.session_state.page == 'find':
        if st.button("⬅ חזרה לתפריט"):
            st.session_state.page = 'home'
            st.rerun()

        # ייבוא הפונקציה מהקובץ השני
        from streamlit_find import streamlit_find

        # הפעלת הפונקציה והעברת ה-ID של המשתמש המחובר
        streamlit_find(st.session_state.user_id)

    # --- מסך אזור אישי למורים ---
    elif st.session_state.page == 'Tutor_page':
        st.title("ברוך הבא למסך המורה!")
        st.info(f"מחובר כמורה עם תעודת זהות: {st.session_state.user_id}")
        if st.button("🚪 התנתקות", use_container_width=False):
            st.session_state.user_id = ""
            st.session_state.page = 'home'
            st.rerun()