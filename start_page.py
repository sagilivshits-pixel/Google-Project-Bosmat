import streamlit as st

# הגדרות דף - לבן ונקי
st.set_page_config(page_title="Learny", layout="centered")

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
    if st.button("⬅ Back to Menu"):
        st.session_state.page = 'home'
        st.rerun()

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