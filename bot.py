import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import asyncio
from main import search_track_name, main_flow
import traceback
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import SEARCH_TRACKS_COUNT

logger = logging.getLogger(__name__)

API_TOKEN = "8385919955:AAECus0D53_i1g8lP1IcP4hUyhvw1-QMJUI"

bot = Bot(token=API_TOKEN)
dp = Dispatcher()


def create_track_options_keyboard(tracks_dict, num=SEARCH_TRACKS_COUNT):
    """Создаёт Inline-клавиатуру из первых num треков словаря"""
    options = list(tracks_dict.items())[:num]
    keyboard_buttons = [
        [InlineKeyboardButton(text=track_name, callback_data=f"track:{track_url}")]
        for track_name, track_url in options
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
    return keyboard


@dp.message(Command("start"))
async def start_handler(message: types.Message):
    logger.info(f"Пользователь {message.from_user.id} запустил бота")
    await message.answer("Привет! Введи название трека для поиска")


@dp.callback_query(lambda c: c.data.startswith("track:"))
async def process_track_choice(callback_query: types.CallbackQuery):
    track_url = callback_query.data.split(":", 1)[1]  # безопаснее с split(":", 1)
    response = main_flow(track_url)
    await callback_query.message.edit_text(f"Выбран трек:\n{response}")


@dp.message()
async def handle_track_name(message: types.Message):
    track_name = message.text
    logger.info(
        f"Пользователь {message.from_user.id} отправил название трека: {track_name}"
    )

    try:
        loop = asyncio.get_running_loop()

        response = await loop.run_in_executor(None, search_track_name, track_name)

        if response["found"]:
            # Если трек найден, просто отправляем результат пользователю
            await message.answer(response["response"])
            logger.info(f"Ответ отправлен пользователю {message.from_user.id}")
        else:
            # Если не найден, создаём клавиатуру с вариантами
            keyboard = create_track_options_keyboard(response["response"])
            await message.answer(
                "Выберите трек из похожих вариантов:", reply_markup=keyboard
            )
            logger.info(f"Ответ отправлен пользователю {message.from_user.id}")

    except Exception as e:
        logger.error(f"Ошибка в обработчике трека: {e}\n{traceback.format_exc()}")
        await message.answer("Произошла ошибка при обработке запроса.")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
