from aiogram import Router, F
from aiogram.types import Message
from database import get_id_by_username

ban_router = Router()

@ban_router.message(F.text.lower().startswith("бан"))
async def ban_user(message: Message):
    member = await message.chat.get_member(message.from_user.id)
    if member.status not in ["administrator", "creator"]:
        return await message.answer("У тебя нет прав администратора")

    user_id = None
    args = message.text.split()

    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    elif len(args) > 1 and args[1].startswith("@"):
        user_id = get_id_by_username(args[1])

    if not user_id:
        return await message.answer("Ответь на сообщение или напиши @ник.")

    try:
        await message.chat.ban(user_id=user_id)
        await message.answer("🚀 Юзер забанен.")
    except Exception:
        await message.answer("❌ Ошибка бана. Я должен быть админом.")