from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from crud_functions import *



api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


kb = ReplyKeyboardMarkup(resize_keyboard = True)

bu1 = KeyboardButton(text = 'Рассчитать')
bu2 = KeyboardButton(text = 'Информация')
bu3 = KeyboardButton(text = 'Купить')

kb.add(bu1)
kb.add(bu2)
kb.add(bu3)



kbinl = InlineKeyboardMarkup()
kbinl2 = InlineKeyboardMarkup()
kbinl3 = InlineKeyboardMarkup()



bu_inl_1 = InlineKeyboardButton(text = 'Рассчитать норму калорий', callback_data = 'calories')
bu_inl_2 = InlineKeyboardButton(text = 'Формулы расчёта', callback_data = 'formulas')
kbinl.add(bu_inl_1)
kbinl.add(bu_inl_2)



bu_inl_3 = InlineKeyboardButton(text = 'Адреналин', callback_data = 'product_buying')
bu_inl_4 = InlineKeyboardButton(text = 'Пропофол', callback_data = 'product_buying')
bu_inl_5 = InlineKeyboardButton(text = 'Галоперидол', callback_data = 'product_buying')
bu_inl_6 = InlineKeyboardButton(text = 'Феназепам', callback_data = 'product_buying')
kbinl2.add(bu_inl_3)
kbinl2.add(bu_inl_4)
kbinl2.add(bu_inl_5)
kbinl2.add(bu_inl_6)


bu_m = InlineKeyboardButton(text = 'М', callback_data = 'М')
bu_w = InlineKeyboardButton(text = 'Ж', callback_data = 'Ж')
kbinl3.add(bu_m)
kbinl3.add(bu_w)



class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()
    sex = State()




@dp.message_handler(commands=['start'])
async def start(message):
     await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup = kb)

@dp.message_handler(text = 'Информация')
async def info(message):
    await message.answer('Пока я умею только считать норму твоих калорий и якобы продавать колёса')


@dp.message_handler(text = 'Купить')
async def get_buying_list(message):
    list_of_products = get_all_products()
    count_of_pic = 0
    for product in list_of_products:
        name = product[1]
        discr = product[2]
        price = product[3]
        with open(f'prod{count_of_pic}.png', 'rb') as photo_of_product:
            await message.answer_photo(photo_of_product ,f'Название: {name}|Описание: {discr}|Цена: {price}')
            count_of_pic +=1
    await message.answer('Выберите продукт для покупки:', reply_markup = kbinl2)


@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup = kbinl)

@dp.callback_query_handler(text = 'formulas')
async def get_formulas(call):
    await call.message.answer('Формулы Миффлина-Сан Жеора для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5;'
                            'Для женщин: 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161.')
    await call.answer()

@dp.callback_query_handler(text = 'product_buying')
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!')
    await call.answer()


@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await call.answer()
    await UserState.age.set()

@dp.message_handler(state = UserState.age)
async def set_growth(message, state):
    await state.update_data(age = message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()

@dp.message_handler(state = UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth = message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()

@dp.message_handler(state = UserState.weight)
async def set_sex(message, state):
    await state.update_data(weight=message.text)
    await message.answer('Введите свой пол:', reply_markup = kbinl3)
    await UserState.sex.set()

@dp.callback_query_handler(state = UserState.sex, text = 'М')
async def calc_for_men(call, state):
    data = await state.get_data()
    calories_for_men = (10*int(data['weight']) + 6.25*int(data['growth']) - 5*int(data['age']))+5
    await call.message.answer(f'Ваша норма калорий: {calories_for_men}ккал/сут')
    await state.finish()

@dp.callback_query_handler(state = UserState.sex, text = 'Ж')
async def calc_for_women(call, state):
    data = await state.get_data()
    calories_for_women = (10*int(data['weight']) + 6.25*int(data['growth']) - 5*int(data['age']))-161
    await call.message.answer(f'Ваша норма калорий: {calories_for_women}ккал/сут')
    await state.finish()




if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)