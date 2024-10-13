FROM python:3.10.0
WORKDIR /
ENV CONTAINER_APP_DIR=/src/app

COPY ./src/requirements.txt $CONTAINER_APP_DIR/requirements.txt
COPY ./src/app/templates $CONTAINER_APP_DIR/templates
COPY ./src/app/static $CONTAINER_APP_DIR/static
COPY ./src/app/*.py $CONTAINER_APP_DIR 
COPY ./src/gunicorn_config.py /src

WORKDIR $CONTAINER_APP_DIR 

RUN pip install -r requirements.txt

# TODO: consider some database setup script running here

EXPOSE 8000

WORKDIR ../

CMD ["gunicorn","--config", "gunicorn_config.py", "app:create_app()"]

