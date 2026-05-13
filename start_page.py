import streamlit as st

# הגדרות דף - נקי ולבן לחלוטין
st.set_page_config(page_title="Learny", layout="wide")

# יצירת הסמל המדויק מ-Screenshot 2026-05-13 at 16.37.54.png באמצעות SVG
# זה קוד גרפי קטן שיוצר את ה"שמש" השחורה
logo_svg = """
<svg width="30" height="30" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
    <g transform="translate(50,50)">
        <path d="M0,-40 C10,-40 20,-30 20,-20 C20,-10 10,0 0,0 C-10,0 -20,-10 -20,-20 C-20,-30 -10,-40 0,-40" fill="black" transform="rotate(0)"/>
        <path d="M0,-40 C10,-40 20,-30 20,-20 C20,-10 10,0 0,0 C-10,0 -20,-10 -20,-20 C-20,-30 -10,-40 0,-40" fill="black" transform="rotate(45)"/>
        <path d="M0,-40 C10,-40 20,-30 20,-20 C20,-10 10,0 0,0 C-10,0 -20,-10 -20,-20 C-20,-30 -10,-40 0,-40" fill="black" transform="rotate(90)"/>
        <path d="M0,-40 C10,-40 20,-30 20,-20 C20,-10 10,0 0,0 C-10,0 -20,-10 -20,-20 C-20,-30 -10,-40 0,-40" fill="black" transform="rotate(135)"/>
        <path d="M0,-40 C10,-40 20,-30 20,-20 C20,-10 10,0 0,0 C-10,0 -20,-10 -20,-20 C-20,-30 -10,-40 0,-40" fill="black" transform="rotate(180)"/>
        <path d="M0,-40 C10,-40 20,-30 20,-20 C20,-10 10,0 0,0 C-10,0 -20,-10 -20,-20 C-20,-30 -10,-40 0,-40" fill="black" transform="rotate(225)"/>
        <path d="M0,-40 C10,-40 20,-30 20,-20 C20,-10 10,0 0,0 C-10,0 -20,-10 -20,-20 C-20,-30 -10,-40 0,-40" fill="black" transform="rotate(270)"/>
        <path d="M0,-40 C10,-40 20,-30 20,-20 C20,-10 10,0 0,0 C-10,0 -20,-10 -20,-20 C-20,-30 -10,-40 0,-40" fill="black" transform="rotate(315)"/>
    </g>
</svg>
"""

# עיצוב הכותרת העליונה - מוצמד לשמאל עם מסגרת עדינה
st.markdown(f"""
    <div style="display: flex; align-items: center; justify-content: flex-start; gap: 10px; padding: 5px; border: 1px dotted #ccc; width: fit-content;">
        {logo_svg}
        <h2 style="font-family: 'Times New Roman', Times, serif; margin: 0; font-size: 24px; font-weight: 400; color: black;">
            Learny <span style="font-size: 20px;">-The only way to learn</span>
        </h2>
    </div>
    <div style="margin-top: 10px; border-bottom: 2px solid #5abaff; width: 100%;"></div>
""", unsafe_allow_html=True)

# תוכן גוף הדף - נקי ולבן
st.write("##") # רווח
st.title("מערכת התאמת מורים אישית")
st.write("ברוכים הבאים! אנא בחרו את סוג הפעולה לביצוע.")

# כפתורים
col1, col2, _ = st.columns([1, 1, 3])

with col1:
    if st.button("כניסה (Sign In)", use_container_width=True):
        st.session_state.page = 'find'

with col2:
    if st.button("הרשמה (Sign Up)", use_container_width=True):
        st.session_state.page = 'input'

# קו תחתון עדין
st.markdown("<br><br><br><hr style='opacity: 0.2;'>", unsafe_allow_html=True)
st.caption("© 2026 Learny Educational Systems")