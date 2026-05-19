import streamlit as st

# הגדרות דף - לבן ונקי כפי שקבעת, העברנו ל-wide כדי לתמוך בתוצאות בצורה יפה
st.set_page_config(page_title="Learny", layout="wide")

# 🔥 הזרקת ה-CSS של המינימייז לקובץ האם כדי שהמסך יתמרכז בצורה מושלמת כשהסיידבר נסגר
st.markdown(
    """
    <style>
        html, body, [data-testid="stAppViewContainer"] {
            direction: rtl;
            text-align: right;
        }
        /* תיקון למינימייז: כשהסיידבר סגור, מאפסים לו את הרוחב כדי שהתוכן יתמרכז */
        section[data-testid="stSidebar"][aria-expanded="false"] {
            width: 0px !important;
            min-width: 0px !important;
            max-width: 0px !important;
            transform: translateX(300px) !important;
        }
        div[data-testid="collapsedControl"] {
            left: auto !important;
            right: 20px !important;
            top: 15px !important;
            z-index: 999999 !important;
        }
        div[data-testid="stSidebarHeader"] {
            direction: ltr !important; 
        }
        div[data-testid="collapsedControl"] svg,
        div[data-testid="stSidebarHeader"] svg {
            transform: rotate(180deg) !important;
        }
        div[data-testid="stMain"] {
            margin-left: 0 !important;
            margin-right: 0 !important;
            transition: margin 0.3s ease !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# ניהול מצב הדפים (הסיגנל)
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# --- דף הבית ---
if st.session_state.page == 'home':
    st.markdown("<h1 style='text-align: center;'>Learny</h1>", unsafe_allow_html=True)
    st.write("##")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Sign In", use_container_width=True):
            st.session_state.page = 'find'
            st.rerun()

    with col2:
        if st.button("Register", use_container_width=True):
            st.session_state.page = 'input'
            st.rerun()

# --- הרצת הקבצים האחרים (בלי לשנות אותם) ---

elif st.session_state.page == 'find':
    # מריץ את הקובץ streamlit_find.py כפי שהוא
    with open("streamlit_find.py", encoding="utf-8") as f:
        code = f.read()
        exec(code)

elif st.session_state.page == 'input':
    if st.button("⬅ Back to Menu"):
        st.session_state.page = 'home'
        st.rerun()

    # מריץ את הקובץ Get_user_input.py כפי שהוא
    with open("Get_user_input.py", encoding="utf-8") as f:
        code = f.read()
        exec(code)