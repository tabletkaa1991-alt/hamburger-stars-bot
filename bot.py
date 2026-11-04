from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message

import payments
from db import create_order

router = Router()

RATE = 1.55
PACKAGES = [50, 100, 250, 500, 1000]


def price(stars):
    return stars * RATE


class OrderForm(StatesGroup):
    username = State()


def buy_kb():
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="⭐ Купить звёзды", callback_data="buy")]]
    )


def packages_kb():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f"{s} ⭐ — {price(s):.2f} ₽", callback_data=f"pkg:{s}")]
            for s in PACKAGES
        ]
    )


@router.message(CommandStart())
async def start(message: Message):
    await message.answer("👋 Привет! Нажми кнопку, чтобы купить звёзды:", reply_markup=buy_kb())


@router.callback_query(F.data == "buy")
async def buy(call: CallbackQuery):
    await call.message.edit_text("Выбери пакет:", reply_markup=packages_kb())
    await call.answer()


@router.callback_query(F.data.startswith("pkg:"))
async def pick(call: CallbackQuery, state: FSMContext):
    stars = int(call.data.split(":")[1])
    await state.update_data(stars=stars)
    await state.set_state(OrderForm.username)
    await call.message.answer(f"Пакет: {stars} ⭐ за {price(stars):.2f} ₽\n\nВведи @username:")
    await call.answer()


@router.message(OrderForm.username)
async def username(message: Message, state: FSMContext):
    data = await state.get_data()
    stars = data["stars"]
    name = message.text.strip().lstrip("@")
    order_id = create_order(message.from_user.id, name, f"s{stars}", stars, price(stars))
    await state.clear()

    url = payments.create_payment(order_id, price(stars), f"{stars} звёзд для @{name}")
    text = f"Заказ #{order_id} создан. Оплати картой:\n{url}" if url else f"Заказ #{order_id} создан. Платёжка не подключена."
    await message.answer(text, reply_markup=buy_kb())
