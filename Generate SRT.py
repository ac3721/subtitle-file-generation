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
debug = False
debug_words = False
check = False
folder_dir = "Test"
offset = 42

def numbers(image, array, count, i, debug = False):
    extracted_text = pytesseract.image_to_string(image)
    line = extracted_text.split('\n')
    if debug:
        print(line)

    pattern = r'^\d{2}:\d{2}\.\d{3}$'
    time = line[0]
    if len(time) > 0:
        time = time.replace(',','')
        if re.match(pattern, time):
            array.append(time.replace('.',','))
        else:
            digits_only = re.sub(r'[^0-9]', '', time)
            if len(digits_only) == 7:
                formatted = digits_only[:2] + ':' + digits_only[2:4] + ',' + digits_only[4:]
                array.append(formatted)
            elif len(digits_only) == 5:
                formatted = digits_only[:1] + ':' + digits_only[1:3] + ',' + digits_only[3:]
                array.append(formatted)
            else:
                array.append('*** ' + digits_only)
    else:
        count[i] += 1
        if count[i] > 1:
            array.append('******')
            count[i] = 0

def crop_image_to_boxes(image, box_height=50):
    width, height = image.size
    crops = []
    for top in range(0, height, box_height):
        bottom = min(top + box_height, height)
        crop_box = (0, top, width, bottom)
        cropped_img = image.crop(crop_box)
        crops.append(cropped_img)
    return crops

def single_run(image_path):
    base_image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    _, binary_image = cv2.threshold(base_image, 200, 255, cv2.THRESH_BINARY)

    image = Image.fromarray(binary_image)
    width, height = image.size

    # cv2.imshow('Binary Image', binary_image)
    scale_factor = 2
    resized_image = image.resize(
        (image.width * scale_factor, image.height * scale_factor),
        resample=Image.LANCZOS
    )
    # resized_image.show()

    left_box = (0, 0, box_width, height)
    middle_box = (box_width, 0, width - box_width - 1, height)
    right_box = (width - box_width, 0, width, height)

    left_section = image.crop(left_box)
    middle_section = image.crop(middle_box)
    right_section = image.crop(right_box) 
    count = [0, 0]

    if debug:
        left_section.show()
    left_boxes = crop_image_to_boxes(left_section, 50)
    for line_img in left_boxes:
        numbers(line_img, start, count, 0, debug)
    if check:
        print("start")
        print(start)

    if debug:
        right_section.show()
    right_boxes = crop_image_to_boxes(right_section, 50)
    for line_img in right_boxes:
        numbers(line_img, end, count,  1, debug)
                
    if check:
        print("end")
        print(end)

    config = '-l eng'
    all_text = pytesseract.image_to_string(middle_section, config=config)
    if debug_words:
        print(all_text)

    line = all_text.split('\n')
    for words in line:
        if len(words) > 0:
            words = words.replace('|', 'I')
            text.append(words)
    if check:
        print(text)

    if len(start) != len(end):
        if len(start) > len(end):
            start.remove('******')
        # for i in min(len(start), len(end)):

    elif len(start) > len(text):
        start.remove('******')
        end.remove('******')

    return len(start), len(end), len(text)
    
for image_name in os.listdir(folder_dir):
    image_path = folder_dir + '/' + image_name
    stats = single_run(image_path)
    print(image_name, stats)

with open('Output/output.srt', 'w') as output_file:
    for i in range(len(text)):
        output_file.write(f"{i + offset + 1}\n")
        output_file.write(f"00:{start[i]} --> 00:{end[i]}\n")
        output_file.write(f"{text[i]}\n\n")