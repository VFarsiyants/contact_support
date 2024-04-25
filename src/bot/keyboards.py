from aiogram.utils.keyboard import InlineKeyboardBuilder
from .callbacks import MenuCallback

sections = ['Contacts', 'Actions', 'Activity Codes']
main_menu_keyboard_builder = InlineKeyboardBuilder()

for section in sections:
    sections_key = section.lower().replace(' ', '_')
    main_menu_keyboard_builder.button(
        text=section,
        callback_data=MenuCallback(
            section=sections_key, section_title=section).pack()
    )
