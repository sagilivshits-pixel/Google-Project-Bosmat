import json
import os
import streamlit as st

# --- 1. הגדרות דף והזרקת CSS (תיקון מינימייז ותזוזה למרכז) ---
st.set_page_config(layout="wide")

st.markdown(
    """
    <style>
        /* 1. אכיפת כיוון עברית על כל המסך */
        html, body, [data-testid="stAppViewContainer"] {
            direction: rtl;
            text-align: right;
        }

        /* 2. סידור הסיידבר בצד ימין כשהוא פתוח */
        section[data-testid="stSidebar"] {
            left: auto !important;
            right: 0 !important;
            width: 300px !important;
            min-width: 300px !important;
            max-width: 300px !important;
            z-index: 99999 !important;
            transition: transform 0.3s ease, width 0.3s ease, min-width 0.3s ease !important;
        }

        /* 3. 🔥 התיקון הקריטי למינימייז: כשהסיידבר סגור, מאפסים לו את הרוחב 
           ומזיזים אותו ימינה כדי שהתוכן הראשי יתמרכז על כל רוחב המסך באופן אוטומטי! */
        section[data-testid="stSidebar"][aria-expanded="false"] {
            width: 0px !important;
            min-width: 0px !important;
            max-width: 0px !important;
            transform: translateX(300px) !important;
        }

        /* 4. פתרון למיקום כפתור הפתיחה (החץ המרחף) כשהסיידבר סגור */
        div[data-testid="collapsedControl"] {
            left: auto !important;
            right: 20px !important;
            top: 15px !important;
            z-index: 999999 !important;
            cursor: pointer !important;
        }

        /* סידור אזור כפתור הסגירה בתוך הסיידבר הפתוח */
        div[data-testid="stSidebarHeader"] {
            direction: ltr !important; 
        }

        /* הפיכת האייקונים של החצים שיצביעו לכיוונים הנכונים בעברית */
        div[data-testid="collapsedControl"] svg,
        div[data-testid="stSidebarHeader"] svg {
            transform: rotate(180deg) !important;
        }

        /* 5. החלקת התנועה של התוכן הראשי בזמן פתיחה/סגירה */
        div[data-testid="stMain"] {
            margin-left: 0 !important;
            margin-right: 0 !important;
            transition: margin 0.3s ease !important;
        }

        /* סידור פנימי של הריווח בסיידבר */
        div[data-testid="stSidebarUserContent"] {
            padding-top: 1rem !important;
            direction: rtl !important;
            text-align: right !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# --- 2. תפריט צד (Sidebar) ימני ---
with st.sidebar:
    st.title("תפריט מערכת")
    st.write("שלום משתמש!")
    st.markdown("---")

    # כפתור התנתקות שמחזיר לעמוד הבית
    if st.button("🚪 התנתקות מהמערכת", use_container_width=True):
        st.session_state.search_done = False
        st.session_state.user_id = ""
        st.switch_page("start_page.py")


# --- 3. פונקציות עזר ---
def load_json(filename):
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    return [] if "appointments" in filename else {}


def save_appointment(student_id, tutor_info):
    filename = 'appointments.json'
    appointments = load_json(filename)
    new_entry = {
        "student_id": student_id,
        "tutor_name": tutor_info['Name'],
        "day": tutor_info['Day'],
        "hour": tutor_info['Hour'],
        "phone": tutor_info['Phone'],
        "subject": tutor_info.get('Subject', ['Subject'])
    }
    appointments.append(new_entry)
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(appointments, f, indent=4, ensure_ascii=False)


# --- 4. ממשק משתמש ותוכן ראשי ---
# טעינת הנתונים
data = load_json('student_matches_detailed.json')
appointments = load_json('appointments.json')

if "search_done" not in st.session_state:
    st.session_state.search_done = False
if "user_id" not in st.session_state:
    st.session_state.user_id = ""

# עמודות יחסיות ששומרות על מרכוז מושלם ומתרחבות באופן דינמי
spacer_right, center_col, spacer_left = st.columns([1, 2, 1])

with center_col:
    st.markdown("<h1 style='text-align: center; margin-bottom: 2rem;'>מערכת התאמת מורים אישית</h1>",
                unsafe_allow_html=True)

    with st.form("search_form"):
        raw_input = st.text_input("הקלד את מספר תעודת הזהות שלך (9 ספרות):", max_chars=9)
        submitted = st.form_submit_button("חפש מורים")

if submitted:
    st.session_state.user_id = raw_input.strip()
    st.session_state.search_done = True

if st.session_state.search_done:
    user_id = st.session_state.user_id
    if not user_id.isdigit() or len(user_id) < 9:
        with center_col:
            st.error("נא להזין תעודת זהות תקינה (9 ספרות).")
    elif user_id in data:
        user_appointments = [app for app in appointments if app.get("student_id") == user_id]

        with center_col:
            if user_appointments:
                st.warning("כבר קבעת פגישה במערכת:")
                for app in user_appointments:
                    phone = app.get('phone', ['Phone'])
                    st.info(
                        f" *תלמיד:* {app['student_id']}  \n"
                        f" *מורה:* {app['tutor_name']}  \n"
                        f" *מקצוע:* {app.get('subject', ['Subject'])}  \n"
                        f" *יום:* {app['day']}, *שעה:* {app['hour']}  \n"
                        f" *טלפון:* {phone}"
                    )
                st.divider()

            all_tutors = data[user_id]
            busy_slots = [
                f"{a['tutor_name']}{a['day']}{a['hour']}_{a['subject']}"
                for a in appointments
            ]

            available_tutors = [
                t for t in all_tutors
                if f"{t['Name']}{t['Day']}{t['Hour']}_{t.get('Subject', ['Subject'])}" not in busy_slots
            ]

        # אזור המורים להצגה במרכז הדף
        if available_tutors:
            with center_col:
                st.subheader("מורים נוספים שזמינים עבורך:")
                cols = st.columns(min(len(available_tutors), 3))

                for index, tutor_info in enumerate(available_tutors):
                    with cols[index % 3]:
                        st.info(f"*{tutor_info['Name']}*\n")
                        st.write(f" מקצוע: {tutor_info.get('Subject', ['Subject'])}\n")
                        st.write(f" יום: {tutor_info['Day']}\n")
                        st.write(f" שעה: {tutor_info['Hour']}\n")
                        st.write(f" טלפון: {tutor_info['Phone']}")

                        if st.button(f"קביעת פגישה", key=f"btn_{index}"):
                            save_appointment(user_id, tutor_info)
                            st.toast(f"נקבעה פגישה עם {tutor_info['Name']}!")
                            st.balloons()
                            st.rerun()

        elif not user_appointments:
            with center_col:
                st.warning("כל המורים המתאימים לך כבר תפוסים בשעות אלו.")
    else:
        with center_col:
            st.error("מספר תעודת הזהות לא נמצא במאגר.")