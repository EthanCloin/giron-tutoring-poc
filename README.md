# Summary

minimal website to demonstrate options for tutoring booking

## Quickstart
run the app.py file via CLI using 
```bash 
flask --app app init-db # *
flask --app app run --debug
```
*\*init-db command only needs run on intial setup, or if you want to reset the db contents*

## Google Calendar Appointment Scheduling Embed

everything you need except payments, direct integration by Google with Google Calendar

$10/month for multiple booking schedules

## Smart Calendar opensource webcomponent

Using the smart calendar means essentially rebuilding the Google embed ourselves.
Upfront development cost and reduced feature set to avoid subscription lockin.

I am pulling the specific files i need out of node_modules and putting them into the static directory
for the flask server! this addressed a problem where the calendar disappeared after including the flask server
layer and as a side effect should decrease the size of the relevant js bundle

# Reference
## flask docs
- https://flask.palletsprojects.com/en/3.0.x/tutorial/database/
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
