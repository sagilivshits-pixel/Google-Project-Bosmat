import streamlit as st
import pandas as pd
import json
import os

# --- 1. הזרקת ה-CSS הפנימי לשמירה על עיצוב אחיד (RTL - ימין לשמאל) ---
st.markdown(
    """
    <style>
        section[data-testid="stSidebar"] {
            left: auto !important;
            right: 0 !important;
            width: 300px !important;
            min-width: 300px !important;
            max-width: 300px !important;
            z-index: 99999 !important;
            transition: transform 0.3s ease, width 0.3s ease, min-width 0.3s ease !important;
        }
        div[data-testid="stSidebarUserContent"] {
            padding-top: 1rem !important;
            direction: rtl !important;
            text-align: right !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# --- 2. תפריט צד (Sidebar) ימני למורה ---
with st.sidebar:
    st.title("תפריט מורה")
    st.markdown("---")

    # כפתור התנתקות
    if st.button("🚪 התנתקות מהמערכת", use_container_width=True):
        st.session_state.user_id = ""
        st.session_state.page = 'home'
        st.rerun()

# --- 3. לוגיקה ותוכן מרכזי ---
# שמירה על עמודות כדי למרכז את התוכן במסך
spacer_right, center_col, spacer_left = st.columns([1, 2, 1])

with center_col:
    st.markdown("<h1 style='text-align: center; margin-bottom: 2rem;'>לוח הפגישות שלי</h1>", unsafe_allow_html=True)

    # בדיקה שיש לנו משתמש מחובר
    tutor_id = st.session_state.get('user_id', '')

    if not tutor_id:
        st.error("לא נמצא מזהה משתמש מחובר. אנא התחבר מחדש.")
    else:
        # א. טעינת בסיס הנתונים (CSV)
        df = pd.read_csv('syn_data.csv', dtype={'ID': str})

        # ב. מציאת שם המורה המחובר
        tutor_info = df[df['ID'] == str(tutor_id)]

        if tutor_info.empty:
            st.error("פרטי המורה לא נמצאו במאגר.")
        else:
            tutor_name = tutor_info['Name'].iloc[0]
            st.subheader(f"שלום {tutor_name}, הנה הפגישות שנקבעו איתך:")
            st.write("---")

            # ג. טעינת הפגישות (JSON)
            appointments = []
            if os.path.exists('appointments.json'):
                with open('appointments.json', 'r', encoding='utf-8') as f:
                    appointments = json.load(f)

            # ד. סינון הפגישות ששייכות רק למורה הזה (משווים אותיות קטנות למניעת באגים)
            my_appointments = [
                app for app in appointments
                if str(app.get('tutor_name', '')).strip().lower() == str(tutor_name).strip().lower()
            ]

            # ה. הצגת הנתונים
            if not my_appointments:
                st.info("אין לך פגישות קרובות במערכת כרגע.")
            else:
                for app in my_appointments:
                    student_id = str(app.get('student_id', ''))

                    # הצלבת מידע עם ה-CSV כדי למצוא את השם האמיתי של התלמיד
                    student_rows = df[df['ID'] == student_id]
                    if not student_rows.empty:
                        student_name = student_rows['Name'].iloc[0]
                        # עדיף לקחת טלפון עדכני מהמסד נתונים, אבל אם אין, ניקח ממה שנשמר בפגישה
                        student_phone = student_rows['Phone number'].iloc[0]
                    else:
                        student_name = "תלמיד לא נמצא במאגר"
                        student_phone = app.get('phone', 'לא זמין')

                    # יצירת כרטיסייה מעוצבת לכל פגישה
                    st.success(
                        f"📅 **יום:** {app.get('day')}  |  ⏰ **שעה:** {app.get('hour')} \n\n"
                        f"👤 **שם התלמיד:** {student_name} \n\n"
                        f"📚 **מקצוע:** {app.get('subject')} \n\n"
                        f"📞 **טלפון התלמיד:** {student_phone}"
                    )