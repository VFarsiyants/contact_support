from aiogram.filters.callback_data import CallbackData


class MenuCallback(CallbackData, prefix="menu"):
    section: str = ''
    section_title: str = ''
    cancel: str = 'cancel'


class ActionCallback(CallbackData, prefix=""):
    action_slug: str
    action_title: str
    instance: int | None = None
