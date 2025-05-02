import json
from pymongo import MongoClient
from random import randint
from tqdm import tqdm

scopus_id = "ScopusID"
Categories = "Categories"

def read_json(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return None

def get_distance(point_x: dict, point_y: dict):
    distance = 0
    for key in point_x:
        if key not in point_y:
            return float("inf")
        distance += (point_x[key] - point_y[key])**2
    return distance**0.5

def calculate_closest(data, coauthors):
    result = []
    for a in tqdm(data):
        a_scopus_id = a[scopus_id]
        a_Categories = a[Categories]
        others = []
        for b in data:
            if b[scopus_id] != a_scopus_id:
                b_scopus_id = b[scopus_id]
                b_Categories = b[Categories]
                distance = get_distance(a_Categories, b_Categories)
                others.append({
                    "scopus_id": b_scopus_id,
                    "distance": round(distance, 2),
                    "common": coauthors.get(a_scopus_id, {}).get(b_scopus_id, 0)
                })

        others_sorted = sorted(others, key=lambda x: x["distance"])[:100]
        result.append({
            "scopus_id": a_scopus_id,
            "closest": others_sorted
        })
    return result

def main():
    # client, db, collection - из .env
    client = MongoClient()
    db = client.get_database('polygon')
    collection_p = db.get_collection('people')
    collection_p.drop()
    collection_c = db.get_collection('closest')
    people = read_json('authors.json')
    people = [human for human in people if sum(human[Categories].values()) > 0.3]
    authors = read_json('authors_co.json')
    coauthors = {}
    for author in tqdm(authors):
        author_id = author[scopus_id]
        coauthors[author_id] = {}
        for nb in author["Connected"]:
            coauthors[author_id][nb["ScopusID"]] = nb["common"]

    collection_p.insert_many(people)
    closest = calculate_closest(people, coauthors)
    collection_c.insert_many(closest)

if __name__ == '__main__':
    main()
