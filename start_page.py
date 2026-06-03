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


# טעינת התמונות
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

# הזרקת ה-CSS הגלובלי
st.markdown(
    f"""
    <style>
        {bg_css}

        /* כיווניות מימין לשמאל */
        html, body, [data-testid="stAppViewContainer"] {{
            direction: rtl;
            text-align: right;
        }}

        /* העלמת הפס הצבעוני העליון והפיכת ה-Header לשקוף */
        [data-testid="stDecoration"] {{
            display: none !important;
        }}
        header {{
            background-color: transparent !important;
        }}

        /* ------------- קוד הסיידבר ------------- */
        section[data-testid="stSidebar"][aria-expanded="false"] {{
            width: 0px !important;
            min-width: 0px !important;
            max-width: 0px !important;
            transform: translateX(300px) !important;
        }}

        div[data-testid="collapsedControl"] {{
            position: fixed !important;
            left: auto !important;
            right: 20px !important;
            top: 15px !important;
            z-index: 999999 !important;
            pointer-events: auto !important;
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

        # הזרקת העיצוב המיוחד של מסך הבית
        st.markdown(f"""
        <style>
            /* מיקום אנכי של התוכן */
            .block-container {{
                max-width: 100% !important;
                padding-top: 18vh !important; 
                z-index: 1;
            }}

            /* תמונת קולאז' משמאל - תופסת חצי מסך מלא */
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

            /* עיצוב פרימיום לכפתורים - משפיע אך ורק על עמוד הבית */
            div.stButton > button {{
                background-color: #1E3A2F !important;
                color: white !important;
                border-radius: 12px !important;
                padding: 14px 20px !important;
                font-size: 1.3rem !important;
                font-weight: bold !important;
                border: none !important;
                box-shadow: 0 4px 15px rgba(30, 58, 47, 0.2) !important;
                transition: all 0.25s ease-in-out !important;
                height: auto !important;
            }}

            /* אפקט ריחוף (Hover) אינטראקטיבי */
            div.stButton > button:hover {{
                background-color: #2d5a49 !important;
                box-shadow: 0 6px 22px rgba(30, 58, 47, 0.3) !important;
                transform: translateY(-2px) !important;
            }}

            div.stButton > button:active {{
                transform: translateY(0px) !important;
            }}
        </style>
        <div class="left-bg"></div>
        """, unsafe_allow_html=True)

        # חלוקה ראשית של המסך - חצי ימין לתוכן, חצי שמאל לקולאז'
        col_right_half, col_left_half = st.columns([1, 1])

        with col_right_half:
            col_spacer_right, col_main_content, col_spacer_left = st.columns([0.5, 2.5, 1.0])

            with col_main_content:
                st.markdown(
                    "<h1 style='text-align: center; color: #1E3A2F; margin-bottom: 45px; font-size: 3.6rem; font-weight: bold;'>ברוכים הבאים ל-Learny</h1>",
                    unsafe_allow_html=True
                )

                # כפתורי המערכת - תורגמו לעברית!
                if st.button("התחברות", use_container_width=True):
                    st.session_state.page = 'login'
                    st.rerun()

                st.write("##")  # מרווח אחיד

                if st.button("הרשמה למערכת", use_container_width=True):
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