import asyncio
from keep_alive import keep_alive
from aiogram import Bot, Dispatcher
from handlers import router
from mut import admin_router
from ban_commands import ban_router
from database import init_db

TOKEN = "8380176381:AAEp_ClwY4BuBVpe3Q27pQ_wosQxe0QU0qA"

async def main():
    init_db()  # Создаем базу при запуске
    keep_alive()
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_router(admin_router)
    dp.include_router(ban_router)
    dp.include_router(router)
    
    
    print("Кент вышел на с вязь...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())