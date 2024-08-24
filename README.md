# Summary

webapp for booking an appointment with a tutor.
built primarily using HTMX and Python.


## Quickstart (MacOS)
1. Create and activate a virtual environment in the root directory using `venv`
```bash
python -m venv .venv
source .venv/bin/activate
```
run the app.py file via CLI using 
```bash 
flask --app app init-db # *
flask --app app run --debug
```
*\*init-db command only needs run on intial setup, or if you want to reset the db contents*


## Project State
refer to the repository Issues 

current goal is to upgrade this to look prettier, utilize HTMX more effectively, Dockerize and deploy on fly.io


## Smart Calendar opensource webcomponent
this was the fastest way for me to get a calendar element on the page. may refactor to use something
different because it's rather annoying to work with. consider doing a Calendly integration too

# Reference
## HTMX
- https://htmx.org

## flask docs
- https://flask.palletsprojects.com/en/3.0.x/tutorial/database/
- https://jinja.palletsprojects.com/en/3.0.x/templates/
- 
## time stuff
- https://agileappscloud.info/aawiki/UTC_Format
- https://www.worldtimebuddy.com/est-to-utc-converter

| UTC Day   | Number |
| --------- | ------ |
| Sunday    | 0      |
| Monday    | 1      |
| Tuesday   | 2      |
| Wednesday | 3      |
| Thursday  | 4      |
| Friday    | 5      |
| Saturday  | 6      |
## calendar stuff
- https://en.wikipedia.org/wiki/ICalendar
- https://www.htmlelements.com/docs/calendar-api