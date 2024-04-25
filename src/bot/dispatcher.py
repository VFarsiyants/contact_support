from aiogram import Bot, Dispatcher, html, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.storage.memory import SimpleEventIsolation

from src.settings import bot_settings
from src.repositories.alchemy.repository import (ContactRepository,
                                                 ActionRepository)

from .routers import action_router, contacts_router
from .keyboards import main_menu_keyboard_builder
from .callbacks import MenuCallback


# Bot token can be obtained via https://t.me/BotFather
TOKEN = bot_settings.BOT_TOKEN

# All handlers should be attached to the Router (or Dispatcher)
dp = Dispatcher(
    events_isolation=SimpleEventIsolation(),
)

dp.include_router(action_router)
dp.include_router(contacts_router)

# Inject your dependencies here
dp['contact_repository'] = ContactRepository
dp['action_repository'] = ActionRepository


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    await message.answer(
        f"Hello, {html.bold(message.from_user.full_name)}! "
        + 'Please select desired section',
        reply_markup=main_menu_keyboard_builder.as_markup()
    )


@dp.callback_query(MenuCallback.filter(F.section == 'main_menu'))
async def main_menu_hanled(query: CallbackQuery):
    await command_start_handler(query.message)


async def run_bot() -> None:
    # Initialize Bot instance with default bot
    # properties which will be passed to all API calls
    bot = Bot(
        token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    # And the run events dispatching
    await dp.start_polling(bot)
