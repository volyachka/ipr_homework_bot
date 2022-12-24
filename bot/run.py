import logging
from aiogram import Bot, Dispatcher, executor
from pyairtable.formulas import match

from airtable_databases import users_database
from airtable_databases.country_database import country_table
from airtable_databases.users_database import user_table
from content.key_board import *
from aiogram.dispatcher.filters import Text
from content import msg
from content import mode
from settings import db_filename
from models import User
from helpers.database import create_db_if_not_exists, create_user

# Объект бота
bot = Bot(token="5299973465:AAEpVoFSj80P7Tpujsd-iTcrfoj5cQsOgZw")
# Диспетчер для бота
dp = Dispatcher(bot)
# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.answer(msg.start_text)
    await message.answer(msg.help_text)
    await message.answer(msg.request_country)
    tg_id = message.from_user.id
    user = User.get_or_none(tg_id=tg_id)
    if user is None:
        user = create_user(message)
    user.mode = mode.country
    user.save()
    return


@dp.callback_query_handler(Text(startswith="cat_"))
async def button_handler_for_categories(call: types.CallbackQuery):
    tg_id = call.from_user.id
    user = User.get_or_none(tg_id=tg_id)
    if user is None:
        await call.answer(msg.impossible_input)
        return
    if user.mode != mode.categories and user.mode != mode.change_categories:
        return
    if call.data == "cat_Confirm":
        if user.mode == mode.categories:
            user.mode = mode.frequency_of_mailing
            await call.message.answer(msg.request_frequency_of_mailing,
                                      reply_markup=get_keyboard_for_frequency_of_mailing())
        else:
            user.mode = mode.done
            await call.message.answer(msg.changes_made)
        user.save()
        return
    current_tracked_categories = user_table.get(user.id).get('fields').get('tracked_categories')

    if current_tracked_categories is None:
        user_table.update(user.id, {'tracked_categories': [call.data[4:]]})
        user.categories = call.data[4:]
        user.save()
        return
    if call.data in current_tracked_categories:
        return
    else:
        await call.answer(msg.answer_to_request)
        current_tracked_categories.append(call.data[4:])
        user.categories = user.categories + " " + call.data[4:]
        user_table.update(user.id, {'tracked_categories': current_tracked_categories})
        user.save()
        return


@dp.callback_query_handler(Text(startswith="freq_"))
async def button_handler_for_frequency_of_mailing(call: types.CallbackQuery):
    tg_id = call.from_user.id
    user = User.get_or_none(tg_id=tg_id)
    if user is None:
        await call.answer(msg.impossible_input)
        return
    if user.mode != mode.frequency_of_mailing and user.mode != mode.change_frequency_of_mailing:
        return
    user.frequency_of_mailing = call.data
    user_table.update(user.id, {'frequency_of_mailing': int(call.data[5:])})
    if user.mode == mode.change_frequency_of_mailing:
        user.mode = mode.done
        user.save()
        await call.message.answer(msg.changes_made)
    else:
        user.mode = mode.tracking_methods
        user.save()
        await call.message.answer(msg.request_tracking_methods, reply_markup=get_keyboard_for_tracking_method())
    return


@dp.callback_query_handler(Text(startswith="track_"))
async def button_handler_for_tracking_methods(call: types.CallbackQuery):
    tg_id = call.from_user.id
    user = User.get_or_none(tg_id=tg_id)
    if user is None:
        await call.answer(msg.impossible_input)
        return
    if user.mode != mode.tracking_methods and user.mode != mode.change_tracking_methods:
        return
    user_table.update(user.id, {'tracking_method': call.data[6:]})
    user.tracking_method = call.data[6:]
    if user.mode == mode.tracking_methods:
        await call.message.answer(msg.all_done)
    else:
        await call.message.answer(msg.changes_made)
    user.mode = mode.done
    user.save()
    return


@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    print(msg.help_text)
    await message.answer(msg.help_text)
    return


@dp.message_handler(commands=['add_category'])
async def help_command(message: types.Message):
    tg_id = message.from_user.id
    user = User.get_or_none(tg_id=tg_id)
    if user is None:
        await message.answer(msg.impossible_input)
        return
    user.mode = mode.change_categories
    user.save()
    await message.answer('tracked_categories: ' + str(
        user_table.first(formula=match({'tg_id': user.tg_id})).get('fields').get('tracked_categories')))
    await message.answer(msg.request_categories, reply_markup=get_keyboard_for_categories())
    return


@dp.message_handler(commands=['delete_category'])
async def help_command(message: types.Message):
    tg_id = message.from_user.id
    user = User.get_or_none(tg_id=tg_id)
    if user is None:
        await message.answer(msg.impossible_input)
        return
    user.mode = mode.delete_category
    user.save()
    await message.answer('available_categories: ' + str(
        user_table.first(formula=match({'tg_id': user.tg_id})).get('fields').get('tracked_categories')))
    await message.answer(msg.request_categories_for_delete)

    return


@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    print(msg.help_text)
    await message.answer(msg.help_text)
    return


@dp.message_handler(commands=['change_country'])
async def help_command(message: types.Message):
    tg_id = message.from_user.id
    user = User.get_or_none(tg_id=tg_id)
    if user is None:
        await message.answer(msg.impossible_input)
        return
    user.mode = mode.change_country
    user.save()
    await message.answer(msg.request_country)
    return


@dp.message_handler(commands=['change_city'])
async def help_command(message: types.Message):
    tg_id = message.from_user.id
    user = User.get_or_none(tg_id=tg_id)
    if user is None:
        await message.answer(msg.impossible_input)
        return
    user.mode = mode.change_city
    user.save()
    await message.answer(msg.request_city)
    return


@dp.message_handler(commands=['change_mailing_frequency'])
async def help_command(message: types.Message):
    tg_id = message.from_user.id
    user = User.get_or_none(tg_id=tg_id)
    if user is None:
        await message.answer(msg.impossible_input)
        return
    user.mode = mode.change_frequency_of_mailing
    user.save()
    await message.answer(msg.request_categories, reply_markup=get_keyboard_for_frequency_of_mailing())
    return


@dp.message_handler(commands=['change_tracking_method'])
async def help_command(message: types.Message):
    tg_id = message.from_user.id
    user = User.get_or_none(tg_id=tg_id)
    if user is None:
        await message.answer(msg.impossible_input)
        return
    user.mode = mode.change_tracking_methods
    user.save()
    await message.answer(msg.request_tracking_methods, reply_markup=get_keyboard_for_tracking_method())
    return



@dp.message_handler(content_types=["text"])
async def echo(message: types.Message):
    tg_id = message.from_user.id
    user = User.get_or_none(tg_id=tg_id)
    if user is None:
        await message.answer(msg.impossible_input)
        return
    if user is None:
        await message.answer(msg.impossible_input)
        return
    print(user)
    print(user.mode)
    if user.mode == mode.country:
        user.country = message.text.capitalize()
        list_of_data = country_table.first(formula=match({'Name': message.text.capitalize()}))
        if list_of_data is None:
            await message.answer(msg.incorrect_country)
            await message.answer(msg.list_of_available_countries)
            return
        else:
            user.mode = mode.city
            user_table.update(user.id, {'country': [list_of_data.get('id')]})
            await message.answer(msg.request_city)
            user.save()
    elif user.mode == mode.city:
        user.city = message.text.capitalize()
        if user.city in users_database.list_of_available_cities:
            user_table.update(user.id, {'city': user.city})
        else:
            user_table.update(user.id, {'city': "Not Belgium or Montenegro city"})
        user.mode = mode.categories
        user.save()
        await message.answer(msg.request_categories, reply_markup=get_keyboard_for_categories())
    elif user.mode == mode.categories or user.mode == mode.change_categories:
        await message.answer(msg.request_categories, reply_markup=get_keyboard_for_categories())
    elif user.mode == mode.tracking_methods or user.mode == mode.change_tracking_methods:
        await message.answer(msg.request_tracking_methods, reply_markup=get_keyboard_for_tracking_method())
    elif user.mode == mode.frequency_of_mailing or user.mode == mode.change_frequency_of_mailing:
        await message.answer(msg.request_frequency_of_mailing, reply_markup=get_keyboard_for_frequency_of_mailing())
    elif user.mode == mode.change_country:
        user.country = message.text.capitalize()
        list_of_data = country_table.first(formula=match({'Name': message.text.capitalize()}))
        if list_of_data is None:
            await message.answer(msg.incorrect_country)
            await message.answer(msg.list_of_available_countries)
            return
        else:
            user.mode = mode.done
            user_table.update(user.id, {'country': [list_of_data.get('id')]})
            await message.answer(msg.changes_made)
            user.save()
    elif user.mode == mode.change_city:
        user.city = message.text.capitalize()
        if user.city in users_database.list_of_available_cities:
            user_table.update(user.id, {'city': user.city})
        else:
            user_table.update(user.id, {'city': "Not Belgium or Montenegro city"})
        user.mode = mode.done
        user.save()
        await message.answer(msg.changes_made)
    elif user.mode == mode.delete_category:
        categories = user_table.first(formula=match({'tg_id': user.tg_id})).get('fields').get('tracked_categories')
        new_list_of_categories = []
        for category in categories:
            if category != message.text:
                new_list_of_categories.append(category)
        user_table.update( user.id, {'tracked_categories': new_list_of_categories})
        user.categories = new_list_of_categories
        await message.answer(msg.changes_made)
        await  message.answer("tracked_categories: " + str(new_list_of_categories))
        user.mode = mode.done
        user.save()
    elif user.mode == mode.done:
        await message.answer(msg.all_done)
    else:
        await message.answer(msg.impossible_input)
    return


if __name__ == "__main__":
    create_db_if_not_exists(db_filename)
    executor.start_polling(dp, skip_updates=True)
