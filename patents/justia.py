import requests
import warnings
import random
import re

def get_cases(page, state=False):
    '''
    Get case records from Justia dockets.
    '''
    if state:
        url = f'https://dockets.justia.com/browse/state-{state}/noscat-10/nos-830?page={str(page)}'

    else:
        url = f'https://dockets.justia.com/browse/noscat-10?page={str(page)}'

    headers = {
        'User-Agent': ''.join(random.sample('abcdefghijklmnopqrstuvwxyz', 10))
    }

    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        response = requests.get(url, verify=False, headers=headers)

    cases = [case.split(' v. ') for case in re.findall('class="case-name"><strong>(.+?)<\/strong><\/a>', response.content.decode('utf-8'))]

    return cases
