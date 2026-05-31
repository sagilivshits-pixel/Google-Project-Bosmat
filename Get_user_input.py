import pandas as pd
import json
import datetime
import streamlit as st
import hashlib

dataf = pd.read_csv('syn_data.csv')
CSV_PATH = "syn_data.csv"

st.title("Tutor/Student Entry Form")

# ── Initialize Session State for ID verification flow ─────────────────────────
if "id_verified" not in st.session_state:
    st.session_state.id_verified = False
if "verified_id" not in st.session_state:
    st.session_state.verified_id = ""

# ── STEP 1: ID CHECK FORM (Only shows if not verified yet) ────────────────────
if not st.session_state.id_verified:
    with st.form("ID form"):
        ID_entry = {
            "ID": st.text_input("enter id :")
        }
        ID_BUTTON = st.form_submit_button("Submit ID ")

    if ID_BUTTON:
        if not ID_entry["ID"]:
            st.error("Please write an id")
        else:
            try:
                df_existing = pd.read_csv(CSV_PATH, dtype={"ID": str})
                if ID_entry["ID"] in df_existing["ID"].values:
                    st.error("User exists, please go to sign-in")
                else:
                    # ID passes all checks! Save it and unlock the next form
                    st.session_state.verified_id = ID_entry["ID"]
                    st.session_state.id_verified = True
                    st.rerun()
            except FileNotFoundError:
                # If file doesn't exist yet, any ID is automatically valid
                st.session_state.verified_id = ID_entry["ID"]
                st.session_state.id_verified = True
                st.rerun()


# ── STEP 2: REGISTRATION FORM (Only shows AFTER ID is verified) ───────────────
else:
    # Display a small badge showing they are locked in with their verified ID
    st.success(f"ID Verified: {st.session_state.verified_id}")

    # שימוש בקונטיינר עם מסגרת במקום פורום - נראה זהה לחלוטין ומאפשר עדכון חי!
    with st.container(border=True):
        st.subheader("Fill in your details:")

        # איסוף הסיסמה והצפנתה
        password_raw = st.text_input("Enter your password : ", type="password")

        # המולטיסלקט המקורי שלך
        selected_days = st.multiselect("select the days",
                                       ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"])

        # מילוי שעות דינמי שמופיע מיד על המסך רק עבור הימים שנבחרו
        hours_list = []
        if selected_days:
            st.write("Set hours for your selected days:")
            for day in selected_days:
                # יוצר תיבת זמן ייחודית לכל יום שנבחר באופן מיידי
                chosen_time = st.time_input(f"Select hour for {day}", datetime.time(19, 0), key=f"time_{day}")
                hours_list.append(chosen_time.strftime("%H:%M"))

        entry = {
            "Pass": hashlib.sha256(password_raw.encode()).hexdigest(),
            "Name": st.text_input("Enter your name :"),
            "Tutor / Student": st.selectbox("what are you?", ["Tutor", "Student"]),
            "Subject": st.multiselect("Select your subjects",
                                      ["Math", "English", "Physics", "Biology", "Chemistry", "History",
                                       "Computer Science"]),
            "Online / F2F": st.selectbox("Face to face or online?", ["Online", "F2F"]),
            "Day": selected_days,  # שומר את רשימת הימים שנבחרו
            "Hour": hours_list,  # שומר את השעות המתאימות להם בדיוק
            "Phone number": st.text_input("phone number :"),
        }

        # כפתור רישום במקום כפתור פורום כדי לאפשר קריאה דינמית של השדות
        submitted = st.button("Register")

    # ── Append to CSV & Navigation ──────────────────────────────────────────────────
    if submitted:
        if not entry["Subject"] or not entry["Day"]:
            st.error("Please select at least one Subject and one Day.")
        else:
            # יצירת ה-DataFrame ופירוק הרשימות לשורות נפרדות
            new_entry_df = pd.DataFrame([entry])
            new_entry_df["ID"] = st.session_state.verified_id  # משתמש ב-ID השמור מהשלב הראשון

            # פירוק מקביל השומר על המבנה המקורי של הדאטה בייס שלך
            new_entry_df = new_entry_df.explode('Subject')
            new_entry_df = new_entry_df.explode(['Day', 'Hour'])  # פירוק סימולטני (היום והשעה שלו ביחד)

            try:
                df_existing = pd.read_csv(CSV_PATH, dtype={"ID": str, "Phone number": str})
                df = pd.concat([df_existing, new_entry_df], ignore_index=True)
            except FileNotFoundError:
                df = new_entry_df

            # שמירה לקובץ
            df.to_csv(CSV_PATH, index=False)
            st.success(f"Success! Added {len(new_entry_df)} record combinations to the database.")
            st.balloons()

            # Clear out the verification state so the script resets properly for subsequent uses
            st.session_state.id_verified = False
            st.session_state.verified_id = ""

            # ניתוב דינמי ומדויק לפי עמודת התפקיד (אינדקס 2 ב-new_entry_df)
            if new_entry_df.iloc[0, 2] == "Student":
                st.session_state.user_id = new_entry_df.iloc[0, 8]  # Maps to ID column cleanly
                st.session_state.page = 'find'
                st.rerun()
            else:
                st.session_state.user_id = new_entry_df.iloc[0, 8]
                st.session_state.page = 'Tutor_page'
                st.rerun()