import streamlit as st
import base64
import os

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
        /* תיקון למינימייז: כשהסיידבר סגור, מאפסים לו את הרוחב כדי שהתוכן יתמרכז */
        section[data-testid="stSidebar"][aria-expanded="false"] {{
            width: 0px !important;
            min-width: 0px !important;
            max-width: 0px !important;
            transform: translateX(300px) !important;
        }}
        div[data-testid="collapsedControl"] {{
            left: auto !important;
            right: 20px !important;
            top: 15px !important;
            z-index: 999999 !important;
        }}
        div[data-testid="stSidebarHeader"] {{
            direction: ltr !important; 
        }}
        div[data-testid="collapsedControl"] svg,
        div[data-testid="stSidebarHeader"] svg {{
            transform: rotate(180deg) !important;
        }}
        /* --------------------------------------------------- */
    </style>
    """,
    unsafe_allow_html=True
)

# הסתרת הסיידבר במסך הבית בלבד
if 'page' not in st.session_state:
    st.session_state.page = 'home'

if st.session_state.page == 'home':
    st.markdown(
        "<style>[data-testid='stSidebar'], [data-testid='collapsedControl'] {display: none !important;}</style>",
        unsafe_allow_html=True)

# --- מכאן והלאה: הלוגיקה והכפתורים המקוריים שלך ללא שום שינוי ---
main_container = st.container()
with main_container:
    if st.session_state.page == 'home':
        st.write("##")
        st.write("##")
        col_right, col_left = st.columns([1, 1], gap="large")
        with col_right:
            st.markdown("<h1>ברוכים הבאים ל-Learny</h1>", unsafe_allow_html=True)
            st.write("##")
            if st.button("Sign In", use_container_width=True):
                st.session_state.page = 'login'
                st.rerun()
            st.write("###")
            if st.button("Register", use_container_width=True):
                st.session_state.page = 'input'
                st.rerun()
        with col_left:
            if os.path.exists("Untitled design.png"):
                st.image("Untitled design.png", use_container_width=True)

    elif st.session_state.page == 'login':
        if st.button("⬅ חזרה לתפריט"):
            st.session_state.page = 'home'
            st.rerun()
        with open("sign_up.py", encoding="utf-8") as f:
            exec(f.read())
    elif st.session_state.page == 'input':
        if st.button("⬅ חזרה לתפריט"):
            st.session_state.page = 'home'
            st.rerun()
        with open("Get_user_input.py", encoding="utf-8") as f:
            exec(f.read())
    elif st.session_state.page == 'find':
        with open("streamlit_find.py", encoding="utf-8") as f:
            exec(f.read())
    elif st.session_state.page == 'Tutor_page':
        with open("Tutor_page.py", encoding="utf-8") as f:
            exec(f.read())