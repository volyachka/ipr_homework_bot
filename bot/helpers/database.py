import peewee
from pyairtable.formulas import match

from airtable_databases.users_database import user_table
from helpers.file_checker import file_exists
from helpers.telegram import handle_username
from models import db, User


def create_user(message):
    # create new_user in database
    tg_id = message.from_user.id
    username = handle_username(message)
    user_table.create({'tg_id': str(tg_id), 'tg_username': handle_username(message)})
    id = user_table.first(formula=match({'tg_id': str(tg_id)})).get('id')
    print(username)
    with db.atomic():
        user = User.create(tg_id=tg_id,
                           tg_username=username,
                           id=id,
                           mode="need to fill country")
    return user


def db_save(model):
    with db.atomic():
        model.save()


def create_db_if_not_exists(filename):
    if file_exists(filename):
        return False
    my_db = peewee.SqliteDatabase(filename)
    my_db.connect()
    my_db.create_tables([User, ])
    my_db.close()
    return True
