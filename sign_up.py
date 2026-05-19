import streamlit as st

st.markdown("<h1 style='text-align: center;'>Learny - Sign In</h1>", unsafe_allow_html=True)
st.write("##")

# טופס התחברות פשוט ונקי
with st.form("login_form"):
    user_id_input = st.text_input("Enter ID (9 digits):", max_chars=9)
    password_input = st.text_input("Enter Password:", type="password")

    # כפתור שליחה יחיד שתופס את מלוא רוחב הטופס
    login_submitted = st.form_submit_button("Sign In", use_container_width=True)

# לוגיקת בדיקת הנתונים והעברת הסיגנל לקובץ הראשי (start_page.py)
if login_submitted:
    if not user_id_input.isdigit() or len(user_id_input.strip()) < 9:
        st.error("Please enter a valid 9-digit ID.")
    elif not password_input:
        st.error("Please enter your password.")
    else:
        # שומר את ה-ID ומעביר ישירות למסך החיפוש בלי לבקש ת"ז שוב בשלב הבא
        st.session_state.user_id = user_id_input.strip()
        st.session_state.search_done = True
        st.session_state.page = 'find'
        st.rerun()