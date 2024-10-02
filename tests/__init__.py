from datetime import datetime
import dearpygui.dearpygui as dpg
from dpg_forms import BaseForm
from dataclasses import dataclass

objs = []

@dataclass
class TestModel:
    name: str
    age: int
    registered: bool
    birth: datetime
    color: tuple[int, int, int]


class CreateForm(BaseForm,
    model=TestModel,
    callback=lambda sender, o: objs.append(o),
    type_hints_patch={'color': float}):
    pass

def test():
    dpg.create_context()
    dpg.create_viewport()
    dpg.show_viewport()
    form = CreateForm(label='kek')
    with dpg.window():
        form.add_me()
        dpg.add_button(label='Test', callback=lambda: form.fill(objs[0]))
    dpg.setup_dearpygui()
    dpg.start_dearpygui()
    dpg.destroy_context()
