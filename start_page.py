import streamlit as st
import base64
import os

# 1. Page Configuration
st.set_page_config(page_title="Learny", layout="wide")


# פונקציית עזר להמרת תמונה ל-base64
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return ""


# טעינת תמונת הרקע (PNG)
img_base64 = get_base64_image("wave_bg.png")

# 2. הזרקת CSS מותאם אישית
# משתמשים ב-background-size: cover כדי למנוע מתיחה של התמונה
bg_style = ""
if img_base64:
    bg_style = f"""
    <style>
        .stApp {{
            background-image: url("data:image/png;base64,{img_base64}");
            background-size: cover !important;
            background-position: center !important;
            background-repeat: no-repeat !important;
            background-attachment: fixed !important;
        }}
    </style>
    """
st.markdown(bg_style, unsafe_allow_html=True)

# עיצוב כללי (RTL והסתרת Sidebar)
st.markdown(
    """
    <style>
        html, body, [data-testid="stAppViewContainer"] {
            direction: rtl;
            text-align: right;
        }
        /* הסתרת ה-Sidebar */
        [data-testid="stSidebar"] { display: none; }
        [data-testid="collapsedControl"] { display: none; }

        /* עיצוב כפתורים */
        .stButton > button {
            width: 100%;
            border-radius: 20px;
        }
        /* כותרות */
        h1 { color: #1E3A2F; text-align: center; }
    </style>
    """,
    unsafe_allow_html=True
)

# 3. ניהול ניווט (Session State)
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# 4. לוגיקת דפים
main_container = st.container()

with main_container:
    if st.session_state.page == 'home':
        st.write("##")
        st.write("##")

        # עמודה ימנית לכפתורים, עמודה שמאלית לתמונה
        col_right, col_left = st.columns([1, 1], gap="large")

        with col_right:
            st.markdown("<h1>ברוכים הבאים ל-Learny</h1>", unsafe_allow_html=True)
            st.write("##")

            if st.button("Sign In", use_container_width=True):
                st.session_state.page = 'login'
                st.rerun()

            st.write("###")  # מרווח

            if st.button("Register", use_container_width=True):
                st.session_state.page = 'input'
                st.rerun()

        with col_left:
            # טעינת תמונת הקולאז' (PNG)
            if os.path.exists("Untitled design.png"):
                st.image("Untitled design.png", use_container_width=True)
            else:
                st.warning("התמונה 'Untitled design.png' לא נמצאה.")

    # ניתוב לדפים האחרים
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