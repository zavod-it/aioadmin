from aiogram import Router
from aiogram.types import Message
from aiogram.enums.parse_mode import ParseMode

from aioadmin.adapter import Adapter


get_table_router = Router(name=__name__)


@get_table_router.message()
async def get_table(message: Message, adapter: Adapter):
    await message.answer("```\n" + repr(await adapter.get_table(message.text)) + "\n```", parse_mode=ParseMode.MARKDOWN)