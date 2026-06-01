import hashlib
import pandas as pd
import streamlit as st
import os

# טעינת הנתונים בצורה נכונה
if os.path.exists('syn_data.csv'):
    df = pd.read_csv('syn_data.csv', dtype={'ID': str})
else:
    df = pd.DataFrame(
        columns=['Pass', 'ID', 'Name', 'Tutor / Student', 'Subject', 'Online / F2F', 'Day', 'Hour', 'Phone number'])

# ── הזרקת CSS חסין - עיצוב הקופסה הלבנה ─────────────────────────────────
st.markdown(
    """
    <style>
        /* עיצוב ישיר של הטופס כקופסה לבנה ואטומה לחלוטין */
        div[data-testid="stForm"] {
            background-color: #FFFFFF !important;
            background: #FFFFFF !important;
            opacity: 1 !important;
            padding: 2.5rem !important;
            border-radius: 16px !important;
            box-shadow: 0px 12px 35px rgba(0,0,0,0.15) !important;
            border: 1px solid #EAEAEA !important;
            margin-top: -30px !important; /* מרים את הקופסה בצורה מעודנת למעלה */
        }

        /* ביטול גבולות כפולים פנימיים */
        div[data-testid="stVerticalBlockBorderWrapper"] {
            background-color: transparent !important;
            background: transparent !important;
            border: none !important;
            padding: 0 !important;
        }

        /* וידוא שכל הטקסטים ותוויות הקלט בתוך הקופסה כהים וקריאים */
        div[data-testid="stForm"] input, 
        div[data-testid="stForm"] label,
        div[data-testid="stForm"] p,
        div[data-testid="stForm"] span,
        div[data-testid="stForm"] h1 {
            color: #262730 !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# יצירת עמודות למרכוז הטופס על המסך
_, center_col, _ = st.columns([1, 1.6, 1])

with center_col:
    # טופס ההתחברות (הקופסה הלבנה)
    with st.form("login_form"):
        # הכותרת בתוך הקופסה למראה מעוצב ונקי
        st.markdown("<h1 style='text-align: center; font-size: 2.2rem; margin-bottom: 1.5rem;'>Learny - התחברות</h1>",
                    unsafe_allow_html=True)

        user_id_input = st.text_input("תעודת זהות (9 ספרות):", max_chars=9)
        password_input = st.text_input("סיסמה:", type="password")

        # הזרקת מרווח קטן ומבוקר במקום ה-st.write("##") הגדול שהיה קודם לכן
        st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)

        # כפתור התחברות
        login_submitted = st.form_submit_button("התחברות", use_container_width=True)

    # לוגיקת בדיקת הפרטים לאחר לחיצה
    if login_submitted:
        search_id = user_id_input.strip()

        # 1. בדיקת תקינות הקלט
        if search_id.isdigit() and len(search_id) == 9:

            # 2. בדיקה האם ה-ID קיים במערכת
            if search_id in df['ID'].values:
                user_row = df[df['ID'] == search_id].iloc[0]

                # הצפנת הסיסמה והשוואה
                hashed_input = hashlib.sha256(password_input.encode()).hexdigest()
                saved_password = str(user_row['Pass']).strip()

                # 3. בדיקה האם הסיסמאות תואמות
                if hashed_input == saved_password:
                    role = str(user_row['Tutor / Student']).strip()
                    st.session_state.user_id = search_id

                    # ניתוב דפים
                    if role == "Student":
                        st.session_state.page = 'find'
                    else:
                        st.session_state.page = 'Tutor_page'
                    st.rerun()
                else:
                    st.error("הסיסמה שהוזנה אינה נכונה. אנא נסה שנית.")
            else:
                st.error("תעודת הזהות אינה קיימת במערכת. אנא הרשם תחילה.")
        else:
            st.error("תעודת הזהות חייבת להכיל בדיוק 9 ספרות.")