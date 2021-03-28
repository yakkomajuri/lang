import os
from operator import itemgetter
from PIL import Image, ImageDraw, ImageFont
from locales import LOCALE_TO_LANGUAGE 
from char_to_pixel import PIXELS_PER_CHAR
import json

STR_VALUES_FOR_TRUE =  { '1', 'true', 'True' }

USE_CACHE = 'USE_CACHE' in os.environ and os.environ['USE_CACHE'] in STR_VALUES_FOR_TRUE
REGENERATE_IMAGES = 'REGENERATE_IMAGES' in os.environ and os.environ['REGENERATE_IMAGES'] in STR_VALUES_FOR_TRUE

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

        # Google returns a policy in English if they don't have a translation for the locale
        if file_name[:2] != 'en' and 'When you use our services, you’re trusting us with your information.' in text:
            continue

        pixels, spaces = count_pixels_in_text(text)
        data.append(
            {
                'pixels': pixels, 
                'chars': len(text), 
                'locale': file_name,
                'text': text,
                'spaces': spaces
            }
        )
    
    output_file_content = 'Language,Locale,Total Pixels,Total Chars,Avg. (Mean) Pixels Per Char,Total Spaces,Text\n'

    sorted_data = sorted(data, key=lambda dic: dic['pixels'])

    print('Generating CSV...')

    for row in sorted_data:
        language = LOCALE_TO_LANGUAGE[row['locale']]
        locale = row['locale']
        total_pixels = row['pixels']
        total_chars = row['chars']
        pixel_to_char_ratio = round(total_pixels/total_chars, 2)
        text = row['text']
        spaces = row['spaces']
        output_file_content += f'"{language}","{locale}",{total_pixels},{total_chars},{pixel_to_char_ratio},{spaces},"{text}"\n'
    
    
    with open('./results.csv', 'w') as output_file:
        output_file.write(output_file_content)

    with open('char_to_pixel.py', 'w') as mapping_file:
        cache = PIXELS_PER_CHAR if USE_CACHE else char_to_pixel_count
        mapping_file.write('PIXELS_PER_CHAR = ' + json.dumps(cache))


def count_pixels_in_text(text):
    pixel_count = 0
    spaces = 0
    for char in text:
        if char == '\n':
            continue
        if char == ' ':
            spaces += 1
            continue
        
        if USE_CACHE:
            pixel_count += PIXELS_PER_CHAR[char]
            continue

        if char in char_to_pixel_count:
            pixel_count += char_to_pixel_count[char]
        else:
            char_px_count = count_black_pixels(draw_letter(char))
            char_to_pixel_count[char] = char_px_count
            pixel_count += char_px_count



    return pixel_count, spaces



def draw_letter(letter, save=True):
    if not REGENERATE_IMAGES:
        if f"{letter}.png" in os.listdir('./imgs'):
            return Image.open(f"./imgs/{letter}.png")


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
