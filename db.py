import sqlite3

import click
from flask import current_app, g


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    db = sqlite3.connect(
        database='data/database.sqlite',
        detect_types=sqlite3.PARSE_DECLTYPES
    )
    with open('schema.sql') as f:
        db.executescript(f.read())
        click.echo('Initialized the database.')


if __name__ == '__main__':
    yes = click.confirm('Do you want to reinitialize database?', abort=True)
    if yes:
        init_db_command()
    else:
        click.echo('Aborted.')
