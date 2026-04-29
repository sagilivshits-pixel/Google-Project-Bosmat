import pandas as pd

df = pd.read_csv('syn_data.csv')
c_row = 0
your_id = int(input("Enter your id: "))
my_rows =df[df['ID']==your_id]
max_rows = df.shape[0]
print(max_rows)
s=0
count = 0

my_rows =df[df['ID']==your_id]

if df .iloc[my_rows.index[0],2] == "Student":
    for s in my_rows.index:
        c_row = 0
        while c_row < max_rows:

            if df .iloc[s,2] == df.iloc[c_row, 2]:
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

