from database import get_id_by_username
from aiogram import Router, F
from aiogram.types import Message, ChatPermissions
import datetime

admin_router = Router()

@admin_router.message(F.text.lower().startswith("мут"))
async def mute_user(message: Message):
    # Проверка: является ли отправитель админом
    member = await message.chat.get_member(message.from_user.id)
    if member.status not in ["administrator", "creator"]:
        return await message.answer("Эту команду могут использовать только админы!")

    user_id = None
    args = message.text.split()
    
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    elif len(args) > 1 and args[1].startswith("@"):
        user_id = get_id_by_username(args[1])

    if not user_id:
        return await message.answer("Ответь на сообщение или тегни через @.") 

    minutes = 10
    for arg in args:
        if arg.isdigit():
            minutes = int(arg)
            break

    until_date = datetime.datetime.now() + datetime.timedelta(minutes=minutes)

    try:
        await message.chat.restrict(
            user_id=user_id,
            permissions=ChatPermissions(can_send_messages=False), 
            until_date=until_date
        )
        await message.answer(f"✅ притих на {minutes} мин.") 
    except Exception:
        await message.answer("❌ Ошибка прав. Проверь, что я админ, а цель — нет.") 

@admin_router.message(F.text.lower().startswith("размут"))
async def unmute_user(message: Message):
    member = await message.chat.get_member(message.from_user.id)
    if member.status not in ["administrator", "creator"]:
        return await message.answer("Только админы могут размучивать!")

    user_id = None
    args = message.text.split()

    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id 
    elif len(args) > 1 and args[1].startswith("@"):
        user_id = get_id_by_username(args[1])

    if not user_id:
        return await message.answer("Тегни или ответь на сообщение.") 

    try:
        await message.chat.restrict(
            user_id=user_id,
            permissions=ChatPermissions(
                can_send_messages=True, 
                can_send_media_messages=True,
                can_send_other_messages=True,
                can_add_web_page_previews=True
            )
        )
        await message.answer("✅ Голос возвращен.") 
    except Exception:
        await message.answer("❌ Не вышло размутить.")