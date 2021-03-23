import requests
import json
from alive_progress import alive_bar
from timeit import default_timer as timer

def GetUpcomingSets():
    sets = []
    data = requests.request('GET', "https://www.neonmob.com/api/setts/legacy_list/?category=coming-soon-series&release_date=asc&page=1").json()
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
    start = timer()
    with open('all-sets.json', 'r') as f:
        sets = json.load(f)
    
    setids = []
    for set in sets:
        setids.append(set['id'])

    upcoming = GetUpcomingSets()
    new = 0
    replaced = 0
    for index, set in enumerate(upcoming):
        filteredindexes = []
        if set['id'] not in setids:
            sets.append(set)
            new += 1
        else:
            for existingindex, existingset in enumerate(sets):
                if existingset['id'] == set['id']:
                    filteredindexes.append(existingindex)
            filteredindexes.sort()
            filteredindexes.reverse()

            for i in filteredindexes:
                sets.pop(i)
            sets.insert(filteredindexes[0], set)
            replaced += 1
    
    with open('all-sets.json', 'w') as f:
        json.dump(sets, f)
    
    end = timer()

    print(str(new) + " new sets added, " + str(replaced) + " sets replaced in " + str(end-start))


if __name__ == "__main__":
    main()