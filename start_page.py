import streamlit as st
import base64
import os

# 1. Page Configuration
st.set_page_config(page_title="Learny", layout="wide")


def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return ""


img_base64 = get_base64_image("wave_bg.png")

# 2. הזרקת CSS מותאם אישית - דגש על שכבות ואיכות
if img_base64:
    st.markdown(
        f"""
        <style>
            .stApp {{
                background-image: url("data:image/png;base64,{img_base64}");
                /* פתרון האיכות: במקום cover, נשתמש ב-100% לרוחב וגובה אוטומטי */
                background-size: 100% auto !important;
                background-position: bottom center !important;
                background-repeat: no-repeat !important;
                background-attachment: fixed !important;
                /* מוודא שהרקע תמיד מאחורי הכל */
                z-index: -1;
            }}

            html, body, [data-testid="stAppViewContainer"] {{
                direction: rtl;
                text-align: right;
            }}

            /* עיצוב כפתורים */
            .stButton > button {{
                width: 100%;
                border-radius: 20px;
            }}
            h1 {{ color: #1E3A2F; text-align: center; }}
        </style>
        """,
        unsafe_allow_html=True
    )

# לוגיקה להסתרה/הצגה של הסיידבר לפי דף
if 'page' not in st.session_state:
    st.session_state.page = 'home'

if st.session_state.page == 'home':
    st.markdown("<style>[data-testid='stSidebar'], [data-testid='collapsedControl'] {display: none;}</style>",
                unsafe_allow_html=True)
else:
    # כאן אנחנו "מכריחים" את הסיידבר להופיע בדפים אחרים עם Z-index גבוה
    st.markdown("<style>[data-testid='stSidebar'] {display: flex !important; z-index: 1000001 !important;}</style>",
                unsafe_allow_html=True)

# 4. לוגיקת דפים (ללא שינוי במבנה המקורי שלך)
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