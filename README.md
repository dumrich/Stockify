# Stockify Web API
[![Build Status](https://travis-ci.com/dumrich/Stockify.svg?token=zTi4VzdoZNq1JFVnvzyd&branch=master)](https://travis-ci.com/dumrich/Stockify)

## **IMPORTANT**: Development on hold until very soon...


Stockify is a web api and (soon to be!) Python library that gets 10 year financial data from the www.sec.gov, and analyzes a list of stocks to invest in.  Python library coming soon.

## How to Install
You need docker and docker-compose in order to build and install this app.

1. First clone the repository
`git clone https://www.github.com/dumrich/Stockify` or click the large green button above the code section to download.

2. After moving to that directory, run `docker build .`

3. Finally, after switching to that directory, run `docker-compose up -d && docker-compose exec web python /Stockify/manage.py runserver 0.0.0.0:8000`

Now, go to `localhost:8000/Stockify/{put ticker here}` to get an analysis and the financial statements.  To scan your list of stocks or our best picks, go to localhost:8000/scanner/stocks?={leave blank if you want to use our master list, put in a list of stocks seperated by commas otherwise}

And done!

# Documentation coming soon!



#### Python Web Dev: Proj 1
Must Use:

- [x] OOP with property decorators, modules, class and static methods, dunder methods
- [ ] Some Data Structures
- [x] Comprehensions
- [ ] Lambda functions
- [ ] Collections
- [] args and kwargs required
- [ ] Inheritence
- [x] Modules
- [ ] closures/Non-OOP Decorators with `functools.wraps`
- [ ] Generators/Generator expressions
- [ ] Package
- [ ] metaclasses
- [ ] F-strings
- [x] Enumerate
- [ ] Zip
- [ ] Assignment Expressions
- [ ] Catch-all unpacking
- [ ] key sorting
- [ ] get/setdefault/defaultdict
- [ ] Itertools
- [ ] Class Hierarchies
- [ ] Classmethods
- [ ] super
- [ ] mixins
- [ ] property decorator/descriptor
- [ ] getattr, getattribute, setattr



#### To Do:
- [ ] Add scanner for all stocks
- [ ] Update the main Stockify algorithm to a custom and better one
- [ ] Add more of the advanced python concepts to project
- [ ] Upload the data package to PyPi
- [ ] Connect the algorithm to the DRF API
- [ ] Make web scraping faster/store statements inside PostgresDB
