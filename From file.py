import numpy as np
import os

def parse_entries(filename, vtt = False):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    entries = content.split("Set to current time\nAdd Line\nMerge Lines")
    results = []

    for entry in entries:
        lines = [line.strip() for line in entry.splitlines() if line.strip()]
        if len(lines) >= 7:
            start = f"{lines[0]}:{lines[3]},{lines[6]}"
            text = lines[9]
            end = f"{lines[10]}:{lines[13]},{lines[16]}"
            if vtt:
                results.append([start.replace(',','.'),text,end.replace(',','.')])
            else:
                results.append([start,text,end])

    return results

folder_dir = "Input text file"
entries = []
vtt = False
offset = 0

for filename in os.listdir(folder_dir):
    file_path = folder_dir + '/' + filename
    parsed_data = parse_entries(file_path, vtt)
    entries += parsed_data
    print(filename, len(parsed_data))

print(len(entries))

output_name = 'Output/output'
if vtt:
    output_name += '.vtt'
else:
    output_name += '.srt'
with open(output_name, 'w') as output_file:
    if vtt:
        output_file.write(f"{'WEBVTT'}\n\n")
    for i in range(len(entries)):
        if not vtt:
            output_file.write(f"{i + offset + 1}\n")
        output_file.write(f"00:{entries[i][0]} --> 00:{entries[i][2]}\n")
        output_file.write(f"{entries[i][1]}\n\n")
