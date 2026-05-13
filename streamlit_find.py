import streamlit as st
import json
import os


@st.cache_data
def load_data():
    with open('student_matches_detailed.json', 'r', encoding='utf-8') as f:
        return json.load(f)


data = load_data()

st.title("מערכת התאמת מורים אישית")
st.write("ברוכים הבאים! כאן תוכלו למצוא את המורים המותאמים לכם.")

with st.form("search_form"):
    raw_input = st.text_input("הקלד את מספר תעודת הזהות שלך (9 ספרות):", max_chars=9)
    submitted = st.form_submit_button("חפש מורים")
if submitted:
    user_id = raw_input.strip()
    if user_id:
        if not user_id.isdigit():
            st.error("נא להזין ספרות בלבד.")
        elif len(user_id) < 9:
            st.warning("תעודת זהות חייבת לכלול 9 ספרות.")
        else:
            if user_id in data:
                tutors = data[user_id]

                if tutors:
                    st.success(f"מצאנו עבורך {len(tutors)} מורים:")
                    cols = st.columns(len(tutors))

                    for index, tutor_info in enumerate(tutors):
                        with cols[index]:
                            st.info(f"*{tutor_info['Name']}*")
                            st.write(f" יום {tutor_info['Day']}")
                            st.write(f" שעה {tutor_info['Hour']}")
                            st.write(f" טלפון {tutor_info['Phone']} ")

                            # הכפתור - האירוע שמפעיל את הכל
                            if st.button("קביעת פגישה", key=f"btn_{tutor_info['Name']}_{index}"):
                                def save_appointment(student_id, tutor_name):
                                    print("you hit")
                                    filename = 'appointments.json'
                                    new_entry = {"student_id": student_id, "Name": tutor_name}
                                    # בדיקה אם הקובץ כבר קיים
                                    if os.path.exists(filename):
                                        with open(filename, 'r', encoding='utf-8') as f:
                                            data = json.load(f)
                                    else:
                                        data = []  # אם הקובץ לא קיים, נתחיל רשימה ריקה

                                    # הוספת הבחירה החדשה ושמירה
                                    data.append(new_entry)
                                    with open(filename, 'w', encoding='utf-8') as f:
                                        json.dump(data, f, indent=4, ensure_ascii=False)
                                # משוב ויזואלי למשתמש
                                st.success(f"הפגישה עם {tutor_info['Name']} נרשמה במערכת!")
                                st.balloons()
                else:
                    st.warning("כרגע אין מורים שמתאימים לך במערכת.")
            else:
                st.error("מספר תעודת הזהות לא נמצא במאגר.")