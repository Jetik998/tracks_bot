import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import asyncio
from main import search_track_name, main_flow
import traceback
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import logic


logger = logging.getLogger(__name__)

API_TOKEN = "8385919955:AAECus0D53_i1g8lP1IcP4hUyhvw1-QMJUI"

bot = Bot(token=API_TOKEN)
dp = Dispatcher()


tracks_dict_global = {}


def create_track_options_keyboard(num=5):
    global tracks_dict_global
    """Создаёт Inline-клавиатуру из первых num треков словаря"""
    options = list(tracks_dict_global.items())[:num]
    keyboard_buttons = [
        [InlineKeyboardButton(text=track_name, callback_data=f"track:{i}")]
        for i, (track_name, _) in enumerate(options, 1)
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
    return keyboard


async def handle_track_selection(callback_query: types.CallbackQuery):
    """
    Обрабатывает нажатие кнопки трека в Telegram-боте.

    Фильтрует callback-запросы по префиксу 'track:', извлекает имя трека,
    ищет URL в глобальном словаре и отправляет пользователю результат
    или сообщение об ошибке, если URL не найден.
    """
    # фильтруем только нужные callback_data
    if not callback_query.data or not callback_query.data.startswith("track:"):
        return

    track_name = callback_query.data.split("track:")[1]
    i = int(track_name)
    track_name = list(tracks_dict_global.keys())[i]
    track_url = tracks_dict_global.get(track_name)
    logic.input_track = track_name
    logger.info("В БОТЕ(logic.input_track = track_name): %s", track_name)

    if track_url:
        response = main_flow(track_url)
        await callback_query.message.answer(response)
    else:
        await callback_query.message.answer("Ошибка: URL трека не найден.")


# регистрируем обработчик
dp.callback_query.register(handle_track_selection)


@dp.message(Command("start"))
async def start_handler(message: types.Message):
    logger.info(f"Пользователь {message.from_user.id} запустил бота")
    await message.answer("Привет! Введи название трека для поиска")


@dp.message()
async def handle_track_name(message: types.Message):
    track_name = message.text
    logger.info(
        f"Пользователь {message.from_user.id} отправил название трека: {track_name}"
    )

    try:
        loop = asyncio.get_running_loop()

        search_tracks = await loop.run_in_executor(None, search_track_name, track_name)

        if search_tracks["found"]:
            # Если трек найден, просто отправляем результат пользователю
            await message.answer(search_tracks["response"])
            logger.info(f"Ответ отправлен пользователю {message.from_user.id}")
        else:
            global tracks_dict_global
            tracks_dict_global = search_tracks["response"]
            # Если не найден, создаём клавиатуру с вариантами
            keyboard = create_track_options_keyboard()
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
