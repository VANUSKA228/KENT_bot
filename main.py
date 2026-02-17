import asyncio
import os
import aiohttp  # Нужно для проверки сервера
from keep_alive import keep_alive
from aiogram import Bot, Dispatcher
from handlers import router
from mut import admin_router
from ban_commands import ban_router
from database import init_db

# Рекомендую использовать Secrets, но пока оставляем как есть
TOKEN = "8380176381:AAEp_ClwY4BuBVpe3Q27pQ_wosQxe0QU0qA"


async def check_self():
    """Проверка, отвечает ли локальный сервер Flask"""
    await asyncio.sleep(3)  # Даем Flask пару секунд на запуск
    try:
        async with aiohttp.ClientSession() as session:
            # Пытаемся зайти на локальный адрес сервера
            async with session.get('http://0.0.0.0:8080/') as response:
                if response.status == 200:
                    text = await response.text()
                    print(f"✅ Сервер Flask работает! Ответ: {text}")
                else:
                    print(f"⚠️ Сервер ответил ошибкой {response.status}")
    except Exception as e:
        print(f"❌ Ошибка проверки сервера: {e}")


async def main():
    init_db()  # Создаем базу при запуске

    # Запускаем Flask сервер
    keep_alive()

    # Проверяем его работу в фоне
    asyncio.create_task(check_self())

    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    dp.include_router(admin_router)
    dp.include_router(ban_router)
    dp.include_router(router)

    print("Кент вышел на связь...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
