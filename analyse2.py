import json
from timeit import default_timer as timer

start = timer()

with open('all-sets.json', 'r') as f:
    sets = json.load(f)

# 21113
searchid = 20523
searchterm = "sketchbook 201"
results = 0

if len(searchterm) >= 2:
    filtered = list(filter(lambda set: searchterm.lower() in set['name'].lower() or searchterm.lower() in set['name_slug'].lower(), sets))
    results = len(filtered)
    if len(filtered) == 0:
        print("Nothing found")
    elif len(filtered) == 1:
        print(filtered)
    else:
        print(filtered)
else:
    print("not enough stuff")

end = timer()
print(str(results) + " results in " + str(end - start))