from typing import Any, TYPE_CHECKING
import re

from aiogram import Router, F
from aiogram.client.bot import Bot
from aiogram.filters import Command
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.scene import SceneRegistry, ScenesManager

from src.bot.callbacks import ActionCallback, MenuCallback
from src.bot.scenes import ActionCreateScene


if TYPE_CHECKING:
    from src.repositories.alchemy.repository import ActionRepository


action_router = Router(name=__name__)

actions = ['Add action', 'Edit action', 'Show actions']
contact_menu_keyboard = InlineKeyboardBuilder()

scene_registry = SceneRegistry(action_router)
scene_registry.add(ActionCreateScene)

for action in actions:
    action_key = action.lower().replace(' ', '_')
    contact_menu_keyboard.button(
        text=action,
        callback_data=ActionCallback(
            action_slug=action_key, action_title=action).pack()
    )


@action_router.callback_query(
    MenuCallback.filter(F.section == 'actions')
)
async def send_actions_menu(
        query: CallbackQuery, callback_data: MenuCallback, bot: Bot,
        scenes: ScenesManager
    ) -> Any:
    await scenes.close()
    await bot.send_message(
        chat_id=query.message.chat.id,
        text=f'{callback_data.section_title} menu section!',
        reply_markup=contact_menu_keyboard.as_markup()
    )


action_router.callback_query.register(
    ActionCreateScene.as_handler(),
    ActionCallback.filter(F.action_slug == 'add_action')
)

action_router.message.register(
    ActionCreateScene.as_handler(),
    Command(re.compile(r'edit_action_(\w+)'))
)


@action_router.callback_query(
    ActionCallback.filter(
        ~F.instance & F.action_slug == 'show_actions')
)
async def send_actions_list(
        query: CallbackQuery, callback_data: MenuCallback, 
        action_repository: 'ActionRepository',
    ) -> Any:
    items = await action_repository.get_all_items()
    text = ''
    for item in items:
        text += f"{item.name} - {item.date} - /edit_action_{item.id}\n"
    await query.message.answer(text=text)
