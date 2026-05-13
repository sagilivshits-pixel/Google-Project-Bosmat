import streamlit as st
import json
import os


# --- פונקציות עזר ---

def load_json(filename):
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    return [] if "appointments" in filename else {}


def save_appointment(student_id, tutor_info):
    filename = 'appointments.json'
    appointments = load_json(filename)

    # יצירת הרשומה החדשה עם כל הפרטים הנדרשים
    new_entry = {
        "student_id": student_id,
        "tutor_name": tutor_info['Name'],
        "day": tutor_info['Day'],
        "hour": tutor_info['Hour'],
        "subject": tutor_info.get('Subject', 'לא צוין')  # הנחה שיש שדה Subject במקור
    }

    appointments.append(new_entry)
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(appointments, f, indent=4, ensure_ascii=False)


# --- הגדרות דף ---
st.title("מערכת התאמת מורים אישית")

# טעינת הנתונים
data = load_json('student_matches_detailed.json')
appointments = load_json('appointments.json')

# ניהול מצב ב-Session State
if "search_done" not in st.session_state:
    st.session_state.search_done = False
if "user_id" not in st.session_state:
    st.session_state.user_id = ""

# --- ממשק משתמש ---
with st.form("search_form"):
    raw_input = st.text_input("הקלד את מספר תעודת הזהות שלך (9 ספרות):", max_chars=9)
    submitted = st.form_submit_button("חפש מורים")

if submitted:
    st.session_state.user_id = raw_input.strip()
    st.session_state.search_done = True

if st.session_state.search_done:
    user_id = st.session_state.user_id

    if not user_id.isdigit() or len(user_id) < 9:
        st.error("נא להזין תעודת זהות תקינה (9 ספרות).")
    elif user_id in data:
        all_tutors = data[user_id]

        # --- לוגיקת הסינון ---
        # אנחנו בונים רשימה של "מורים תפוסים" לפי מפתח של שם+יום+שעה+מקצוע
        busy_slots = [
            f"{a['tutor_name']}{a['day']}{a['hour']}_{a['subject']}"
            for a in appointments
        ]

        # מציגים רק מורים שלא נמצאים ב-busy_slots
        available_tutors = [
            t for t in all_tutors
            if f"{t['Name']}{t['Day']}{t['Hour']}_{t.get('Subject', 'לא צוין')}" not in busy_slots
        ]

        if available_tutors:
            st.success(f"מצאנו עבורך {len(available_tutors)} מורים פנויים:")
            cols = st.columns(min(len(available_tutors), 3))  # הגבלה ל-3 עמודות בשורה לנראות

            for index, tutor_info in enumerate(available_tutors):
                with cols[index % 3]:
                    st.info(f"*{tutor_info['Name']}*")
                    st.write(f" מקצוע: {tutor_info.get('Subject', 'לא צוין')}")
                    st.write(f" יום {tutor_info['Day']}, שעה {tutor_info['Hour']}")
                    st.write(f" {tutor_info['Phone']}")

                    if st.button(f"קביעת פגישה", key=f"btn_{index}"):
                        save_appointment(user_id, tutor_info)
                        st.success(f"נקבעה פגישה עם {tutor_info['Name']}!")
                        st.balloons()
                        # ריצה מחדש כדי לעדכן את הרשימה ולהעלים את המורה שתפסנו
                        st.rerun()
        else:
            st.warning("כל המורים המתאימים לך כבר תפוסים בשעות אלו.")
    else:
        st.error("מספר תעודת הזהות לא נמצא.")