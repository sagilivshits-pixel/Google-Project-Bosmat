import pandas as pd
import json
import datetime
import streamlit as st
df = pd.read_csv('syn_data.csv')
CSV_PATH  = "syn_data.csv"   # update path if needed

max_rows = df.shape[0]
def get_input(prompt, valid_options=None):
    while True:
        value = input(prompt).strip()
        if valid_options:
            if value.lower() in [v.lower() for v in valid_options]:
                return valid_options[[v.lower() for v in valid_options].index(value.lower())]
            print(f"  Choose from: {', '.join(valid_options)}")
        elif value:
            return value
        else:
            print("  This field cannot be empty.")

# ── Collect input ─────────────────────────────────────────────────────────────
st.title("entry")
with st.form("entry_form"):
    entry = {
        "ID":              st.text_input("Enter ID :"),
        "Name":            st.text_input("Enter your name :"),
        "Tutor / Student": st.selectbox("what are you?",["Tutor","Student"]),
        "Subject":         st.multiselect("Select your subjects", ["Math", "English", "Physics", "Biology", "Chemistry", "History", "Computer Science"]),
        "Online / F2F":    st.selectbox("Face to face or online?",["Online","F2F"]),
        "Day":             st.multiselect("select the days", ["sunday","monday","tuesday","Wednesday","thursday","friday","saturday"]),
        "Hour":            st.time_input('Select an hour', datetime.time(19, 0)),
        "Phone number":    st.text_input("phone number :"),
    }
    submitted = st.form_submit_button("Save Entry")
# ── Append to CSV ─────────────────────────────────────────────────────────────
if submitted:
    try:
        df = pd.read_csv(CSV_PATH, dtype={"ID": str, "Phone number": str})
        df = pd.concat([df, pd.DataFrame([entry])], ignore_index=True)
    except FileNotFoundError:
        df = pd.DataFrame([entry])

    df.to_csv(CSV_PATH, index=False)
    print(f"✓ CSV saved!  ({len(df)} rows)")
    st.success(f"CSV saved!  ({len(df)} rows)")
    st.balloons()


