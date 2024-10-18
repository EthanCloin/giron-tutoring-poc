# Summary

Webapp for booking an appointment with a tutor.
Built with Flask, HTMX, Docker, and SQLite.

## Quickstart
The project is configured to use Docker Compose as a development environment.

[Download and Install Docker Desktop](https://www.docker.com/)

With Docker Desktop running, you can simply navigate to the project root and run
```bash
docker compose up
```
This command will direct Docker to follow instructions defined in `compose.yml` to build and run the app container. 

You can find the proejct running on localhost at port 8080 on your local machine, as dictated by the 'ports' section in the app block of compose.yml.

Compose will also support watching: any changes in the src/app directory will trigger a rebuild of the container. 

If for whatever reason you don't want to use compose, you can build and run the container directly from the Dockerfile:
```bash
docker build -t <image-tagname> .
docker run -it --rm -p 8080:8000 <image-tagname>
```

The latest official image can be found in the [public Docker Hub Repository](https://hub.docker.com/repository/docker/ethancloin/booking-app/general)

# Open Source Tools
## [HTMX](https://htmx.org)
Lightweight framework for building hypermedia-driven applications.

Extends HTML by adding attributes which send AJAX requests like `hx-get` or `hx-post`

Supports DOM manipulation by replacing the `hx-target` element with the HTML response

## [Flask](https://flask.palletsprojects.com/en/3.0.x/)
Python micro-framework which supports API routing logic via decorators and HTML template rendering with the Jinja engine. 

- https://flask.palletsprojects.com/en/3.0.x/tutorial/database/
- https://jinja.palletsprojects.com/en/3.0.x/templates/

# Research
## Time Zones and Standards
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

## Calendar Formats
- https://en.wikipedia.org/wiki/ICalendar
- https://www.htmlelements.com/docs/calendar-api
