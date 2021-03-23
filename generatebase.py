import requests
import json
from alive_progress import alive_bar

# coming-soon-series

def GetSets():
    sets = []
    data = requests.request('GET', "https://www.neonmob.com/api/setts/legacy_list/?category=&release_date=asc&page=1").json()
    # https://www.neonmob.com/api/setts/legacy_list/?category=&release_date=asc&page=1
    total = data['count']

    with alive_bar(total, bar='smooth', spinner='dots_recur') as bar:
        while True:
            nxt = data['next']
            for set in data['results']:
                sets.append({'id': set['id'],
                            'name': set['name'],
                            'name_slug': set['name_slug'],
                            'creator': {'username': set['creator']['username'],
                                        'name': set['creator']['name']},
                            'description': set['description'],
                            'edition_size': set['edition_size'],
                            'difficulty': set['difficulty']['name']})
                bar()
            # other bar stuff
            if not nxt:
                break # pass
            data = requests.request('GET', nxt).json()
    return sets

def main():
    sets = GetSets()
    with open('all-sets.json', 'w') as f:
        json.dump(sets, f)

if __name__ == "__main__":
    main()