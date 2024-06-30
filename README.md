# Summary

minimal website to demonstrate options for tutoring booking

run with VSCode Live Server extension or preferred httpserver

## Google Calendar Appointment Scheduling Embed

everything you need except payments, direct integration by Google with Google Calendar

$10/month for multiple booking schedules

## Smart Calendar opensource webcomponent

Using the smart calendar means essentially rebuilding the Google embed ourselves.
Upfront development cost and reduced feature set to avoid subscription lockin.

### Required Custom Logic

Database

- Tutor Availability

Client

- Request Tutor Availability for some time period
- Lookup Tutor Availability by Day
- Form to request Booking
- Manage state like `selectedDate` and `selectedTutor` to affect rendered content

Server

- CRUD operations on Tutor Availability
- Calendar integration
- Google Meet integration
