import argparse
import sys

# python db.py --mode search -f all-sets.json --id 20654
# python db.py --mode search -f all-sets.json -s 'hi'
# python db.py --mode check-duplicates -f all-sets.json
# python db.py --mode base -f all-sets.json
# python db.py --mode upcoming -f all-sets.json
# python db.py --mode recent -f all-sets.json

parser = argparse.ArgumentParser()

parser.add_argument('--mode', choices=['search', 'check-duplicates', 'base', 'upcoming', 'recent'], help='specify operating mode', required=True, type=str)
parser.add_argument('-f', required=True, type=str, help='file name', metavar='file_name')
parser.add_argument('--id', required='search' in sys.argv, help='set id to search', metavar='set_id')
parser.add_argument('-s', required='search' in sys.argv, help='string to search', metavar='str')

args = parser.parse_args()

if args.mode == 'check-duplicates':
    pass
elif args.mode == 'base':
    pass
elif args.mode == 'upcoming':
    pass
elif args.mode == 'recent':
    pass
elif args.mode == 'search':
    pass
else:
    pass