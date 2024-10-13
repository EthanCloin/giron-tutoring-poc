FROM python:3.10.0

COPY ./requirements.txt app/requirements.txt
WORKDIR app

RUN pip install -r requirements.txt

COPY ./app/templates /app
COPY ./app/static /app
COPY ./app/*.py /app

# TODO: consider some database setup script running here

EXPOSE 8000

CMD ["gunicorn","--config", "gunicorn_config.py", "__init__:create_app()"]

