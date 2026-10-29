import pandas as pd
df = pd.read_excel("Halloween.xlsx", sheet_name=0)

names = {"luoyan": "L", "wenjin": "H", "yuanhao": "B", "tianyi": "T", "allen": "A"}

print(df.columns)
cols_as_arrays = {col: df[col].to_numpy() for col in df.columns}

start = cols_as_arrays["Start"].astype(str)
end = cols_as_arrays["End"].astype(str)
text = cols_as_arrays["Text"].astype(str)
person = cols_as_arrays["Person"].astype(str)
speaker = [len(person)] 

print(text[200])
print(person[200])
i = 500
str(speaker[i]) + ": " + text[i]

for i in person:
    if str(i).lower() in names.keys():
        speaker.append(names[str(i).lower()])
    else:
        speaker.append(str(i))

print(speaker)

import math
start_filtered = []
end_filtered = []
text_filtered = []
for i in range(len(text)):
    if len(str(text[i])) >= 2 and str(text[i]) != 'nan':
        start_filtered.append("00:" + start[i][:5] + "," + start[i][6:])
        end_filtered.append("00:" + end[i][:5] + "," + end[i][6:])
        if str(speaker[i]) != 'nan':
            text_filtered.append(str(speaker[i]) + ": " + text[i])
        else:
            text_filtered.append(text[i])


offset = 6
output_name = 'output'
vtt = False
if vtt:
    output_name += '.vtt'
else:
    output_name += '.srt'

with open(output_name, 'w',encoding="utf-8") as output_file:
    if vtt:
        output_file.write("WEBVTT\n\n")
    for i in range(len(text_filtered)):
        if not vtt:
            output_file.write(f"{i + offset + 1}\n")
        output_file.write(f"{start_filtered[i]} --> {end_filtered[i]}\n")
        output_file.write(f"{text_filtered[i]}\n\n")
