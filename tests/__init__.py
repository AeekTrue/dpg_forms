from datetime import datetime
import dearpygui.dearpygui as dpg
from dpg_forms import BaseForm
from dataclasses import dataclass
from pydantic import BaseModel


objs = []

class TestModel(BaseModel):
    name: str
    age: int
    registered: bool
    birth: datetime
    color: float


class CreateForm(BaseForm,
    model=TestModel,
    callback=lambda sender, o: print(o),
    type_hints_patch={'color': float}):
    pass

default_form_values = TestModel(name='asdf', age=228, registered=True, birth=datetime(2000, 9, 14), color=1)
def test():
    dpg.create_context()
    dpg.create_viewport()
    dpg.show_viewport()
    form = CreateForm(label='kek')
    form.fill(default_form_values)
    with dpg.window():
        form.add_me()
        dpg.add_button(label='Test', callback=lambda: form.fill(objs[0]))
    dpg.setup_dearpygui()
    dpg.start_dearpygui()
    dpg.destroy_context()
