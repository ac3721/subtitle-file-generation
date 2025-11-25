import numpy as np
import os

def parse_entries(filename, vtt = False):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    entries = content.split("Set to current time\nAdd Line\nMerge Lines")
    results = []

    for entry in entries:
        lines = [line.strip() for line in entry.splitlines() if line.strip()]
        print(lines)
        if len(lines) >= 7:
            index = lines.index('Set to current time')
            start = f"{lines[index-8]}:{lines[index-5]},{lines[index-2]}"
            lines = lines[(index+1):]
            print("second\n", lines)
            second_index = lines.index(':')
            text = lines[:(second_index - 2)]
            end = f"{lines[second_index - 2]}:{lines[second_index + 1]},{lines[second_index + 4]}"
            if len(text) > 1:
                combined = [""]
                for line in text:
                    combined[0] += line + '\n'
                print (combined[0])
                text = combined[0][:len(combined[0])-1]     
            else:
                text = text[0]
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
