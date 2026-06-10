import pandas as pd
import datetime
import streamlit as st
import hashlib
import os


def get_user_input():
    CSV_PATH = "syn_data.csv"

    # ── מילוני תרגום (Mapping): תצוגה בעברית -> שמירה באנגלית ב-CSV ──
    role_map = {
        "תלמיד": "Student",
        "מורה": "Tutor"
    }

    subject_map = {
        "מתמטיקה": "Math",
        "אנגלית": "English",
        "פיזיקה": "Physics",
        "ביולוגיה": "Biology",
        "כימיה": "Chemistry",
        "היסטוריה": "History",
        "מדעי המחשב": "Computer Science"
    }

    modality_map = {
        "מקוון (אונליין)": "Online",
        "פרונטלי (פנים אל פנים)": "F2F"
    }

    day_map = {
        "יום ראשון": "Sunday",
        "יום שני": "Monday",
        "יום שלישי": "Tuesday",
        "יום רביעי": "Wednesday",
        "יום חמישי": "Thursday",
        "יום שישי": "Friday",
        "יום שבת": "Saturday"
    }

    # ── הזרקת CSS מתוקן - ללא פגיעה בתיבות ההקלדה ──────────────────
    st.markdown("""
            <style>
            /* 1. הקופסה הלבנה */
            div[data-testid*="olumn"]:nth-child(2) > div {
                background-color: #FFFFFF !important;
                background: #FFFFFF !important;
                opacity: 1 !important;
                padding: 2.5rem !important;
                border-radius: 16px !important;
                box-shadow: 0px 12px 35px rgba(0,0,0,0.08) !important;
                border: 1px solid #EAEAEA !important;
            }

            /* 2. מניעת כפילות רקעים בתוך הקופסה */
            div[data-testid="stVerticalBlockBorderWrapper"], 
            div[data-testid="stForm"] {
                background-color: transparent !important;
                background: transparent !important;
                border: none !important;
                padding: 0 !important;
            }

            /* 🌟 התיקון: הגדלת התוויות (Labels) שמעל השדות והכפתורים *בלבד*! 
               זה מבטיח שהטקסט בתוך התיבה עצמה יישאר בגודל הסטנדרטי ולא ייחתך 🌟 */
            div[data-testid*="olumn"]:nth-child(2) label p,
            div[data-testid*="olumn"]:nth-child(2) button p,
            div[data-testid*="olumn"]:nth-child(2) button {
                color: #262730 !important;
                font-size: 1.15rem !important;
            }

            /* 3. הגדלת הכותרות של השלבים (H3) */
            div[data-testid*="olumn"]:nth-child(2) h3 {
                font-size: 1.8rem !important;
                color: #1f1f1f !important;
            }
            </style>
        """, unsafe_allow_html=True)

    # ניהול סטייט להרשמה
    if "id_verified" not in st.session_state:
        st.session_state.id_verified = False
    if "verified_id" not in st.session_state:
        st.session_state.verified_id = ""

    # מרכז את הטופס על המסך (עמודות [1, 4, 1])
    _, center_col, _ = st.columns([1, 4, 1])

    with center_col:
        # --- שלב 1: בדיקת תעודת זהות ---
        if not st.session_state.id_verified:
            with st.container(border=True):
                st.subheader("שלב 1: אימות משתמש")
                with st.form(key="id_verification_form"):
                    id_input = st.text_input("הכנס תעודת זהות (9 ספרות):")
                    submit_id = st.form_submit_button("המשך להרשמה")

                    if submit_id:
                        if not id_input or len(id_input) < 9:
                            st.error("אנא הכנס תעודת זהות תקינה (9 ספרות)")
                        else:
                            if os.path.exists(CSV_PATH):
                                df_existing = pd.read_csv(CSV_PATH, dtype={"ID": str})
                                if id_input in df_existing["ID"].values:
                                    st.error("המשתמש כבר קיים במערכת, אנא עבור לדף התחברות")
                                    return

                            st.session_state.verified_id = id_input
                            st.session_state.id_verified = True
                            st.rerun()

        # --- שלב 2: מילוי פרטים מלא בעברית ---
        else:
            with st.container(border=True):
                st.success(f"מזהה מאומת: {st.session_state.verified_id}")
                st.subheader("שלב 2: מילוי פרטים אישיים")

                password_raw = st.text_input("בחר סיסמה:", type="password")
                name = st.text_input("שם מלא:")
                phone = st.text_input("מספר טלפון:")

                # בחירות בעברית
                role_ui = st.selectbox("תפקיד:", list(role_map.keys()))

                st.divider()

                subjects_ui = st.multiselect("מקצועות לימוד:", list(subject_map.keys()))
                modality_ui = st.selectbox("אופן לימוד:", list(modality_map.keys()))

                st.write("זמינות:")
                days_ui = st.multiselect("ימים:", list(day_map.keys()))

                # מילוי שעות דינמי לכל יום שנבחר בעברית
                hours_list = []
                if days_ui:
                    st.write("הגדר שעות לימים שנבחרו:")
                    for day_hebrew in days_ui:
                        chosen_time = st.time_input(f"בחר שעה עבור {day_hebrew}", datetime.time(19, 0),
                                                    key=f"time_{day_hebrew}")
                        hours_list.append(chosen_time.strftime("%H:%M"))

                st.divider()
                submit_all = st.button("סיום הרשמה ושמירה")

                if submit_all:
                    if not name or not password_raw or not subjects_ui or not days_ui:
                        st.error("חובה למלא את כל השדות ולבחור לפחות מקצוע אחד ויום אחד.")
                    else:
                        pwd_hash = hashlib.sha256(password_raw.encode()).hexdigest()

                        # התרגום השקט לאנגלית
                        role = role_map[role_ui]
                        subjects = [subject_map[s] for s in subjects_ui]
                        modality = modality_map[modality_ui]
                        days = [day_map[d] for d in days_ui]

                        new_entry = {
                            "Pass": [pwd_hash],
                            "ID": [st.session_state.verified_id],
                            "Name": [name],
                            "Tutor / Student": [role],
                            "Subject": [subjects],
                            "Online / F2F": [modality],
                            "Day": [days],
                            "Hour": [hours_list],
                            "Phone number": [phone]
                        }

                        new_entry_df = pd.DataFrame(new_entry)
                        new_entry_df = new_entry_df.explode('Subject')
                        new_entry_df = new_entry_df.explode(['Day', 'Hour'])

                        try:
                            df_existing = pd.read_csv(CSV_PATH, dtype={"ID": str, "Phone number": str})
                            df_final = pd.concat([df_existing, new_entry_df], ignore_index=True)
                        except FileNotFoundError:
                            df_final = new_entry_df

                        df_final.to_csv(CSV_PATH, index=False)

                        st.success("ההרשמה בוצעה בהצלחה!")
                        st.balloons()

                        temp_id = st.session_state.verified_id
                        st.session_state.id_verified = False
                        st.session_state.verified_id = ""
                        st.session_state.user_id = temp_id

                        # ניתוב לפי התפקיד
                        if role == "Student":
                            st.session_state.page = 'find'
                        else:
                            st.session_state.page = 'Tutor_page'

                        st.rerun()