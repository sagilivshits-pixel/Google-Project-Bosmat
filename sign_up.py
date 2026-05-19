import streamlit as st

st.markdown("<h1 style='text-align: center;'>Learny - Sign In</h1>", unsafe_allow_html=True)
st.write("##")

# טופס התחברות פשוט במרכז
with st.form("login_form"):
    user_id_input = st.text_input("Enter ID (9 digits):", max_chars=9)
    password_input = st.text_input("Enter Password:", type="password")

    # כפתור התחברות יחיד (ללא כפתור הרשמה)
    login_submitted = st.form_submit_button("Sign In", use_container_width=True)

# ברגע שלוחצים על Sign In - בודקים נתונים ומעבירים לקובץ החיפוש
if login_submitted:
    if not user_id_input.isdigit() or len(user_id_input.strip()) < 9:
        st.error("Please enter a valid 9-digit ID.")
    elif not password_input:
        st.error("Please enter your password.")
    else:
        # 1. שומר את ה-ID שהוזן כדי שקובץ החיפוש יקרא אותו אוטומטית
        st.session_state.user_id = user_id_input.strip()
        st.session_state.search_done = True

        # 2. משנה את הסיגנל ל-'find' כדי שקובץ האם יטען את streamlit_find.py
        st.session_state.page = 'find'
        st.rerun()