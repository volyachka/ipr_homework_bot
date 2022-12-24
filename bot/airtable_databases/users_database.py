from airtable import Airtable
from pyairtable import Table
import pyairtable
from pyairtable.formulas import match

base_id = "appXjIXNWsvS0lrQf"
table_name = "tbljIqYknSoLX58I2"
view = "GridView"
user_table = Table('keymemYeYwP6fWTy0', base_id, table_name)
list_of_data = user_table.first(formula = match({'tg_username' : 'f'}))
# print(list_of_data)
# print(list_of_data.get('id'))
# user_table.delete(list_of_data.get('id'))
# user_table.update('tg_id', '1', {'city' : 'Brussels'})
# contact = {
#     'tg_id': '1',
#     'tg_username': 'Petya',
#     # 'country': "Not Belgium or Montenegro city",
#     'city': "Not Belgium or Montenegro city",
#     'tracked_categories': ["Household items"],
#     'frequency_of_mailing': 42,
#     'tracking_method': "newest"
# }
#


# user_table.create({    'tg_id': '1',
#     'tg_username': 'Petya',
#     'country': 'France',
#     'city': 'Paris',
#     'tracked_categories': ['hats', 'books'],
#     'frequency_of_mailing': 'ones in 3 days',
#     'tracking_method': 'cheapest' })
# def add_record(contact):
#     "добавляем запись в бд пользователя"
#     user_table.create(contact)
#
# def update_record(contact, tg_id):
#     "обновляем запись в бд пользователя по tg_id"
#     user_table.update('tg_id', tg_id, contact)
#
# add_record(contact)

list_of_available_cities = {
    "Brussels",
    "Antwerp",
    "Ghent",
    "Charleroi",
    "Lieje",
    "Bruges",
    "Namur",
    "Leuven",
    "Mons",
    "Aalst",
    "Mechelen",
    "La Louvière",
    "Hasselt",
    "Sint-Niklaas",
    "Kortrijk",
    "Other Belgian cities",
    "Podgorica",
    "Nikšić",
    "Herceg Novi",
    "Pljevlja",
    "Bar",
    "Bijelo Polje",
    "Other Montenegrin city",
    "Not Belgium or Montenegro city"
}