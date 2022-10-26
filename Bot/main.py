import datetime
import itertools
import logging
import os
import re
from dataclasses import dataclass
from typing import Iterable, Optional

import aiogram
from aiogram import Bot, Dispatcher, executor, filters
from aiogram.contrib.fsm_storage.mongo import MongoStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import markdown as md
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env')

if os.getenv('BOT_DEBUG'):
    logging.basicConfig(level=logging.DEBUG)

CITIES = os.getenv('CITIES').split(',')

bot = Bot(token=os.getenv('BOT_TOKEN'))
mem = MongoStorage(db_name='HelpService', uri=os.getenv('MONGODB_URL'))
dp = Dispatcher(bot, storage=mem)


class States(StatesGroup):
    start = State()
    q_username = State()
    q_city = State()
    q_name = State()
    q_phone = State()
    q_district = State()
    q_address = State()
    q_people = State()
    q_comment = State()
    q_food = State()
    q_can_cook = State()
    q_meds = State()
    confirm = State()


class ButtonText:
    back = "Назад"
    cancel = "Скасувати"
    yes = "Так"
    no = "Ні"
    make_order = "Зробити замовлення"
    view_orders = "Переглянути мої замовлення"
    no_comment = "Без коментаря"
    use_telegram_name = "Використати ім'я з Telegram"
    change_name = "Змінити ім'я"
    no_food = "Без їжі"
    no_meds = "Без медикаментів"


def create_dynamic_keyboard(values: Iterable, cols: int):
    return ReplyKeyboardMarkup(list(itertools.zip_longest(
        *itertools.repeat(itertools.chain((KeyboardButton(str(v)) for v in values), (KeyboardButton(ButtonText.cancel),)), cols),
        fillvalue='')), resize_keyboard=True, row_width=cols)


class Keyboards:
    cancel = ReplyKeyboardMarkup([[KeyboardButton(ButtonText.cancel)]], resize_keyboard=True, row_width=1)
    yes_no_cancel = ReplyKeyboardMarkup([[KeyboardButton(ButtonText.yes), KeyboardButton(ButtonText.no)],
                                         [KeyboardButton(ButtonText.cancel)]], resize_keyboard=True, row_width=2)
    yes_cancel = ReplyKeyboardMarkup([[KeyboardButton(ButtonText.yes), KeyboardButton(ButtonText.cancel)]], resize_keyboard=True, row_width=2)
    register = ReplyKeyboardMarkup([[KeyboardButton(ButtonText.use_telegram_name)]], resize_keyboard=True, row_width=1)
    register_cancel = ReplyKeyboardMarkup([[KeyboardButton(ButtonText.use_telegram_name)],
                                           [KeyboardButton(ButtonText.cancel)]], resize_keyboard=True, row_width=1)
    order_orders = ReplyKeyboardMarkup([[KeyboardButton(ButtonText.change_name), KeyboardButton(ButtonText.make_order)],
                                        [KeyboardButton(ButtonText.view_orders)]], resize_keyboard=True, row_width=2)
    cities = create_dynamic_keyboard(CITIES, cols=2) if len(CITIES) > 1 else None
    no_comment_cancel = ReplyKeyboardMarkup([[KeyboardButton(ButtonText.no_comment)],
                                             [KeyboardButton(ButtonText.cancel)]], resize_keyboard=True, row_width=1)
    no_food_cancel = ReplyKeyboardMarkup([[KeyboardButton(ButtonText.no_food)],
                                          [KeyboardButton(ButtonText.cancel)]], resize_keyboard=True, row_width=1)
    no_meds_cancel = ReplyKeyboardMarkup([[KeyboardButton(ButtonText.no_meds)],
                                          [KeyboardButton(ButtonText.cancel)]], resize_keyboard=True, row_width=1)


def format_phone_number(phone: str):
    clean = re.sub(r'[^0-9]+', '', phone)

    length = len(clean)

    if length == 10 or length == 12:
        tail = f'{clean[-7:-4]} {clean[-4:-2]} {clean[-2:]}'
        if length == 12:
            return f'+{clean[:3]} {clean[-9:-7]} {tail}'
        else:
            return f'({clean[0]}{clean[-9:-7]}) {tail}'
    else:
        return phone


@dataclass
class Order:
    city: str
    name: str
    phone: str
    district: str
    address: str
    people: int
    can_cook: bool = None
    food: str = None
    meds: str = None
    comment: str = 'відсутній'
    order_id: str = None
    status: int = 1
    date: datetime.datetime = None

    def format_md(self):  # TODO format phone
        food = self.food or 'не потрібна'
        meds = self.meds or 'не потрібні'

        body = (f"Місто: {self.city}\n"
                f"Ім'я: {self.name}\n"
                f"Телефон: {format_phone_number(self.phone)}\n"
                f"Район: {self.district}\n"
                f"Адреса: {self.address}\n"
                f"Кількість людей: {self.people}\n"
                f"Їжа: {food}\n"
                f"Медикаменти: {meds}")

        if self.food:
            can_cook = 'так' if self.can_cook else 'ні'

            body += f"\nМожете готувати: {can_cook}"

        if self.comment:
            body += f"\nКоментар: {self.comment}"

        if self.date is None:
            self.date = datetime.datetime(2000, 1, 1)

        if self.order_id:
            return md.escape_md(f"Номер замовлення: {self.order_id}\n"
                                f"{body}\n"
                                f"Статус: {self.status}\n"
                                f"Дата: {self.date:%d.%m.%Y %H:%M:%S}")
        else:
            return md.escape_md(body)


@dp.message_handler(text=ButtonText.change_name, state=States.start)
async def h__start__change_name(msg: Message, allow_cancel: bool = True):
    await States.q_username.set()
    await msg.answer("Вкажіть ваше ім'я.", reply_markup=Keyboards.register_cancel if allow_cancel else Keyboards.register)


@dp.message_handler(commands='start', state='*')
async def h__any__start(msg: Message):
    await States.start.set()

    bucket = await mem.get_bucket(user=msg.from_user.id)

    start_msg = "Я бот HelpService..."

    if bucket.get('name'):
        await msg.answer(start_msg, reply_markup=Keyboards.order_orders)
    else:
        await msg.answer(start_msg)

        await h__start__change_name(msg, allow_cancel=False)


@dp.message_handler(text=ButtonText.cancel, state='*')
async def h__any__cancel(msg: Message):
    await h__any__start(msg)


@dp.message_handler(text=ButtonText.make_order, state=States.start)
async def h__start__order(msg: Message):
    await mem.update_bucket(user=msg.from_user.id, q_name=msg.text)

    if len(CITIES) == 1:
        await mem.update_bucket(user=msg.from_user.id, q_city=CITIES[0])

        await States.q_name.set()
        await msg.answer("Вкажіть ім'я.", reply_markup=Keyboards.cancel)
    else:
        await States.q_city.set()
        await msg.answer("Вкажіть місто.", reply_markup=Keyboards.cities)


async def h__q_username__next_state(msg: Message):
    await States.start.set()
    await msg.answer("Гарне ім'я. )", reply_markup=Keyboards.order_orders)


@dp.message_handler(text=ButtonText.use_telegram_name, state=States.q_username)
async def h__q_username__telegram(msg: Message):
    user = msg.from_user

    name = f'{user.first_name} {user.last_name}' if user.last_name else user.first_name

    await mem.update_bucket(user=msg.from_user.id, name=name, orders=[])

    await msg.answer(f"Ваше ім'я: {name}.")
    await h__q_username__next_state(msg)


@dp.message_handler(state=States.q_username)
async def h__q_username(msg: Message):
    await mem.update_bucket(user=msg.from_user.id, name=msg.text, orders=[])

    await h__q_username__next_state(msg)


@dp.message_handler(filters.Text(CITIES, ignore_case=True), state=States.q_city)
async def h__q_city(msg: Message):
    city = msg.text.lower()
    city = next(c for c in CITIES if c.lower() == city)

    await mem.update_bucket(user=msg.from_user.id, q_city=city)

    await States.q_name.set()
    await msg.answer("Вкажіть ім'я.", reply_markup=Keyboards.cancel)


@dp.message_handler(state=States.q_name)
async def h__q_name(msg: Message):
    await mem.update_bucket(user=msg.from_user.id, q_name=msg.text)

    await States.q_phone.set()
    await msg.answer("Вкажіть номер телефону.", reply_markup=Keyboards.cancel)


@dp.message_handler(regexp=r'^[+]?[0-9 \-\(\)]{3,25}$', state=States.q_phone)
async def h__q_phone(msg: Message):
    phone = re.sub(r'\D', '', msg.text, flags=re.ASCII)  # TODO better parsing, better checking

    await mem.update_bucket(user=msg.from_user.id, q_phone=phone)

    await States.q_district.set()
    await msg.answer(f"Вкажіть район.", reply_markup=Keyboards.cancel)


@dp.message_handler(state=States.q_district)
async def h__q_district(msg: Message):
    await mem.update_bucket(user=msg.from_user.id, q_district=msg.text)

    await States.q_address.set()
    await msg.answer(f"Вкажіть адресу/орієнтир.", reply_markup=Keyboards.cancel)


@dp.message_handler(state=States.q_address)
async def h__q_address(msg: Message):
    await mem.update_bucket(user=msg.from_user.id, q_address=msg.text)

    await States.q_people.set()
    await msg.answer("Вкажіть кількість людей.", reply_markup=Keyboards.cancel)


@dp.message_handler(regexp='^[0-9]+$', state=States.q_people)
async def h__q_people(msg: Message):
    people = int(msg.text)

    if not people:
        await msg.answer("Це замало.")
        return

    await mem.update_bucket(user=msg.from_user.id, q_people=people)

    await States.q_comment.set()
    await msg.answer("Вкажіть коментар.", reply_markup=Keyboards.no_comment_cancel)


@dp.message_handler(text=ButtonText.no_comment, state=States.q_comment)
async def h__q_comment__no_comment(msg: Message):
    await States.q_food.set()
    await msg.answer("Вкажіть їжу (через кому).", reply_markup=Keyboards.no_food_cancel)


@dp.message_handler(state=States.q_comment)
async def h__q_comment(msg: Message):
    await mem.update_bucket(user=msg.from_user.id, q_comment=msg.text)

    await h__q_comment__no_comment(msg)


@dp.message_handler(text=ButtonText.no_food, state=States.q_food)
async def h__q_food__no_food(msg: Message):
    await h__q_food(msg, None)


@dp.message_handler(state=States.q_food)
async def h__q_food__text(msg: Message):
    await h__q_food(msg, msg.text)


async def h__q_food(msg: Message, food: Optional[str]):
    await mem.update_bucket(user=msg.from_user.id, q_food=food)

    if food:
        await States.q_can_cook.set()
        await msg.answer("Ви можете готувати? (y/n)", reply_markup=Keyboards.yes_no_cancel)
    else:
        await h__q_can_cook(msg, None)


async def h__q_can_cook(msg: Message, can_cook: Optional[bool]):
    await mem.update_bucket(user=msg.from_user.id, q_can_cook=can_cook)

    await States.q_meds.set()
    await msg.answer("Вкажіть медикаменти (через кому).",
                     reply_markup=Keyboards.cancel if can_cook is None else Keyboards.no_meds_cancel)


@dp.message_handler(filters.Text((ButtonText.yes, 'y'), ignore_case=True), state=States.q_can_cook)
async def h__q_can_cook__yes(msg: Message):
    await h__q_can_cook(msg, True)


@dp.message_handler(filters.Text((ButtonText.no, 'n'), ignore_case=True), state=States.q_can_cook)
async def h__q_can_cook__no(msg: Message):
    await h__q_can_cook(msg, False)


@dp.message_handler(text=ButtonText.no_meds, state=States.q_meds)
async def h__q_meds__no_meds(msg: Message):
    await h__q_meds(msg, None)


@dp.message_handler(state=States.q_meds)
async def h__q_meds__text(msg: Message):
    await h__q_meds(msg, msg.text)


async def h__q_meds(msg: Message, meds: Optional[str]):
    bucket = await mem.get_bucket(user=msg.from_user.id)

    if not meds and not bucket.get('q_food'):
        return await h__any__wrong(msg)

    order = Order(bucket.pop('q_city'), bucket.pop('q_name'), bucket.pop('q_phone'), bucket.pop('q_district'),
                  bucket.pop('q_address'), bucket.pop('q_people'), bucket.pop('q_can_cook'), bucket.pop('q_food', None),
                  meds, bucket.pop('q_comment', None))

    bucket['order'] = order.__dict__

    await mem.set_bucket(user=msg.from_user.id, bucket=bucket)

    await States.confirm.set()
    await msg.answer(f"{order.format_md()}\n\nПідтверджуєте замовлення?", reply_markup=Keyboards.yes_cancel)


@dp.message_handler(text=ButtonText.yes, state=States.confirm)
async def h__confirm__yes(msg: Message):
    bucket = await mem.get_bucket(user=msg.from_user.id)

    order = Order(**bucket.pop('order'))
    orders = bucket.setdefault('orders', [])

    order.order_id = f"{msg.from_user.id}.{len(orders) + 1}{'F' if order.food else ''}{'M' if order.meds else ''}"
    order.date = datetime.datetime.now()

    orders.append(order.__dict__)

    await mem.set_bucket(user=msg.from_user.id, bucket=bucket)

    await msg.answer(f"Замовлення підтверджено.\n"
                     f"Номер замовлення: {order.order_id}")

    await h__any__start(msg)


@dp.message_handler(text=ButtonText.view_orders, state=States.start)
async def h__start__orders(msg: Message):
    bucket = await mem.get_bucket(user=msg.from_user.id, default={})

    orders = bucket.get('orders')

    if orders:
        for order in orders:
            await msg.answer(Order(**order).format_md(), parse_mode=aiogram.types.ParseMode.MARKDOWN_V2)
    else:
        await msg.answer('Замовлень немає.')

    await h__any__start(msg)


@dp.message_handler(state='*')
async def h__any__wrong(msg: Message, state: FSMContext = None):
    await msg.answer("Something's wrong, I can feel it.")


def main():
    async def close_db(d: Dispatcher):  # TODO remove?
        await d.storage.close()
        await d.storage.wait_closed()

    executor.start_polling(dp, on_shutdown=close_db)


if __name__ == '__main__':
    main()
