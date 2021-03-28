from char_to_pixel import PIXELS_PER_CHAR

output = 'Character,Number Of Black Pixels\n'
for char, pixels in sorted(PIXELS_PER_CHAR.items(), key=lambda item: item[1]):
    output += f'"{char}",{pixels}\n'

with open('./char_to_pixels.csv', 'w') as output_file:
    output_file.write(output)