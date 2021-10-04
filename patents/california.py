import requests
import warnings
import random
import re

from . import justia

def get_cases(page):
    return justia.get_cases(page, state='california')

def get_inc_records(name):
    url = f'https://businesssearch.sos.ca.gov/CBS/SearchResults?filing=&SearchType=CORP&SearchCriteria={name}&SearchSubType=Keyword'

    headers = {
        'User-Agent': ''.join(random.sample('abcdefghijklmnopqrstuvwxyz', 10)),
    }

    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        response = requests.post(url, headers=headers, verify=False)

    content = re.sub(' + +', ' ', response.content.decode('utf-8').replace('\n', ' ').replace('\r', ' '))
    entities = re.findall('<td.*?>(.+?)</td>', content)
    entities = [entities[i:i+6] for i in range(0, len(entities), 6)]

    if entities:
        return [{
            'name': re.findall(' name="EntityId" class="btn-link EntityLink">(.+?)</button>', entity[3])[0].replace(',', '').replace('.', ''),
            'jurisdiction': entity[4][1:-1],
            'year': entity[1][7:11],
        } for entity in entities]

    else:
        return []


def get_matching_record(name):
    entities = get_inc_records(name)

    if entities:
        for entity in entities:
            if entity['name'] == name.upper().replace(',', '').replace('.', ''):
                return entity

    return ''


