import pandas as pd
import json
import datetime
import streamlit as st
import hashlib
dataf = pd.read_csv('syn_data.csv')
CSV_PATH = "syn_data.csv"
M_rows = dataf.shape[0]
# ── Collect input ─────────────────────────────────────────────────────────────
st.title("Tutor/Student Entry Form")
with st.form("entry_form"):
    entry = {
        "Pass": hashlib.sha256(st.text_input("Enter your password : ").encode()).hexdigest(),
        "ID": st.text_input("Enter ID :"),
        "Name": st.text_input("Enter your name :"),
        "Tutor / Student": st.selectbox("what are you?", ["Tutor", "Student"]),
        "Subject": st.multiselect("Select your subjects",
                                      ["Math", "English", "Physics", "Biology", "Chemistry", "History",
                                       "Computer Science"]),
        "Online / F2F": st.selectbox("Face to face or online?", ["Online", "F2F"]),
        "Day": st.multiselect("select the days",
                                  ["sunday", "monday", "tuesday", "Wednesday", "thursday", "friday", "saturday"]),
        "Hour": st.time_input('Select an hour', datetime.time(19, 0)).strftime("%H:%M"),  # Format time as string
        "Phone number": st.text_input("phone number :"),
        }
    submitted = st.form_submit_button("Register")


if submitted:
            if not entry["Subject"] or not entry["Day"]:
                st.error("Please select at least one Subject and one Day.")
            else:
                # Create DataFrame and explode the lists into separate rows
                new_entry_df = pd.DataFrame([entry])
                new_entry_df = new_entry_df.explode('Subject').explode('Day')

                try:
                    df_existing = pd.read_csv(CSV_PATH, dtype={"ID": str, "Phone number": str})
                    df = pd.concat([df_existing, new_entry_df], ignore_index=True)
                except FileNotFoundError:
                    df = new_entry_df

                df.to_csv(CSV_PATH, index=False)
                st.success(f"Success! Added {len(new_entry_df)} record combinations to the database.")
                st.balloons()

                # ── Navigation Connection ─────────────────────────────────────────────
                # Direct the routing signal straight to the 'find' (tutor matching) screen
                st.session_state.page = 'find'
                st.rerun()