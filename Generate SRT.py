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
folder_dir = "Images"

def numbers(image, array):
    extracted_text = pytesseract.image_to_string(image)
    # print(extracted_text)
    line = extracted_text.split('\n')
    print(line)

    pattern = r'^\d{2}:\d{2}\.\d{3}$'
    for time in line:
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


for image_path in os.listdir(folder_dir):
    # image = Image.open(image_path)
    base_image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    _, binary_image = cv2.threshold(base_image, 200, 255, cv2.THRESH_BINARY)
    # kernel = np.ones((2,2), np.uint8)
    # thicker_text = cv2.erode(binary_image, kernel, iterations=1)

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

    left_section.show()
    print("start")
    numbers(left_section, start)
    print(start)
    print("end")
    numbers(right_section, end)
    print(end)

    config = '-l eng'
    all_text = pytesseract.image_to_string(middle_section, config=config)
    print(all_text)

    line = all_text.split('\n')
    for words in line:
        if len(words) > 0:
            words = words.replace('|', 'I')
            text.append(words)

with open('Output/output.srt', 'w') as output_file:
    for i in range(len(start)):
        output_file.write(f"{i+1}\n")
        output_file.write(f"00:{start[i]} --> 00:{end[i]}\n")
        output_file.write(f"{text[i]}\n\n")