import json
import os
import streamlit as st

# --- 1. הזרקת ה-CSS הפנימי בלבד (ללא set_page_config שיוצר שגיאה) ---
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

# --- 2. תפריט צד (Sidebar) ימני ---
with st.sidebar:
    st.title("תפריט מערכת")
    st.write("שלום משתמש!")
    st.markdown("---")

    # כפתור התנתקות שמחזיר לעמוד הבית הראשי דרך הסטייט של קובץ האם
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


# --- 4. טעינת נתונים ראשונית ---
data = load_json('student_matches_detailed.json')
appointments = load_json('appointments.json')

if "search_done" not in st.session_state:
    st.session_state.search_done = False
if "user_id" not in st.session_state:
    st.session_state.user_id = ""

# שמירה על המרכוז הקיים בעזרת עמודות פריסה
spacer_right, center_col, spacer_left = st.columns([1, 2, 1])

# --- 5. ממשק משתמש ותוכן ראשי ---
with center_col:
    st.markdown("<h1 style='text-align: center; margin-bottom: 2rem;'>מערכת התאמת מורים אישית</h1>",
                unsafe_allow_html=True)

    if not st.session_state.search_done:
        with st.form("search_form"):
            raw_input = st.text_input("הקלד את מספר תעודת הזהות שלך (9 ספרות):", max_chars=9)
            submitted = st.form_submit_button("חפש מורים")

        if submitted:
            st.session_state.user_id = raw_input.strip()
            st.session_state.search_done = True
            st.rerun()

if st.session_state.search_done:
    user_id = st.session_state.user_id

    if not user_id.isdigit() or len(user_id) < 9:
        with center_col:
            st.error("נא להזין תעודת זהות תקינה (9 ספרות).")
            if st.button("חזרה לחיפוש"):
                st.session_state.search_done = False
                st.rerun()

    elif user_id in data:
        user_appointments = [app for app in appointments if app.get("student_id") == user_id]

        with center_col:
            if user_appointments:
                st.warning("הפגישות שנקבעו לך:")
                for app in user_appointments:
                    phone = app.get('phone', app.get('Phone', ['Phone']))
                    st.info(
                        f" *תלמיד:* {app['student_id']}  \n"
                        f" *מורה:* {app['tutor_name']}  \n"
                        f" *מקצוע:* {app.get('subject', ['Subject'])}  \n"
                        f" *יום:* {app['day']}, *שעה:* {app['hour']}  \n"
                        f" *טלפון:* {phone}"
                    )
                st.divider()  # קו הפרדה ויזואלי בין פגישות קיימות למורים פנויים

            all_tutors = data[user_id]
            busy_slots = [
                f"{a['tutor_name']}{a['day']}{a['hour']}_{a.get('subject', ['Subject'])}"
                for a in appointments
            ]

            available_tutors = [
                t for t in all_tutors
                if f"{t['Name']}{t['Day']}{t['Hour']}_{t.get('Subject', ['Subject'])}" not in busy_slots
            ]

        # טיפול בהצגת המורים הזמינים (מחוץ ל-with center_col כדי למנוע בעיות ריקוד עמודות פנימיות בסטרימליט)
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
            if st.button("חזרה לחיפוש"):
                st.session_state.search_done = False
                st.rerun()