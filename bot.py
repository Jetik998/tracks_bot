import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import asyncio
from main import main_flow
import traceback

logger = logging.getLogger(__name__)

API_TOKEN = "8385919955:AAECus0D53_i1g8lP1IcP4hUyhvw1-QMJUI"

bot = Bot(token=API_TOKEN)
dp = Dispatcher()


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
        pairs_list = await loop.run_in_executor(None, main_flow, track_name)

        before_tracks = [name for name in pairs_list[0] if name is not None]
        after_tracks = [name for name in pairs_list[1] if name is not None]

        before_str = (
            "Before (Предыдущий):\n" + "\n".join(before_tracks)
            if before_tracks
            else "Before: нет треков"
        )
        after_str = (
            "After (Следующий):\n" + "\n".join(after_tracks)
            if after_tracks
            else "After: нет треков"
        )

        response = f"{before_str}\n\n{after_str}"
        await message.answer(response)
        logger.info(f"Ответ отправлен пользователю {message.from_user.id}")

    except Exception as e:
        logger.error(f"Ошибка в обработчике трека: {e}\n{traceback.format_exc()}")
        await message.answer("Произошла ошибка при обработке запроса.")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
