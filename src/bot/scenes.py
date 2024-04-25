from aiogram import F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.scene import Scene, on
from pydantic import BaseModel

from src.repositories.entries import ContactEntry, ActionEntry
from src.repositories.alchemy.repository import ContactRepository, ActionRepository


# TODO need to find more elegant solution to generate create scene
def build_create_scene(
        state: str, repository, entry_class: BaseModel):
    scene_steps = []
    for key, value in entry_class.model_fields.items():
        if key == 'id':
            continue
        scene_steps.append({
            'field': key,
            'prompt_message': value.json_schema_extra['prompt']
        })

    class CreateScene(Scene, state=state):
        """Class represents contacts create section"""
        @on.callback_query.enter()
        async def on_enter(
                self, query: CallbackQuery,
                state: FSMContext, step: int | None = 0):
            try:
                field_data = scene_steps[step]
            except IndexError:
                return await self.wizard.exit()
            await state.update_data(step=step)
            await query.message.answer(
                field_data['prompt_message'],
            )
            # add cancel button and return to main section menu logic

        @on.message.enter()
        async def _on_enter(
                self, message, state: FSMContext, step: int | None = 0):
            try:
                field_data = scene_steps[step]
            except IndexError:
                return await self.wizard.exit()
            
            text: str = message.text
            if text.startswith('/edit'):
                instance_id = text.split('_')[-1]
                await state.update_data(raw_data={
                    'id': instance_id
                })
            await state.update_data(step=step)
            await message.answer(
                field_data['prompt_message'],
            )

        @on.message.exit()
        async def on_exit(self, message: Message, state: FSMContext) -> None:
            data = await state.get_data()
            raw_data = data.get('raw_data', {})
            # TODO add pydantic validation
            try:
                entry = entry_class(**raw_data)
            except ValueError:
                await state.set_state({})
                await message.answer('Object was not saved')
                return
            if entry.id:
                await repository.update(entry.dict())
            else:
                await repository.insert_objects(entry.dict())
            await message.answer('Object was saved')
            await state.set_state({})

        @on.message(F.text)
        async def answer(self, message: Message, state: FSMContext) -> None:
            # TODO add pydantic validation
            data = await state.get_data()
            step = data["step"]
            raw_data = data.get('raw_data', {})
            field = scene_steps[step]['field']
            raw_data[field] = message.text
            await state.update_data(raw_data=raw_data)
            await self.wizard.retake(state=state, step=step + 1)

    return CreateScene


ContactCreateScene = build_create_scene(
    'create_contact', ContactRepository, ContactEntry)

ActionCreateScene = build_create_scene(
    'create_action', ActionRepository, ActionEntry)
