import pandas as pd
import json
def find_a_match():
    df = pd.read_csv('syn_data.csv')
    c_row = 0
    max_rows = df.shape[0]
    print(max_rows)
    only_ids = df['ID'].unique().tolist()
    matches_dict = {}
    for your_id in only_ids:
        my_rows = df[df['ID'] == your_id]
        if df.iloc[my_rows.index[0], 2] == "Student":
            current_student_id = str(your_id)
            matches_dict[current_student_id] = []
            for s in my_rows.index:
                c_row = 0
                while c_row < max_rows:

                    if df.iloc[s, 2] == df.iloc[c_row, 2]:
                        c_row += 1

                    else:
                        if df.iloc[s, 3:7].tolist() == df.iloc[c_row, 3:7].tolist():
                            if df.iloc[s, 3:7].tolist() == df.iloc[c_row, 3:7].tolist():
                                tutor_details = {
                                    "Name": df.iloc[c_row, 1],
                                    "Phone": df.iloc[c_row, 7],
                                    "Day": df.iloc[c_row, 5],
                                    "Hour": df.iloc[c_row, 6],
                                    "Subject" : df.iloc[c_row, 3]
                                }

                                # שימוש באותו שם משתנה בדיוק (current_student_id)
                                if tutor_details not in matches_dict[current_student_id]:
                                    matches_dict[current_student_id].append(tutor_details)
                            print("match found for you", df.iloc[s,0], "your match is:", df.iloc[c_row, 1])
                            c_row += 1
                        else:
                            c_row += 1

        else:
            print("your a Tutor" ,df.iloc[my_rows.index[0], 1])

    with open('student_matches_detailed.json', 'w', encoding='utf-8') as f:
        json.dump(matches_dict, f, ensure_ascii=False, indent=4)
    print("\n--- הסתיים! הקובץ tutor_matches.json נשמר בתיקייה שלך ---")
find_a_match()