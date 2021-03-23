import json
from timeit import default_timer as timer

def main():
    start = timer()
    with open('all-sets.json', 'r') as f:
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


if __name__ == "__main__":
    main()