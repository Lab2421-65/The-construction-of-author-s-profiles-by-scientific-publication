from pymongo import MongoClient
from random import shuffle
import json


client = MongoClient()
db = client.get_database('polygon')
collection_p = db.get_collection('people')
collection_c = db.get_collection('closest')
field = 'Categories.Nuclear and High Energy Physics'

def get_data():
    """Получение всех данных без id"""
    return list(collection_p.find({}, {'_id': 0}))

def get_by_name(name: str, many=False) -> dict:
    if many:
        item = list(collection_p.find({'author_name': name}, {'_id': 0}))[0]
    else:
        item = collection_p.find_one({'author_name': name}, {'_id': 0})
    return item

def get_by_scopus_id(scopus_id: str) -> dict:
    if not scopus_id:
        return {}
    return collection_p.find_one({'ScopusID': scopus_id}, {'_id': 0})

def get_batch(page:int=1, page_size: int=10):
    return list(collection_p.find({}, {'_id': 0}).sort({field: -1}).skip(page_size * (page - 1)).limit(page_size))

def get_by_orcid(orcid: str) -> dict:
    if not orcid:
        return {}
    return collection_p.find_one({'ORCID': orcid}, {'_id': 0})

def get_author_name(scopus_id: str) -> str:
    return collection_p.find_one({'ScopusID': scopus_id}, {'name': 1, '_id': 0}).get('author_name', '')

def get_closest(scopus_id: str, top: int=5):
    if not scopus_id:
        return {}
    item = collection_c.find_one({'ScopusID': scopus_id}, {'_id': 0})
    size = min(len(item.get('Connected')), top)
    items = item.get('Connected', [])[:size]
    for i in range(len(items)):
        items[i]['author_name'] = get_author_name(items[i]['ScopusID'])
        print(items[i]['author_name'])
    return items


def make_result():
    database = client.get_database('polygon')
    history = database.get_collection('peopl')
    org = database.get_collection('Organization')
    orgs = {str(item['_id']): item['name_en'] for item in org.find()}
    print(orgs)
    result = []
    for item in history.find():
        org_id = item['org_id']
        result.append({'aff': item.get('org'), 'org': orgs[str(org_id)]})
    
    shuffle(result)
    with open('modelling.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

print(get_by_scopus_id('57193414565').get('Categories', {}).items())
