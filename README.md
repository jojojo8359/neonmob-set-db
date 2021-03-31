# neonmob-set-db [![Daily update](https://github.com/jojojo8359/neonmob-set-db/actions/workflows/update.yml/badge.svg?event=schedule)](https://github.com/jojojo8359/neonmob-set-db/actions/workflows/update.yml) [![Rebuild database](https://github.com/jojojo8359/neonmob-set-db/actions/workflows/rebuild.yml/badge.svg?event=schedule)](https://github.com/jojojo8359/neonmob-set-db/actions/workflows/rebuild.yml)
A self-updating database of all series/sets on NeonMob.

The `db.py` script contains various functions for fetching new data and analyzing existing data.

```
usage: db.py [-h] --mode {search,check-duplicates,base,upcoming,recent} -f file_name [--id set_id | -s str] [--pages pages]

optional arguments:
  -h, --help            show this help message and exit
  --mode {search,check-duplicates,base,upcoming,recent}
                        specify operating mode (required)
  -f file_name          file name (required)
  --id set_id           set id to search
  -s str                string to search
  --pages pages         pages of recent sets to update
```
For all commands, the `--mode` and `-f` flags are required.

# Modes

## `search`
The search mode searches a given file for sets matching specific criteria. Right now, it can search for specified set ids and set names.

#### Usage:

`python db.py --mode search -f all-sets.json --id 12345`

`python db.py --mode search -f all-sets.json -s 'NeonMob'`

## `check-duplicates`
The check-duplicate mode will search a given file for duplicated set data, and will give a report back to the user as to which set ids are duplicated in the file.

#### Usage:

`python db.py --mode check-duplicates -f all-sets.json`

## `base`
The base mode will retrieve ALL sets that are publicly available on NeonMob (excluding upcoming sets, since they have not been added into the master pool of sets) and save them to a specified filename. EXISTING FILES WILL BE OVERWRITTEN. Expect this command to take many minutes to complete.

#### Usage:

`python db.py --mode base -f all-sets.json`

## `upcoming`
The upcoming mode will append all upcoming sets to the file specified, replacing existing sets and ensuring no duplicates exist.

#### Usage:

`python db.py --mode upcoming -f all-sets.json`

## `recent`
The recent mode will append a specified number of pages of recent sets to the file specified, where a page of sets is usually 9 (for how they are displayed on the website).

#### Usage:

`python db.py --mode recent -f all-sets.json --pages 3`
