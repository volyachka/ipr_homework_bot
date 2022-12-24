from airtable import Airtable
from pyairtable import Table
import pyairtable
from pyairtable.formulas import match

base_id = "appXjIXNWsvS0lrQf"
table_name = "tblqi8o0FUiKmDnyS"
view = "GridView"
country_table = Table('keymemYeYwP6fWTy0', base_id, table_name)
print(country_table.all())
# list_of_data = country_table.first(formula = match({'tg_username' : 'f'}))