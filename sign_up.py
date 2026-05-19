import streamlit as st
import pandas as pd
dataf = pd.read_csv('syn_data.csv')
CSV_PATH = "syn_data.csv"
st.markdown("<h1 style='text-align: center;'>Learny - Sign In</h1>", unsafe_allow_html=True)
st.write("##")

# טופס התחברות
with st.form("login_form"):
    user_id_input = st.text_input("Enter ID (9 digits):", max_chars=9)
    password_input = st.text_input("Enter Password :", type="password")

    # כפתור התחברות
    login_submitted = st.form_submit_button("Sign In", use_container_width=True)
# ברגע שלוחצים על Sign In
if login_submitted:
    # בדיקת התנאי: האם הקלט מכיל רק ספרות והאורך שלו הוא בדיוק 9 ספרות
    if user_id_input.isdigit() and len(user_id_input.strip()) == 9 :
        # אם התנאי מתקיים (נכון) - מעביר אותך ישירות לסטרימליט פינד
        st.session_state.page = 'find'
        st.rerun()
    else:
        # אם התנאי לא מתקיים (לא נכון) - מציג הודעה שחייב 9 ספרות ולא מחבר
        st.error("חייב שיהיה 9 ספרות")