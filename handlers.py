from database import get_all_users
from database import save_user
from aiogram import Router, F
from aiogram.types import Message
import datetime # Понадобится для команды "время"

router = Router()


# --- ТВОЙ ИСХОДНЫЙ КОД (БЕЗ ИЗМЕНЕНИЙ) ---

# Функция 1: Сработает ТОЛЬКО на одно слово "кент"
@router.message(F.text.lower() == "кент")
async def answer_cho(message: Message):
    await message.answer("чо")
    
    
    
    

# Функция 2: Сработает ТОЛЬКО на фразу "привет кент"
@router.message(F.text.lower() == "привет кент")
async def answer_darova(message: Message):
    await message.answer(f"Дарова, {message.from_user.first_name}")
           
           
           
           
# --- НОВЫЕ ПРИМЕРЫ И ОБЪЯСНЕНИЯ ---

# 1. Действие: Информация (Пример: "Кент инфо")
# Используем .startswith(), чтобы бот реагировал, если фраза начинается с этих слов
@router.message(F.text.lower().startswith("кент инфо"))
async def info_cmd(message: Message):
    await message.answer("КЕНТ Версия 0.1.")
    
    
    
    

@router.message(F.text.lower() == "удалить")
async def delete_msg(message: Message):
    member = await message.chat.get_member(message.from_user.id)
    if member.status not in ["administrator", "creator"]:
        return await message.answer("Эту команду могут использовать только админы!")

    if message.reply_to_message:
        await message.reply_to_message.delete()
        await message.delete()
    else:
        await message.answer("Чтобы удалить, ответь этим словом на сообщение.")
        
        
        
        

# 3. Действие: Работа с данными пользователя (Пример: "мой id")
@router.message(F.text.lower() == "мой id")
async def get_id(message: Message):
    await message.answer(f"Твой ID: {message.from_user.id}")
    
    
    

# 4. Действие: Слот-машина / Рандом (Пример: "кент крути")
# Бот отправит игровой кубик (казино, дартс и т.д.)
@router.message(F.text.lower().in_(["кент деп", "кент делай"]))
async def roll_dice(message: Message):
    await message.answer_dice(emoji="🎰") # Можно менять на 🏀, 🎲, 🎯
    
@router.message(F.text.lower() == "кент список")
async def show_user_list(message: Message):
    # Проверка на админа (чтобы обычные юзеры не смотрели базу)
    member = await message.chat.get_member(message.from_user.id)
    if member.status not in ["administrator", "creator"]:
        return await message.answer("Только админ может смотреть список!")

    users = get_all_users()

    if not users:
        return await message.answer("В моей памяти пока пусто. Пусть кто-нибудь что-то напишет!")

    # Формируем текст списка
    text = "<b>📋 Чек-лист активных пользователей:</b>\n\n"
    for i, username in enumerate(users, 1):
        text += f"{i}. @{username}\n"
    
    text += f"\n<i>Всего в базе: {len(users)}</i>"
    
    await message.answer(text, parse_mode="HTML")
    
    
   # ... (предыдущий код в handlers.py)

@router.message(F.text.lower().in_(["команды", "помощь", "хелп"]))
async def help_cmd(message: Message):
    help_text = (
        "<b>🛠 Список команд:</b>\n\n"
        "<b>🚫 Модерация:</b>\n"
        "• <code>Мут @имя [мин]</code>\n"
        "• <code>Размут @имя</code>\n"
        "• <code>Бан @имя</code>\n"
        "• <code>удалить</code> — (ответом) стереть сообщение\n\n"
        "<b>📋 Инфо:</b>\n"
        "• <code>кент список</code> — список @имя ползователей доступных для ползования ботом\n"
        "• <code>мой id</code> — твой ID\n\n"
        "<b>🎰 Развлечения:</b>\n"
        "• <code>кент деп</code> — слот-машина\n"
        "<i>💡 Можно тегом или ответом!</i>"
    )
    await message.answer(help_text, parse_mode="HTML")
    
    
    
    
# 5. А в самом конце — функцию записи в базу, которая ловит ВООБЩЕ ВСЁ
@router.message()
async def monitor_users(message: Message):
    # Записываем юзера, если у него есть ник
    if message.from_user.username:
        try:
            save_user(message.from_user.id, message.from_user.username)
        except Exception as e:
            print(f"Ошибка базы: {e}")
    