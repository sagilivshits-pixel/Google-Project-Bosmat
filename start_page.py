import streamlit as st

# הגדרות דף - מבטיח רקע לבן ונקי
st.set_page_config(page_title="Learny", layout="centered")

# כותרת פשוטה בטקסט שחור (בלי סמלים)
st.markdown("<h1 style='text-align: center; color: black;'>Learny</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: black;'>Welcome. Please choose an option:</p>", unsafe_allow_html=True)

# יצירת מרווח
st.write("##")

# יצירת שני טורים לכפתורים
col1, col2 = st.columns(2)

with col1:
    if st.button("Sign In", use_container_width=True):
        st.session_state.page = 'find'
        st.write("Redirecting to Sign In...")
        # כאן תבוא הפקודה להריץ את streamlit_find.py

with col2:
    if st.button("Register", use_container_width=True):
        st.session_state.page = 'input'
        st.write("Redirecting to Register...")
        # כאן תבוא הפקודה להריץ את Get_user_input.py