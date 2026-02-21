import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardMarkup, InlineKeyboardButton,
    FSInputFile
)
from aiogram.filters import Command

# ====== ТОКЕН ИЗ RENDER ======
TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

# ====== ТОВАРЫ ======
products = {
    "hat1": {
        "category": "hats",
        "name": "Детская шапка",
        "price": 299,
        "photo": "hat1.jpg"
    },
    "suit1": {
        "category": "suits",
        "name": "Мужской костюм",
        "price": 1599,
        "photo": "suit1.jpg"
    },
    "shoes1": {
        "category": "shoes",
        "name": "Кроссовки",
        "price": 1899,
        "photo": "shoes1.jpg"
    },
    "bag1": {
        "category": "bags",
        "name": "Сумка",
        "price": 899,
        "photo": "bag1.jpg"
    },
    "baby1": {
        "category": "baby",
        "name": "Комплект для новорожденного",
        "price": 799,
        "photo": "baby1.jpg"
    },
    "socks1": {
        "category": "underwear",
        "name": "Набор носков",
        "price": 399,
        "photo": "socks1.jpg"
    }
}

# ====== ГЛАВНОЕ МЕНЮ ======
main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🧢 Детские шапки"), KeyboardButton(text="👕 Мужские костюмы")],
        [KeyboardButton(text="👟 Обувь"), KeyboardButton(text="👜 Кошельки, сумки")],
        [KeyboardButton(text="👶 Товары для новорожденных"), KeyboardButton(text="🧦 Носки, трусы, колготы")]
    ],
    resize_keyboard=True
)

# ====== START ======
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Добро пожаловать в магазин 🔥", reply_markup=main_kb)

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

# ====== ПОКАЗ ТОВАРОВ ======
async def show_products(message, category):
    found = False

    for product_id, product in products.items():
        if product["category"] == category:
            found = True

            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(
                        text="🛒 Купить",
                        callback_data=f"buy_{product_id}"
                    )]
                ]
            )

            photo = FSInputFile(product["photo"])

            await message.answer_photo(
                photo=photo,
                caption=f"{product['name']}\nЦена: {product['price']} грн",
                reply_markup=keyboard
            )

    if not found:
        await message.answer("В этой категории пока нет товаров.")

# ====== ЗАПУСК ======
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())