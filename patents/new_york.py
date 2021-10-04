import requests
import warnings
import random
import json

from . import justia

def get_cases(page):
    return justia.get_cases(page, state='new_york')

def get_inc_records(name):
    url = 'https://apps.dos.ny.gov/PublicInquiryWeb/api/PublicInquiry/GetComplexSearchMatchingEntities'

    headers = {
        'User-Agent': ''.join(random.sample('abcdefghijklmnopqrstuvwxyz', 10)),
        'Content-Type': 'application/json',
    }

    payload = {
        'entityStatusIndicator': 'AllStatuses',
        'entityTypeIndicator': ['Corporation', 'LimitedLiabilityCompany', 'LimitedPartnership', 'LimitedLiabilityPartnership'],
        'listPaginationInfo': {
            'listStartRecord': 1,
            'listEndRecord': 50,
        },
        'searchByTypeIndicator': 'EntityName',
        'searchExpressionIndicator': 'Contains',
        'searchValue': name.replace(' et al.', ''),
    }

    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        response = requests.post(url, data=json.dumps(payload), headers=headers, verify=False)

    entities = response.json()['entitySearchResultList']

    if len(entities):
        return [{
            'name': entity['entityName'].replace(',', '').replace('.', ''),
            'jurisdiction': entity['jurisdiction'].replace(', USA', ''),
            'year': entity['initialFilingDate'][:4],
        } for entity in entities]

    return []

def get_matching_record(name):
    entities =  get_inc_records(name)
        
    if entities:
        for entity in entities:
            if entity['name'] == name.upper().replace(',', '').replace('.', ''):
                return entity

    return ''