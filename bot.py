import asyncio
import csv
from datetime import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardMarkup, InlineKeyboardButton,
    FSInputFile
)
from aiogram.filters import Command
import os
TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)
ADMIN_ID = 7217992539

bot = Bot(token=TOKEN)
dp = Dispatcher()

# ====== ТОВАРЫ ======

products = {
    "hat1": {
        "category": "hats",
        "name": "Детская шапка",
        "price": 299,
        "photo": "hat1.jpg",
        "sizes": ["48", "50", "52"]
    },
    "suit1": {
        "category": "suits",
        "name": "Мужской костюм",
        "price": 1599,
        "photo": "suit1.jpg",
        "sizes": ["S", "M", "L", "XL"]
    },

    # 👟 ОБУВЬ
    "shoes1": {
        "category": "shoes",
        "name": "Кроссовки мужские",
        "price": 1899,
        "photo": "shoes1.jpg",
        "sizes": ["40", "41", "42", "43"]
    },

    # 👜 СУМКИ
    "bag1": {
        "category": "bags",
        "name": "Мужская сумка",
        "price": 899,
        "photo": "bag1.jpg",
        "sizes": ["Стандарт"]
    },

    # 👶 НОВОРОЖДЕННЫЕ
    "baby1": {
        "category": "baby",
        "name": "Комплект для новорожденного",
        "price": 799,
        "photo": "baby1.jpg",
        "sizes": ["0-3 мес", "3-6 мес"]
    },

    # 🧦 НОСКИ / БЕЛЬЁ
    "socks1": {
        "category": "underwear",
        "name": "Набор носков",
        "price": 399,
        "photo": "socks1.jpg",
        "sizes": ["36-39", "40-43"]
    }
}

# ====== МЕНЮ ======

main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🧢 Детские шапки"),
         KeyboardButton(text="👕 Мужские костюмы")],
        [KeyboardButton(text="👟 Обувь"),
         KeyboardButton(text="👜 Кошельки, сумки")],
        [KeyboardButton(text="👶 Товары для новорожденных"),
         KeyboardButton(text="🧦 Носки, трусы, колготы")],
        [KeyboardButton(text="🛒 Корзина")]
    ],
    resize_keyboard=True
)

user_state = {}
user_cart = {}

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Добро пожаловать 🔥", reply_markup=main_kb)

# ====== КАТЕГОРИИ ======

@dp.message(lambda m: m.text == "🧢 Детские шапки")
async def show_hats(message: types.Message):
    await show_products(message, "hats")

@dp.message(lambda m: m.text == "👕 Мужские костюмы")
async def show_suits(message: types.Message):
    await show_products(message, "suits")

@dp.message(lambda m: m.text == "👟 Обувь")
async def show_shoes(message: types.Message):
    await show_products(message, "shoes")

@dp.message(lambda m: m.text == "👜 Кошельки, сумки")
async def show_bags(message: types.Message):
    await show_products(message, "bags")

@dp.message(lambda m: m.text == "👶 Товары для новорожденных")
async def show_baby(message: types.Message):
    await show_products(message, "baby")

@dp.message(lambda m: m.text == "🧦 Носки, трусы, колготы")
async def show_underwear(message: types.Message):
    await show_products(message, "underwear")

@dp.message(lambda m: m.text == "🛒 Корзина")
async def show_cart(message: types.Message):
    ...

            photo = FSInputFile(product["photo"])

            await message.answer_photo(
                photo=photo,
                caption=f"{product['name']}\nЦена: {product['price']} грн",
                reply_markup=keyboard
            )

# ====== ВЫБОР ТОВАРА ======

@dp.callback_query(lambda c: c.data.startswith("buy_"))
async def choose_size(callback: types.CallbackQuery):
    product_id = callback.data.split("_")[1]
    product = products[product_id]

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text=size,
                callback_data=f"size_{product_id}_{size}"
            )] for size in product["sizes"]
        ]
    )

    await callback.message.answer("Выберите размер:", reply_markup=keyboard)
    await callback.answer()

@dp.callback_query(lambda c: c.data.startswith("size_"))
async def add_to_cart(callback: types.CallbackQuery):
    _, product_id, size = callback.data.split("_")
    user_id = callback.from_user.id

    if user_id not in user_cart:
        user_cart[user_id] = []

    user_cart[user_id].append({
        "product_id": product_id,
        "size": size
    })

    await callback.message.answer("Товар добавлен в корзину ✅")
    await callback.answer()

# ====== КОРЗИНА ======

@dp.message(lambda m: m.text and "корзина" in m.text.lower())
async def show_cart(message: types.Message):
    user_id = message.from_user.id

    if user_id not in user_cart or not user_cart[user_id]:
        await message.answer("Корзина пустая.")
        return

    text = "🛒 Ваша корзина:\n\n"
    total = 0

    for item in user_cart[user_id]:
        product = products[item["product_id"]]
        text += f"{product['name']} | Размер: {item['size']} | {product['price']} грн\n"
        total += product["price"]

    text += f"\nИтого: {total} грн"

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text="Оформить заказ",
                callback_data="checkout"
            )]
        ]
    )

    await message.answer(text, reply_markup=keyboard)

# ====== ОФОРМЛЕНИЕ ======

@dp.callback_query(lambda c: c.

data == "checkout")
async def start_checkout(callback: types.CallbackQuery):
    user_state[callback.from_user.id] = {"step": "name"}
    await callback.message.answer("Введите имя:")
    await callback.answer()

@dp.message()
async def process_order(message: types.Message):
    user_id = message.from_user.id

    if user_id not in user_state:
        return

    state = user_state[user_id]

    if state["step"] == "name":
        state["name"] = message.text
        state["step"] = "phone"
        await message.answer("Введите телефон:")
        return

    if state["step"] == "phone":
        state["phone"] = message.text
        state["step"] = "city"
        await message.answer("Введите город:")
        return

    if state["step"] == "city":
        state["city"] = message.text
        state["step"] = "warehouse"
        await message.answer("Введите отделение Новой Почты:")
        return

    if state["step"] == "warehouse":
        state["warehouse"] = message.text

        cart = user_cart.get(user_id, [])
        text = "🔥 Новый заказ!\n\n"

        total = 0
        for item in cart:
            product = products[item["product_id"]]
            text += f"{product['name']} | Размер: {item['size']} | {product['price']} грн\n"
            total += product["price"]

        text += f"\nИтого: {total} грн\n\n"
        text += f"Имя: {state['name']}\n"
        text += f"Телефон: {state['phone']}\n"
        text += f"Город: {state['city']}\n"
        text += f"Отделение: {state['warehouse']}"

        await bot.send_message(ADMIN_ID, text)
        await message.answer("Заказ оформлен ✅")

        user_cart[user_id] = []
        del user_state[user_id]

async def main():
    await dp.start_polling(bot)

import os

if __name__ == "__main__":
    TOKEN = os.getenv("BOT_TOKEN")
    asyncio.run(main())