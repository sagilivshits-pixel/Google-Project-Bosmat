import pandas as pd
import json
import datetime
import streamlit as st
import hashlib

dataf = pd.read_csv('syn_data.csv')
CSV_PATH = "syn_data.csv"

# ── Collect input ─────────────────────────────────────────────────────────────
st.title("Tutor/Student Entry Form")

# טופס בדיקת ה-ID הקיים
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
        except FileNotFoundError:
            pass

# טופס המילוי הראשי - מסודר ונקי
with st.form("entry_form"):
    st.subheader("Fill in your details:")

    # איסוף הסיסמה והצפנתה
    password_raw = st.text_input("Enter your password : ", type="password")

    entry = {
        "Pass": hashlib.sha256(password_raw.encode()).hexdigest(),
        "ID": st.text_input("Enter ID (9 digits):"),
        "Name": st.text_input("Enter your name :"),
        "Tutor / Student": st.selectbox("what are you?", ["Tutor", "Student"]),
        "Subject": st.multiselect("Select your subjects",
                                  ["Math", "English", "Physics", "Biology", "Chemistry", "History",
                                   "Computer Science"]),
        "Online / F2F": st.selectbox("Face to face or online?", ["Online", "F2F"]),
        "Day": st.multiselect("select the days",
                              ["sunday", "monday", "tuesday", "Wednesday", "thursday", "friday", "saturday"]),
        "Hour": st.time_input('Select an hour', datetime.time(19, 0)).strftime("%H:%M"),
        "Phone number": st.text_input("phone number :"),
    }

    submitted = st.form_submit_button("Register")

# ── Append to CSV & Navigation ──────────────────────────────────────────────────
if submitted:
    if not entry["Subject"] or not entry["Day"]:
        st.error("Please select at least one Subject and one Day.")
    else:
        # יצירת ה-DataFrame ופירוק הרשימות לשורות נפרדות
        new_entry_df = pd.DataFrame([entry])
        new_entry_df["ID"] = ID_entry["ID"]
        new_entry_df = new_entry_df.explode('Subject').explode('Day')

        try:
            df_existing = pd.read_csv(CSV_PATH, dtype={"ID": str, "Phone number": str})
            df = pd.concat([df_existing, new_entry_df], ignore_index=True)
        except FileNotFoundError:
            df = new_entry_df

        # שמירה לקובץ
        df.to_csv(CSV_PATH, index=False)
        st.success(f"Success! Added {len(new_entry_df)} record combinations to the database.")
        st.balloons()

        # ניתוב דינמי ומדויק לפי עמודת התפקיד (אינדקס 2 ב-new_entry_df)
        if new_entry_df.iloc[0, 2] == "Student":
            st.session_state.user_id = ID_entry["ID"]
            st.session_state.page = 'find'
            st.rerun()
        else:
            st.session_state.user_id = ID_entry["ID"]
            st.session_state.page = 'Tutor_page'
            st.rerun()