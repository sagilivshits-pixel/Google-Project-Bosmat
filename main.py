import pandas as pd

def find_a_match():
    df = pd.read_csv('syn_data.csv')
    c_row = 0
    max_rows = df.shape[0]
    print(max_rows)
    only_ids = df['ID'].unique().tolist()
    for your_id in only_ids:
        my_rows = df[df['ID'] == your_id]
        if df.iloc[my_rows.index[0], 2] == "Student":
            for s in my_rows.index:
                c_row = 0
                while c_row < max_rows:

                    if df.iloc[s, 2] == df.iloc[c_row, 2]:
                        c_row += 1

                    else:
                        if df.iloc[s, 3:7].tolist() == df.iloc[c_row, 3:7].tolist():
                            print("match found for you", df.iloc[s,0], "your match is:", df.iloc[c_row, 1])
                            c_row += 1
                        else:
                            c_row += 1

        else:
            print("your a Tutor" ,df.iloc[my_rows.index[0], 1])
find_a_match()