import json
import os
import streamlit as st
import pandas as pd
from main import find_a_match

# --- 1. הזרקת CSS (שילוב של הסיידבר והקופסה הלבנה) ---
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

        /* הסטייל של הקופסה הלבנה (מתוך Get_user_input) */
        div[data-testid*="olumn"]:nth-child(2) > div {
            background-color: #FFFFFF !important;
            background: #FFFFFF !important;
            opacity: 1 !important;
            padding: 2.5rem !important;
            border-radius: 16px !important;
            box-shadow: 0px 12px 35px rgba(0,0,0,0.08) !important;
            border: 1px solid #EAEAEA !important;
        }

        /* ניקוי רקעים כפולים ומניעת כפל גבולות */
        div[data-testid="stVerticalBlockBorderWrapper"], 
        div[data-testid="stForm"] {
            background-color: transparent !important;
            background: transparent !important;
            border: none !important;
            padding: 0 !important;
        }

        /* התאמת פונטים וצבעים בתוך הקופסה */
        div[data-testid*="olumn"]:nth-child(2) label,
        div[data-testid*="olumn"]:nth-child(2) p,
        div[data-testid*="olumn"]:nth-child(2) span,
        div[data-testid*="olumn"]:nth-child(2) h1,
        div[data-testid*="olumn"]:nth-child(2) h3 {
            color: #262730 !important;
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


# --- 3. פונקציות עזר ---
def load_json(filename):
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    return [] if "appointments" in filename else {}


def save_appointment(student_id, tutor_info):
    filename = 'appointments.json'
    appointments = load_json(filename)
    df_users = pd.read_csv('syn_data.csv', dtype={'ID': str})
    student_row = df_users[df_users['ID'].astype(str).str.strip().str.lower() == str(student_id).strip().lower()]
    student_name = student_row['Name'].iloc[0] if not student_row.empty else "תלמיד"

    new_entry = {
        "student_id": str(student_id).strip(),
        "student_name": student_name,
        "tutor_name": tutor_info['Name'],
        "day": tutor_info['Day'],
        "hour": tutor_info['Hour'],
        "phone": tutor_info['Phone'],
        "subject": tutor_info.get('Subject', 'Subject')
    }
    appointments.append(new_entry)
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(appointments, f, indent=4, ensure_ascii=False)


# --- 4. לוגיקה ראשית בתוך הקופסה הלבנה ---
if "search_done" not in st.session_state:
    st.session_state.search_done = False

# יצירת מבנה עמודות למרכוז (העמודה השנייה תהפוך לקופסה הלבנה)
spacer_right, center_col, spacer_left = st.columns([1, 3, 1])

with center_col:
    st.markdown("<h1 style='text-align: center;'>מערכת התאמת מורים</h1>", unsafe_allow_html=True)
    st.write("")  # מרווח קטן

    if not st.session_state.search_done:
        with st.form("search_form"):
            st.subheader("שלום! הקלד תעודת זהות כדי להתחיל:")
            raw_input = st.text_input("תעודת זהות (9 ספרות):", max_chars=20)
            if st.form_submit_button("חפש מורים זמינים"):
                st.session_state.user_id = raw_input.strip()
                st.session_state.search_done = True
                st.rerun()
    else:
        user_id = st.session_state.user_id
        find_a_match()  # הרצת לוגיקת ההתאמה

        data = load_json('student_matches_detailed.json')
        appointments = load_json('appointments.json')

        if user_id in data:
            # הצגת פגישות קיימות
            user_appointments = [
                app for app in appointments
                if str(app.get("student_id")).strip().lower() == str(user_id).strip().lower()
            ]

            if user_appointments:
                st.warning("📅 הפגישות שנקבעו לך:")
                for app in user_appointments:
                    st.info(
                        f"**מורה:** {app['tutor_name']}  |  "
                        f"**יום:** {app['day']}  |  "
                        f"**שעה:** {app['hour']}  |  "
                        f"**מקצוע:** {app.get('subject', 'כללי')}"
                    )
                st.divider()

            # סינון והצגת מורים פנויים
            all_tutors = data[user_id]
            available_tutors = []
            for tutor_info in all_tutors:
                is_booked = False
                for app in appointments:
                    if (str(app.get('tutor_name', '')).strip().lower() == str(
                            tutor_info.get('Name', '')).strip().lower() and
                            str(app.get('day', '')).strip().lower() == str(
                                tutor_info.get('Day', '')).strip().lower() and
                            str(app.get('hour', '')).strip().lower() == str(
                                tutor_info.get('Hour', '')).strip().lower()):
                        is_booked = True
                        break
                if not is_booked:
                    available_tutors.append(tutor_info)

            st.subheader("מורים זמינים עבורך:")
            if not available_tutors:
                st.info("אין כרגע תורים פנויים המתאימים לדרישות שלך.")
            else:
                for index, tutor_info in enumerate(available_tutors):
                    # כל מורה מופיע בקופסה כחולה/ירוקה בתוך המתחם הלבן
                    with st.container():
                        st.info(
                            f"👤 **מורה:** {tutor_info['Name']}  \n"
                            f"📚 **מקצוע:** {tutor_info.get('Subject', 'כללי')}  \n"
                            f"⏰ **מועד:** {tutor_info['Day']} בשעה {tutor_info['Hour']}"
                        )
                        if st.button(f"קביעת פגישה עם {tutor_info['Name']}", key=f"btn_{index}",
                                     use_container_width=True):
                            save_appointment(user_id, tutor_info)
                            st.toast("הפגישה נקבעה בהצלחה!")
                            st.rerun()
                    st.write("")  # מרווח בין מורים

            if st.button("🔎 חיפוש חדש"):
                st.session_state.search_done = False
                st.rerun()
        else:
            st.error("מצטערים, תעודת הזהות לא נמצאה במערכת.")
            if st.button("חזרה לחיפוש"):
                st.session_state.search_done = False
                st.rerun()