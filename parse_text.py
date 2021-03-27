import os
from bs4 import BeautifulSoup

for file_name in os.listdir('./raw_html'):
    with open(f'./raw_html/{file_name}', 'r') as html_file:
        soup = BeautifulSoup(html_file.read(), "html.parser")
    text = ''
    for p in soup.select("div.nrAB0c.KMMDve > p"):
        text += p.get_text()

    with open(f'./data/{file_name}', 'x') as output_file:
        output_file.write(text)
    