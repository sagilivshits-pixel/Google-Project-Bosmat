import streamlit as st
import base64
import os
from Get_user_input import *
from streamlit_find import *

# 1. הגדרות דף - חובה Layout Wide
st.set_page_config(page_title="Learny", layout="wide")


def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return ""


# טעינת התמונות (משתמש בקובץ הקיים שלך לקולאז')
img_base64 = get_base64_image("wave_bg.png")
collage_base64 = get_base64_image("Untitled design.png")

# יצירת ה-CSS של הרקע הכללי (הגלים)
bg_css = ""
if img_base64:
    bg_css = f"""
    .stApp {{
        background-image: url("data:image/png;base64,{img_base64}");
        background-size: 100% auto !important;
        background-position: bottom center !important;
        background-repeat: no-repeat !important;
        background-attachment: fixed !important;
        z-index: -1;
    }}
    """

# הזרקת ה-CSS הגלובלי (החזרת הסיידבר והעלמת הקו העליון בצורה חכמה)
st.markdown(
    f"""
    <style>
        {bg_css}

        /* כיווניות מימין לשמאל */
        html, body, [data-testid="stAppViewContainer"] {{
            direction: rtl;
            text-align: right;
        }}

        /* פתרון הקו למעלה: מעלים רק את הפס הצבעוני, הופכים את ה-Header לשקוף כדי שהסיידבר ייראה! */
        [data-testid="stDecoration"] {{
            display: none !important;
        }}
        header {{
            background-color: transparent !important;
        }}

        /* ------------- הקוד המקורי והעובד שלך לסיידבר ------------- */
        section[data-testid="stSidebar"][aria-expanded="false"] {{
            width: 0px !important;
            min-width: 0px !important;
            max-width: 0px !important;
            transform: translateX(300px) !important;
        }}
        /* מיקום כפתור הפתיחה של הסיידבר בצד ימין למעלה */
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

# אתחול ה-page במידה ולא קיים
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# ניהול המסכים והתוכן המרכזי
main_container = st.container()
with main_container:
    if st.session_state.page == 'home':

        # הזרקת העיצוב המיוחד של מסך הבית (מיקום הקולאז' משמאל)
        st.markdown(f"""
        <style>
            /* מיקום התוכן בצד ימין */
            .block-container {{
                max-width: 100% !important;
                padding-top: 22vh !important; 
                z-index: 1;
            }}

            /* תמונת קולאז' משמאל - נצמדת ל-0 מוחלט מלמעלה ומשמאל ותופסת חצי מסך מלא */
            .left-bg {{
                position: fixed;
                top: 0 !important; 
                left: 0 !important;
                width: 50vw !important; 
                height: 100vh !important;
                background-image: url("data:image/png;base64,{collage_base64}");
                background-size: cover !important;
                background-position: center !important;
                z-index: 0;
                pointer-events: none;
            }}
        </style>
        <div class="left-bg"></div>
        """, unsafe_allow_html=True)

        # שימוש בטריק 4 העמודות שלך [1, 4, 1, 6]
        col_right_spacer, col_content, col_mid_spacer, col_left_empty = st.columns([1, 4, 1, 6])

        with col_content:
            st.markdown(
                "<h1 style='text-align: center; color: #1E3A2F; margin-bottom: 40px; font-size: 3.5rem;'>ברוכים הבאים ל-Learny</h1>",
                unsafe_allow_html=True
            )

            # כפתורי סטרימליט מקוריים ורגילים לחלוטין
            if st.button("Sign In", use_container_width=True):
                st.session_state.page = 'login'
                st.rerun()

            st.write("##")  # מרווח בין כפתורים

            if st.button("Register", use_container_width=True):
                st.session_state.page = 'input'
                st.rerun()

    # שאר דפי המערכת המקוריים שלך
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
            get_user_input()

    elif st.session_state.page == 'find':
        with open("streamlit_find.py", encoding="utf-8") as f:
            exec(f.read())

    elif st.session_state.page == 'Tutor_page':
        with open("Tutor_page.py", encoding="utf-8") as f:
            exec(f.read())