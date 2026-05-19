import streamlit as st

st.markdown("<h1 style='text-align: center;'>Learny - Sign In</h1>", unsafe_allow_html=True)
st.write("##")

# טופס התחברות
with st.form("login_form"):
    user_id_input = st.text_input("Enter ID (9 digits):", max_chars=9)
    # תיבת הסיסמה חזרה כאן (מוגדרת כסודית עם כוכביות)
    password_input = st.text_input("Enter Password (Optional):", type="password")

    # כפתור התחברות
    login_submitted = st.form_submit_button("Sign In", use_container_width=True)

# ברגע שלוחצים על Sign In - בודקים רק את תעודת הזהות (הסיסמה אופציונלית)
if login_submitted:
    if not user_id_input.isdigit() or len(user_id_input.strip()) < 9:
        st.error("Please enter a valid 9-digit ID.")
    else:
        # 1. שומר את ה-ID שהוזן כדי שקובץ החיפוש יקרא אותו אוטומטית מיד
        st.session_state.user_id = user_id_input.strip()
        st.session_state.search_done = True

        # 2. משנה את הסיגנל ל-'find' כדי שקובץ האם (start_page) יטען את streamlit_find.py
        st.session_state.page = 'find'
        st.rerun()