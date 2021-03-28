from PIL import Image
import json
import hashlib

img = Image.open(f"./ህ.png")


with open('./square_data.py', 'w') as square_data_file:
    square_data_file.write('SQUARE_IMG_DATA_HASH = "' + hashlib.md5(json.dumps(list(img.getdata())).encode()).hexdigest() + '"')


