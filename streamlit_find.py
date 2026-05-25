import json
import os
import streamlit as st
import pandas as pd
from main import find_a_match

# --- CSS עיצוב ---
st.markdown(
    """
    <style>
        section[data-testid="stSidebar"] { left: auto !important; right: 0 !important; width: 300px !important; }
        div[data-testid="stSidebarUserContent"] { padding-top: 1rem !important; direction: rtl !important; text-align: right !important; }
    </style>
    """,
    unsafe_allow_html=True
)

# --- תפריט צד ---
with st.sidebar:
    st.title("תפריט מערכת")
    if st.button("🚪 התנתקות מהמערכת", use_container_width=True):
        st.session_state.search_done = False
        st.session_state.user_id = ""
        st.session_state.page = 'home'
        st.rerun()


# --- פונקציות עזר ---
def load_json(filename):
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    return [] if "appointments" in filename else {}


def save_appointment(student_id, tutor_info):
    filename = 'appointments.json'
    appointments = load_json(filename)

    # 🌟 התיקון: הוספנו .str.lower() ו-.lower() כדי להתעלם מאותיות גדולות/קטנות
    df_users = pd.read_csv('syn_data.csv', dtype={'ID': str})
    student_row = df_users[
        df_users['ID'].astype(str).str.strip().str.lower() == str(student_id).strip().lower()
        ]

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


# --- לוגיקה ראשית ---
data = load_json('student_matches_detailed.json')
appointments = load_json('appointments.json')

if "search_done" not in st.session_state: st.session_state.search_done = False

spacer_right, center_col, spacer_left = st.columns([1, 2, 1])

with center_col:
    st.markdown("<h1 style='text-align: center;'>מערכת התאמת מורים</h1>", unsafe_allow_html=True)

    if not st.session_state.search_done:
        with st.form("search_form"):
            raw_input = st.text_input("הקלד תעודת זהות:", max_chars=20)
            if st.form_submit_button("חפש מורים"):
                st.session_state.user_id = raw_input.strip()
                st.session_state.search_done = True
                st.rerun()
    else:
        user_id = st.session_state.user_id

        find_a_match()

        data = load_json('student_matches_detailed.json')
        appointments = load_json('appointments.json')

        if user_id in data:
            # 🌟 גם כאן מתעלמים מהבדלי אותיות במציאת התורים של התלמיד
            user_appointments = [
                app for app in appointments
                if str(app.get("student_id")).strip().lower() == str(user_id).strip().lower()
            ]

            if user_appointments:
                st.warning("הפגישות שנקבעו לך:")
                for app in user_appointments:
                    st.info(
                        f"📅 **יום:** {app['day']}  |  "
                        f"⏰ **שעה:** {app['hour']}  |  "
                        f"📚 **מקצוע:** {app.get('subject', 'כללי')}  |  "
                        f"👤 **מורה:** {app['tutor_name']}"
                    )

            all_tutors = data[user_id]

            # סינון תורים שכבר נתפסו
            available_tutors = []
            for tutor_info in all_tutors:
                is_booked = False
                for app in appointments:
                    # 🌟 השוואה חסינה לחלוטין (מוודא שגם המורה וגם היום לא יושפעו מאותיות גדולות/קטנות)
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

            st.subheader("מורים זמינים:")

            if not available_tutors:
                st.info("אין כרגע תורים פנויים למורים עבורך.")
            else:
                for index, tutor_info in enumerate(available_tutors):
                    st.info(
                        f"📅 **יום:** {tutor_info['Day']}  |  "
                        f"⏰ **שעה:** {tutor_info['Hour']}  |  "
                        f"📚 **מקצוע:** {tutor_info.get('Subject', 'כללי')}  |  "
                        f"👤 **מורה:** {tutor_info['Name']}"
                    )

                    if st.button(f"קביעת פגישה עם {tutor_info['Name']} ({tutor_info['Day']} ב-{tutor_info['Hour']})",
                                 key=f"btn_{index}"):
                        save_appointment(user_id, tutor_info)
                        st.toast("הפגישה נקבעה בהצלחה!")
                        st.rerun()
        else:
            st.error("תעודת הזהות לא נמצאה.")
            if st.button("חזרה"):
                st.session_state.search_done = False
                st.rerun()