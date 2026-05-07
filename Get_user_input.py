import pandas as pd
import json
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
print("\n─── Add New Entry ───────────────────────────")

entry = {
    "ID":              get_input("ID: "),
    "Name":            get_input("Full name: "),
    "Tutor / Student": get_input("Role [Tutor/Student]: ", ["Tutor", "Student"]),
    "Subject":         get_input("Subject [Math/English/Physics/Biology/Chemistry/History/Computer Science]: ",
                                  ["Math", "English", "Physics", "Biology", "Chemistry", "History", "Computer Science"]),
    "Online / F2F":    get_input("Session type [Online/F2F]: ", ["Online", "F2F"]),
    "Day":             get_input("Day [Monday/Tuesday/Wednesday/Thursday/Friday/Saturday/Sunday]: ",
                                  ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]),
    "Hour":            get_input("Hour (e.g. 09:00): "),
    "Phone number":    get_input("Phone number (e.g. 555-1234): "),
}

# ── Append to CSV ─────────────────────────────────────────────────────────────
try:
    df = pd.read_csv(CSV_PATH, dtype={"ID": str, "Phone number": str})
    df = pd.concat([df, pd.DataFrame([entry])], ignore_index=True)
except FileNotFoundError:
    df = pd.DataFrame([entry])

df.to_csv(CSV_PATH, index=False)
print(f"✓ CSV saved!  ({len(df)} rows)")


if df.iloc[my_rows.index[0], 2] == "Student":
    for s in my_rows.index:
        c_row = 0
        while c_row < max_rows:

            if df.iloc[s, 2] == df.iloc[c_row, 2]:
                c_row += 1

            else:
                if df.iloc[s, 3:7].tolist() == df.iloc[c_row, 3:7].tolist():
                    print("match found")
                    print(df.iloc[c_row])
                    c_row += 1
                else:
                    c_row += 1

else:
    print("your a Tutor")
    