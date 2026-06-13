import streamlit as st
import pandas as pd
import json
import os

# --- 1. הזרקת CSS (שילוב של הסיידבר והקופסה הלבנה מההרשמה) ---
st.markdown(
    """
    <style>
        /* יישור הסיידבר לימין */
        div[data-testid="stSidebarUserContent"] {
            direction: rtl !important;
            text-align: right !important;
            padding-top: 1.5rem !important;
        }
        section[data-testid="stSidebar"] {
            right: 0 !important;
            left: auto !important;
        }

        /* הסטייל של הקופסה הלבנה */
        div[data-testid*="olumn"]:nth-child(2) > div {
            background-color: #FFFFFF !important;
            opacity: 1 !important;
            padding: 2.5rem !important;
            border-radius: 16px !important;
            box-shadow: 0px 12px 35px rgba(0,0,0,0.1) !important;
            border: 1px solid #EAEAEA !important;
        }

        /* ניקוי רקעים כפולים */
        div[data-testid="stVerticalBlockBorderWrapper"] {
            background-color: transparent !important;
        }

        /* התאמת כותרות בתוך הקופסה הלבנה */
        h1, h3 {
            color: #1f1f1f !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# --- 2. תפריט צד ---
with st.sidebar:
    st.title("תפריט מערכת")
    if st.button("🚪 התנתקות מהמערכת", use_container_width=True):
        st.session_state.search_done = False
        st.session_state.user_id = ""
        st.session_state.page = 'home'
        st.rerun()


# --- 3. פונקציות טעינה וניהול ---
def load_json(filename):
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []


def cancel_appointment(student_id, tutor_name, day, hour):
    filename = 'appointments.json'
    appointments = load_json(filename)

    # סינון החוצה של הפגישה הספציפית
    updated_appointments = [
        app for app in appointments
        if not (
                str(app.get("student_id")).strip().lower() == str(student_id).strip().lower() and
                str(app.get("tutor_name")).strip().lower() == str(tutor_name).strip().lower() and
                str(app.get("day")).strip().lower() == str(day).strip().lower() and
                str(app.get("hour")).strip().lower() == str(hour).strip().lower()
        )
    ]

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(updated_appointments, f, indent=4, ensure_ascii=False)


# --- 4. לוגיקה מרכזית (ממורכזת בתוך הקופסה הלבנה) ---
spacer_right, center_col, spacer_left = st.columns([1, 3, 1])

with center_col:
    st.markdown("<h1 style='text-align: center;'>לוח הפגישות שלי</h1>", unsafe_allow_html=True)

    tutor_id = st.session_state.get('user_id', '')

    if not tutor_id:
        st.error("לא נמצא מזהה מורה. אנא התחבר מחדש.")
    else:
        # טעינת נתונים
        df = pd.read_csv('syn_data.csv')
        appointments = load_json('appointments.json')

        tutor_row = df[df['ID'].astype(str).str.strip() == str(tutor_id).strip()]

        if tutor_row.empty:
            st.error("מורה לא נמצא במאגר.")
        else:
            tutor_name = tutor_row['Name'].iloc[0]
            st.markdown(f"<h3 style='text-align: center;'>שלום, {tutor_name}</h3>", unsafe_allow_html=True)
            st.divider()

            # סינון פגישות למורה הנוכחי
            my_appointments = [
                app for app in appointments
                if str(app.get('tutor_name', '')).strip().lower() == str(tutor_name).strip().lower()
            ]

            if not my_appointments:
                st.info("אין לך פגישות קרובות במערכת כרגע.")
            else:
                # הצגת כל פגישה
                for index, app in enumerate(my_appointments):
                    student_id = str(app.get('student_id', '')).strip()
                    student_rows = df[df['ID'].astype(str).str.strip() == student_id]

                    if not student_rows.empty:
                        student_name = student_rows['Name'].iloc[0]
                        student_phone = student_rows['Phone number'].iloc[0]
                    else:
                        student_name = app.get('student_name', "תלמיד")
                        student_phone = app.get('phone', 'לא זמין')

                    with st.container():
                        st.success(
                            f"📅 **יום:** {app.get('day')}  |  ⏰ **שעה:** {app.get('hour')} \n\n"
                            f"👤 **שם התלמיד:** {student_name}  \n"
                            f"📱 **טלפון:** {student_phone}  \n"
                            f"📚 **מקצוע:** {app.get('subject', 'כללי')}"
                        )

                        # כפתור ביטול ייעודי למורה
                        if st.button(f"❌ ביטול פגישה עם {student_name}", key=f"cancel_tut_{index}",
                                     use_container_width=True):
                            cancel_appointment(student_id, tutor_name, app.get('day'), app.get('hour'))
                            st.toast("הפגישה בבוטלה בהצלחה והתור התפנה!")
                            st.rerun()
                    st.write("")  # מרווח