import json

with open('all-sets.json', 'r') as f:
    sets = json.load(f)

# 21113
searchid = 177

filtered = list(filter(lambda set: set['id'] == searchid, sets))
if len(filtered) == 0:
    print("Nothing found")
elif len(filtered) == 1:
    print("Match found")
else:
    print("More than one match found")