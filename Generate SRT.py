from PIL import Image
import numpy as np
import pytesseract
import cv2
import os
import re

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

box_width = 78
start = []
end = []
text = []
time_stamp = []
debug = False
debug_words = False
check = True
folder_dir = "Images"
offset = 0
vtt = True

def timestamp(image, debug = False):
    stamp = None
    extracted_text = pytesseract.image_to_string(image)
    line = extracted_text.split('\n')
    if debug:
        print(line)

    pattern = r'^\d{2}:\d{2}\.\d{3}$'
    time = line[0]
    if len(time) > 0:
        time = time.replace(',','')
        if re.match(pattern, time):
            stamp = time.replace('.',',')
        else:
            digits_only = re.sub(r'[^0-9]', '', time)
            if len(digits_only) == 7:
                stamp = digits_only[:2] + ':' + digits_only[2:4] + ',' + digits_only[4:]
            elif len(digits_only) == 5:
                stamp = digits_only[:1] + ':' + digits_only[1:3] + ',' + digits_only[3:] + '0**'
            elif len(digits_only) > 5:
                stamp = digits_only[:2] + ':' + digits_only[2:4] + ',' + digits_only[4:] + '**'
            else:
                stamp = '*** ' + digits_only
    else:
        stamp = '******'

    if vtt:
        stamp = stamp.replace(',','.')
    return stamp

def crop_image_around_text_lines(image, base_image, pad_extra=10, min_gap=5):    
    if base_image.ndim == 3:
        gray = np.mean(base_image, axis=2).astype(np.uint8)
    else:
        gray = base_image

    projection = np.sum(255 - gray, axis=1)
    threshold = np.max(projection) * 0.2

    row_has_text = projection > threshold
    lines = []
    in_line = False
    for i, has_text in enumerate(row_has_text):
        if has_text and not in_line:
            start = i
            in_line = True
        elif not has_text and in_line:
            end = i
            in_line = False
            lines.append((start, end))
    if in_line:
        lines.append((start, len(row_has_text)))
    
    merged_lines = []
    for line in lines:
        if not merged_lines or line[0] > merged_lines[-1][1] + min_gap:
            merged_lines.append(line)
        else:
            merged_lines[-1] = (merged_lines[-1][0], line[1])

    crops = []
    for start, end in merged_lines:
        center = (start + end) // 2
        height = end - start
        pad = height // 2 + pad_extra
        top = max(center - pad, 0)
        bottom = min(center + pad, image.size[1])
        crop_box = (0, top, image.size[0], bottom)
        crops.append(image.crop(crop_box))
    return crops

def single_run(image_path):
    base_image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    _, binary_image = cv2.threshold(base_image, 200, 255, cv2.THRESH_BINARY)

    image = Image.fromarray(binary_image)

    # cv2.imshow('Binary Image', binary_image)
    scale_factor = 2
    resized_image = image.resize(
        (image.width * scale_factor, image.height * scale_factor),
        resample=Image.LANCZOS
    )

    boxes = crop_image_around_text_lines(image, base_image)

    for line_img in boxes:
        # line_img.show()
        width, height = line_img.size
        left_box = (0, 0, box_width, height)
        middle_box = (box_width, 0, width - box_width - 1, height)
        right_box = (width - box_width, 0, width, height)

        left_section = line_img.crop(left_box)
        middle_section = line_img.crop(middle_box)
        right_section = line_img.crop(right_box) 

        if debug:
            left_section.show()
        start_stamp = timestamp(left_section, debug)
        if check:
            print("start", start_stamp)

        if debug:
            right_section.show()
        end_stamp = timestamp(right_section, debug)       
        if check:
            print("end", end_stamp)

        extracted_text = pytesseract.image_to_string(middle_section, config='psm 7 -l eng')
        if debug_words:
            print(extracted_text)
        line_text = extracted_text.split('\n')[0].replace('|', 'I')
        if check:
            print(line_text)

        if re.sub(r'[^0-9]', '', start_stamp) > re.sub(r'[^0-9]', '', end_stamp):
            stamp = "00:" + start_stamp +' --> 00:' + end_stamp + '&&'
        else:
            stamp = "00:" + start_stamp +' --> 00:' + end_stamp

        if len(line_text) != 0 or start_stamp != '******' or end_stamp != '******':
            start.append(start_stamp)
            end.append(end_stamp)
            text.append(line_text)
            time_stamp.append(stamp)

    return len(start), len(end), len(text), len(boxes)
    
for image_name in os.listdir(folder_dir):
    image_path = folder_dir + '/' + image_name
    stats = single_run(image_path)
    print(image_name, stats)

output_name = 'Output/output'
if vtt:
    output_name += '.vtt'
else:
    output_name += '.srt'
with open(output_name, 'w') as output_file:
    if vtt:
        output_file.write(f"{'WEBVTT'}\n\n")
    for i in range(len(text)):
        if not vtt:
            output_file.write(f"{i + offset + 1}\n")
        output_file.write(f"00:{start[i]} --> 00:{end[i]}\n")
        output_file.write(f"{text[i]}\n\n")