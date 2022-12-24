from aiogram import types


def get_keyboard_for_categories():
    buttons = [
        types.InlineKeyboardButton(text="Accessories for kids", callback_data="cat_Accessories for kids"),
        types.InlineKeyboardButton(text="Clothes", callback_data="cat_Clothes"),
        types.InlineKeyboardButton(text="Vehicles", callback_data="cat_Vehicles"),
        types.InlineKeyboardButton(text="Household items", callback_data="cat_Household items"),
        types.InlineKeyboardButton(text="Education & Books", callback_data="cat_Education & Books"),
        types.InlineKeyboardButton(text="Furniture", callback_data="cat_Furniture"),
        types.InlineKeyboardButton(text="Home appliances", callback_data="cat_Home appliances"),
        types.InlineKeyboardButton(text="Personal things", callback_data="cat_Personal things"),
        types.InlineKeyboardButton(text="Other", callback_data="cat_Other"),
        types.InlineKeyboardButton(text="Confirm", callback_data="cat_Confirm")

    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2, resize_keyboard=True)
    keyboard.add(*buttons)
    return keyboard


def get_keyboard_for_frequency_of_mailing():
    buttons = [
        types.InlineKeyboardButton(text="once a day", callback_data="freq_24"),
        types.InlineKeyboardButton(text="once in three days", callback_data="freq_72"),
        types.InlineKeyboardButton(text="once in seven days", callback_data="freq_168"),
        types.InlineKeyboardButton(text="once in fourteen days", callback_data="freq_336")
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2, resize_keyboard=True)
    keyboard.add(*buttons)
    return keyboard


def get_keyboard_for_tracking_method():
    buttons = [
        types.InlineKeyboardButton(text="top-20 the cheapest", callback_data="track_cheapest"),
        types.InlineKeyboardButton(text="top-20 the newest", callback_data="track_newest"),
        types.InlineKeyboardButton(text="top-20 the closest", callback_data="track_closest"),
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2, resize_keyboard=True)
    keyboard.add(*buttons)
    return keyboard
