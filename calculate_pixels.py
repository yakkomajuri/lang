import os
from operator import itemgetter
from PIL import Image, ImageDraw, ImageFont
from locales import LOCALE_TO_LANGUAGE 
import json

char_to_pixel_count = {}

def process_data():
    data = []
    data_file_list = os.listdir('./data')
    data_file_list_len = len(data_file_list)
    i = 0
    for file_name in data_file_list:
        print(f'Currently processing {file_name}: {i} of {data_file_list_len}')
        i += 1
        with open(f'./data/{file_name}', 'r') as data_file:
            text = data_file.read()
        data.append(
            {
                'pixels': count_pixels_in_text(text), 
                'chars': len(text), 
                'locale': file_name,
                'text': text
            }
        )
    
    output_file_content = 'Language,Locale,Total Pixels,Total Chars,Pixel/Char Ratio,Text\n'

    sorted_data = sorted(data, key=lambda dic: dic['pixels'])

    print('Generating CSV...')

    for row in sorted_data:
        language = LOCALE_TO_LANGUAGE[row['locale']]
        locale = row['locale']
        total_pixels = row['pixels']
        total_chars = row['chars']
        pixel_to_char_ratio = round(total_pixels/total_chars, 2)
        text = row['text']
        output_file_content += f'{language},{locale},{total_pixels},{total_chars},{pixel_to_char_ratio},{text}\n'
    
    with open('./results.csv', 'w') as output_file:
        output_file.write(output_file_content)

    with open('char_to_pixel.py', 'w') as mapping_file:
        mapping_file.write('PIXELS_PER_CHAR = ' + json.dumps(char_to_pixel_count))


def count_pixels_in_text(text):
    pixel_count = 0
    for char in text:
        if char in {'\s', '\n'}:
            pass
        elif char in char_to_pixel_count:
            pixel_count += char_to_pixel_count[char]
        else:
            char_px_count = count_black_pixels(draw_letter(char))
            char_to_pixel_count[char] = char_px_count
    return pixel_count




def draw_letter(letter, save=True):
    try:
        return Image.open(f"{letter}.png")
    except:
        pass
    
    arial_unicode = ImageFont.truetype('/Library/Fonts/Arial Unicode.ttf', 100)
    img = Image.new('RGB', (200, 200), 'white')

    draw = ImageDraw.Draw(img)
    draw.text((0,0), letter, font=arial_unicode, fill='#000000')

    if save:
        img.save("imgs/{}.png".format(letter), 'PNG')

    return img


def count_black_pixels(img):
    pixels = list(img.getdata())
    return len(list(filter(lambda rgb: sum(rgb) == 0, pixels)))


process_data()

# http://alexmic.net/letter-pixel-count/