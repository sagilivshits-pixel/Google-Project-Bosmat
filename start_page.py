import streamlit as st
import base64
import os
from Get_user_input import *
from streamlit_find import *

# הגדרות דף - שומר על ה-Layout הרקע והגדרת ה-wide המקורית שלך
st.set_page_config(page_title="Learny", layout="wide")


def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return ""


img_base64 = get_base64_image("wave_bg.png")

# יצירת ה-CSS של הרקע בנפרד כדי לא לגעת בקוד שלך
bg_css = ""
if img_base64:
    bg_css = f"""
    .stApp {{
        background-image: url("data:image/png;base64,{img_base64}");
        /* מונע זום ושומר את התמונה למטה */
        background-size: 100% auto !important;
        background-position: bottom center !important;
        background-repeat: no-repeat !important;
        background-attachment: fixed !important;
        z-index: -1;
    }}
    """

# הזרקת ה-CSS המקורי שלך שעבד מושלם + הרקע!
st.markdown(
    f"""
    <style>
        {bg_css}

        /* ------------- הקוד המקורי והעובד שלך ------------- */
        html, body, [data-testid="stAppViewContainer"] {{
            direction: rtl;
            text-align: right;
        }}
        h1, h2, h3, p, label, .stMarkdown {{
            color: #262730 !important;
            direction: rtl;
            text-align: right;
        }}
        div[data-testid="stForm"] {{
            direction: rtl;
            text-align: right;
        }}
    </style>
    """,
    unsafe_allow_html=True
)

# אתחול ה-session_state במידה ולא קיים
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'user_id' not in st.session_state:
    st.session_state.user_id = ""

# מיכל ראשי לעיטוף האפליקציה
main_container = st.container()
with main_container:
    # --- מסך הבית הראשי ---
    if st.session_state.page == 'home':
        st.write("##")
        st.write("##")
        col_right, col_left = st.columns([1, 1], gap="large")
        with col_right:
            st.markdown("<h1>ברוכים הבאים ל-Learny</h1>", unsafe_allow_html=True)
            st.write("##")
            # תרגום כפתור ההתחברות לעברית
            if st.button("התחברות", use_container_width=True):
                st.session_state.page = 'login'
                st.rerun()
            st.write("###")
            # תרגום כפתור ההרשמה לעברית
            if st.button("הרשמה למערכת", use_container_width=True):
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
        if st.session_state.user_id:
            streamlit_find(st.session_state.user_id)
        else:
            st.error("שגיאה: לא נמצא מזהה משתמש. אנא התחבר מחדש.")
            if st.button("חזרה למסך הבית"):
                st.session_state.page = 'home'
                st.rerun()

    # --- מסך אזור אישי למורים ---
    elif st.session_state.page == 'Tutor_page':
        if st.session_state.user_id:
            with open("Tutor_page.py", encoding="utf-8") as f:
                exec(f.read())
        else:
            st.error("שגיאה: לא נמצא מזהה משתמש. אנא התחבר מחדש.")
            if st.button("חזרה למסך הבית"):
                st.session_state.page = 'home'
                st.rerun()