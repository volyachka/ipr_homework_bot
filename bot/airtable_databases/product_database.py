from pyairtable import Table

base_id = "appXjIXNWsvS0lrQf"
table_name = "tblAGOz1jL6EKpovb"
view = "AdminView"
airtable = Table('keymemYeYwP6fWTy0', base_id, table_name)
print(airtable.all(view = view))