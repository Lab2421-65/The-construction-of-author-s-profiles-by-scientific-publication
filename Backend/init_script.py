import json
from pymongo import MongoClient
from random import randint


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

def calculate_closest(data):
    result = []
    for k,a in enumerate(data):
        a_ScopusID = a["ScopusID"]
        a_Categories = a["Categories"]
        others = []
        for b in data:
            if b["ScopusID"] != a_ScopusID:
                b_ScopusID = b["ScopusID"]
                b_Categories = b["Categories"]
                distance = get_distance(a_Categories, b_Categories)
                others.append({
                    "ScopusID": b_ScopusID,
                    "distance": round(distance, 2),
                })

        others_sorted = sorted(others, key=lambda x: x["distance"])

        result.append({
            "Name": a['author_name'],
            "ScopusID": a_ScopusID,
            "closest": others_sorted
        })
        print(k)
    return result

def main():
    # client, db, collection - из .env
    client = MongoClient()
    db = client.get_database('polygon')
    collection_p = db.get_collection('people')
    collection_p.drop()
    collection_c = db.get_collection('closest')
    people = read_json(r'C:\Users\user\Desktop\JINR\Output_normalization_4.json')
    collection_p.insert_many(people)
    closest = calculate_closest(people)
    collection_c.insert_many(closest)

if __name__ == '__main__':
    main()
