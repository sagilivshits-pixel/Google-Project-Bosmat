import streamlit as st
import pandas as pd
import json
import os

st.markdown(
    """
    <style>
        /* יישור התוכן לימין */
        div[data-testid="stSidebarUserContent"] {
            direction: rtl !important;
            text-align: right !important;
            padding-top: 1.5rem !important;
        }

        /* וידוא שהסיידבר נשאר מחובר לקיר הימני */
        section[data-testid="stSidebar"] {
            right: 0 !important;
            left: auto !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

with st.sidebar:
    st.title("תפריט מערכת")
    if st.button("🚪 התנתקות מהמערכת", use_container_width=True):
        st.session_state.search_done = False
        st.session_state.user_id = ""
        st.session_state.page = 'home'
        st.rerun()


# כאן ממשיך שאר הקוד המקורי שלך (לוגיקת הפגישות או החיפוש)
# --- 3. פונקציות טעינה ---
def load_json(filename):
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []


# --- 4. לוגיקה מרכזית עם עמודות למרכוז ---
# יצירת עמודות: צדדיות ריקות (1) ואמצעית רחבה (2)
spacer_right, center_col, spacer_left = st.columns([1, 2, 1])

with center_col:
    st.markdown("<h1 style='text-align: center;'>לוח הפגישות שלי</h1>", unsafe_allow_html=True)

    tutor_id = st.session_state.get('user_id', '')

    if not tutor_id:
        st.error("לא נמצא מזהה מורה. אנא התחבר מחדש.")
    else:
        df = pd.read_csv('syn_data.csv')
        appointments = load_json('appointments.json')

        tutor_row = df[df['ID'].astype(str).str.strip() == str(tutor_id).strip()]

        if tutor_row.empty:
            st.error("מורה לא נמצא במאגר.")
        else:
            tutor_name = tutor_row['Name'].iloc[0]
            st.markdown(f"<h3 style='text-align: center;'>שלום, {tutor_name}</h3>", unsafe_allow_html=True)
            st.write("")  # מרווח

            my_appointments = [
                app for app in appointments
                if str(app.get('tutor_name', '')).strip().lower() == str(tutor_name).strip().lower()
            ]

            if not my_appointments:
                st.info("אין לך פגישות קרובות במערכת כרגע.")
            else:
                for app in my_appointments:
                    student_id = str(app.get('student_id', '')).strip()
                    student_rows = df[df['ID'].astype(str).str.strip() == student_id]

                    if not student_rows.empty:
                        student_name = student_rows['Name'].iloc[0]
                        student_phone = student_rows['Phone number'].iloc[0]
                    else:
                        student_name = app.get('student_name', "תלמיד")
                        student_phone = app.get('phone', 'לא זמין')

                    # הצגה בתוך קופסה מעוצבת
                    with st.container():
                        st.success(
                            f"📅 **יום:** {app.get('day')}  |  ⏰ **שעה:** {app.get('hour')} \n\n"
                            f"👤 **שם התלמיד:** {student_name}  \n"
                            f"📱 **טלפון:** {student_phone}  \n"
                            f"📚 **מקצוע:** {app.get('subject', 'כללי')}"
                        )
                        st.markdown("---")