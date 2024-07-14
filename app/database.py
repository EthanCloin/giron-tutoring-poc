from flask import current_app, g
import sqlite3
import click


def get_db():
    # 'g' is a flask object generated on each unique request.
    # if a single request hits the db multiple times, it would reuse the
    # db already present in 'g'
    if "db" not in g:
        g.db = sqlite3.connect("./booking.db", detect_types=sqlite3.PARSE_DECLTYPES)
        g.db.row_factory = sqlite3.Row

    return g.db


def init_db():
    db = get_db()

    with current_app.open_resource("static/sql/build-fresh-schema.sql") as f:
        db.executescript(f.read().decode("utf8"))


@click.command("init-db")
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo("Initialized the database.")


def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
