import numpy as np
import os

def parse_entries(filename, vtt = False):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    entries = content.split("Add Line\nMerge Lines")
    results = []

    for entry in entries:
        lines = [line.strip() for line in entry.splitlines() if line.strip()]
        if len(lines) >= 16:
            index = lines.index('Set to current time')
            start = f"{lines[index-8]}:{lines[index-5]},{lines[index-2]}"
            lines = lines[(index+1):]
            second_index = lines.index(':')
            text = lines[:(second_index - 2)]
            end = f"{lines[second_index - 2]}:{lines[second_index + 1]},{lines[second_index + 4]}"
            if len(text) > 1:
                combined = [""]
                for line in text:
                    combined[0] += line + '\n'
                text = combined[0][:len(combined[0])-1]     
            else:
                if len(text)==0:
                    print(start, end, filename)
                else:
                    text = text[0]
            if vtt:
                results.append([start.replace(',','.'),text,end.replace(',','.')])
            else:
                results.append([start,text,end])

    return results

folder_dir = "Input text file"
entries = set()
vtt = False
offset = 0

input = os.listdir(folder_dir)
input.remove('example.txt')
for filename in input:
    file_path = folder_dir + '/' + filename
    parsed_data = parse_entries(file_path, vtt)
    entries.update(tuple(entry) for entry in parsed_data)
    print(filename, len(parsed_data))

print(len(entries))

output_name = 'Output/output'
if vtt:
    output_name += '.vtt'
else:
    output_name += '.srt'

entries_list = sorted(entries, key=lambda x: x[0])
with open(output_name, 'w',encoding="utf-8") as output_file:
    if vtt:
        output_file.write("WEBVTT\n\n")
    for i, entry in enumerate(entries_list):
        if not vtt:
            output_file.write(f"{i + offset + 1}\n")
        output_file.write(f"00:{entry[0]} --> 00:{entry[2]}\n")
        output_file.write(f"{entry[1]}\n\n")
