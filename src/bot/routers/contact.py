from typing import Any, TYPE_CHECKING
import re

from aiogram import Router, F
from aiogram.client.bot import Bot
from aiogram.filters import Command
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.scene import SceneRegistry, ScenesManager

from src.bot.callbacks import ActionCallback, MenuCallback
from src.bot.scenes import ContactCreateScene


if TYPE_CHECKING:
    from src.repositories.alchemy.repository import ContactRepository


contacts_router = Router(name=__name__)

actions = ['Add contact', 'Edit contact', 'Show contacts']
contact_menu_keyboard = InlineKeyboardBuilder()

scene_registry = SceneRegistry(contacts_router)
scene_registry.add(ContactCreateScene)

for action in actions:
    action_key = action.lower().replace(' ', '_')
    contact_menu_keyboard.button(
        text=action,
        callback_data=ActionCallback(
            action_slug=action_key, action_title=action).pack()
    )


@contacts_router.callback_query(
    MenuCallback.filter(F.section == 'contacts')
)
async def send_contacts_menu(
        query: CallbackQuery, callback_data: MenuCallback, bot: Bot,
        scenes: ScenesManager
    ) -> Any:
    await scenes.close()
    await bot.send_message(
        chat_id=query.message.chat.id,
        text=f'{callback_data.section_title} menu section!',
        reply_markup=contact_menu_keyboard.as_markup()
    )


contacts_router.callback_query.register(
    ContactCreateScene.as_handler(),
    ActionCallback.filter(F.action_slug == 'add_contact')
)

contacts_router.message.register(
    ContactCreateScene.as_handler(),
    Command(re.compile(r'edit_contact_(\d+)'))
)


@contacts_router.callback_query(
    ActionCallback.filter(
        ~F.instance & F.action_slug == 'show_contacts')
)
async def send_contacts_list(
        query: CallbackQuery, callback_data: MenuCallback, 
        contact_repository: 'ContactRepository',
    ) -> Any:
    items = await contact_repository.get_all_items()
    text = ''
    for item in items:
        text += f"{item.fullname} - {item.phone} - /edit_contact_{item.id}"
    await query.message.answer(text=text)
