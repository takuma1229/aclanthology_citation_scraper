# ACL Anthology paper scraper

## setup
```
$ rye init
$ rye sync
$ . .venv/bin/activate
```

## get all papers and citation counts for specific year
```
// example: execute script for ACL in 2022
$ make run CONFERENCE=acl YEAR=2022
```

## get all papers and citation counts for all years within the specified period
```
// example: execute script for ACL in 2010-2021
$ make run_all CONFERENCE=acl START_YEAR=2010 END_YEAR=2021
```