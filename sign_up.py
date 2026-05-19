import hashlib
import pandas as pd
import streamlit as st

# טעינת הנתונים בצורה נכונה (מאלצים את ה-ID להיקרא כטקסט)
df = pd.read_csv('syn_data.csv', dtype={'ID': str})

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
    search_id = user_id_input.strip()

    # 1. בדיקה ראשונית של תקינות הקלט (9 ספרות)
    if search_id.isdigit() and len(search_id) == 9:

        # 2. בדיקה האם ה-ID בכלל קיים ב-CSV כדי למנוע קריסה בשורת ה-index[0]
        if search_id in df['ID'].values:

            # מציאת המיקום המדויק של המשתמש ב-CSV
            my_position = df[df['ID'] == search_id].index[0]

            # הצפנת הסיסמה שהמשתמש הקליד ב-SHA256
            hashed_input = hashlib.sha256(password_input.encode()).hexdigest()

            # שליפת הסיסמה המוצפנת השמורה ב-CSV (עמודה אינדקס 8 - Pass)
            saved_password = str(df.iloc[my_position, 8]).strip()

            # 3. בדיקה האם הסיסמאות תואמות
            if hashed_input == saved_password:
                st.session_state.user_id = search_id
                st.session_state.page = 'find'
                st.rerun()
            else:
                st.error("הסיסמה שהוזנה אינה נכונה")
        else:
            st.error("תעודת הזהות לא קיימת במערכת")
    else:
        st.error("חייב שיהיה 9 ספרות")