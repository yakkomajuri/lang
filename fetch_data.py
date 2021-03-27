import requests
from locales import LOCALE_TO_LANGUAGE 


for locale in LOCALE_TO_LANGUAGE.keys():
    with open(f'raw_html/{locale}', 'x') as new_file:
        new_file.write(requests.get(f'https://policies.google.com/privacy?hl={locale}').text)

