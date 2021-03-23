import json
import sys
from timeit import default_timer as timer
import argparse
import requests
from alive_progress import alive_bar

def printseries(serieslist):
    for series in serieslist:
        print(series['name'] + ' (' + str(series['id']) + ') by ' + series['creator']['username'] + ': ' + series['difficulty'] + ' ' + series['edition_size'] + ' series')

def checkduplicates(filename):
    start = timer()
    with open(filename, 'r') as f:
        sets = json.load(f)
    
    tracker = {}

    for set in sets:
        if set['id'] in tracker:
            tracker[set['id']] += 1
        else:
            tracker[set['id']] = 1
    
    # print(tracker)
    found = 0
    for i in tracker:
        if tracker[i] > 1:
            print(str(i) + ": " + str(tracker[i]))
            found += 1
    end = timer()
    print(str(end-start))

def searchbyid(id, filename):
    start = timer()

    with open(filename, 'r') as f:
        sets = json.load(f)

    filtered = list(filter(lambda set: set['id'] == id, sets))
    if len(filtered) == 0:
        print("Nothing found")
    elif len(filtered) == 1:
        print("Match found")
        printseries(filtered)
    else:
        print("More than one match found")
        printseries(filtered)
    
    end = timer()
    print(str(end - start))

def searchbystr(s, filename):
    start = timer()

    with open(filename, 'r') as f:
        sets = json.load(f)

    results = 0

    if len(s) >= 2:
        filtered = list(filter(lambda set: s.lower() in set['name'].lower() or s.lower() in set['name_slug'].lower(), sets))
        results = len(filtered)
        if len(filtered) == 0:
            print("Nothing found")
        elif len(filtered) == 1:
            # print(filtered)
            printseries(filtered)
        else:
            # print(filtered)
            printseries(filtered)
    else:
        print("not enough stuff")

    end = timer()
    print(str(results) + " results in " + str(end - start))

def getbase(filename):
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
    
    with open(filename, 'w') as f:
        json.dump(sets, f)

def getupcomingsets():
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

def getupcoming(filename):
    start = timer()
    with open(filename, 'r') as f:
        sets = json.load(f)
    
    setids = []
    for set in sets:
        setids.append(set['id'])

    upcoming = getupcomingsets()
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

def getrecentsets(pages):
    sets = []
    data = requests.request('GET', "https://www.neonmob.com/api/setts/legacy_list/?category=newest&release_date=desc&page=1").json()
    # https://www.neonmob.com/api/setts/legacy_list/?category=&release_date=asc&page=1
    total = pages * 9

    with alive_bar(total, bar='smooth', spinner='dots_recur') as bar:
        for i in range(pages):
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

def getrecent(filename, pages):
    start = timer()
    with open('all-sets.json', 'r') as f:
        sets = json.load(f)
    
    setids = []
    for set in sets:
        setids.append(set['id'])
    
    recent = getrecentsets(pages)
    new = 0
    replaced = 0
    for index, set in enumerate(recent):
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

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('--mode', choices=['search', 'check-duplicates', 'base', 'upcoming', 'recent'], help='specify operating mode (required)', required=True, type=str)
    parser.add_argument('-f', required=True, type=str, help='file name (required)', metavar='file_name')
    searches = parser.add_mutually_exclusive_group(required='search' in sys.argv)
    searches.add_argument('--id', help='set id to search', metavar='set_id', type=int)
    searches.add_argument('-s', help='string to search', metavar='str', type=str)
    parser.add_argument('--pages', help='pages of recent sets to update', metavar='pages', type=int, required='recent' in sys.argv)

    args = parser.parse_args()

    if args.mode == 'check-duplicates':
        checkduplicates(args.f)
    elif args.mode == 'base':
        getbase(args.f)
    elif args.mode == 'upcoming':
        getupcoming(args.f)
    elif args.mode == 'recent':
        getrecent(args.f, args.pages)
    elif args.mode == 'search':
        if args.s == None:
            searchbyid(args.id, args.f)
        else:
            searchbystr(args.s, args.f)
    else:
        print("Something isn't right")

if __name__ == "__main__":
    main()