import dearpygui.dearpygui as dpg
from typing import Callable, get_type_hints
from datetime import datetime


type_field_mapping = {
    str: dpg.add_input_text,
    int: dpg.add_input_int,
    float: dpg.add_input_double,
    bool: dpg.add_checkbox,
    datetime: dpg.add_date_picker
}


class BaseForm:
    Model: type
    field_types: dict
    submit_callback: Callable

    def __init_subclass__(cls, model, callback, type_hints_patch=None) -> None:
        cls.Model = model
        cls.field_types = get_type_hints(model)
        if type_hints_patch is not None:
            cls.field_types.update(type_hints_patch)
        cls.submit_callback = callback

    def __init__(self, label=''):
        self.field_ids = []
        self.field_names = []
        with dpg.stage() as self._staging_containter_id:
            with dpg.group(label=label) as group_id:
                for field_name in self.field_types:
                    field_type = self.field_types[field_name]
                    dpg_field = type_field_mapping.get(field_type)
                    if dpg_field is not None:
                        field_id = dpg_field(label=field_name.capitalize())
                        self.field_ids.append(field_id)
                        self.field_names.append(field_name)
                    else:
                        raise TypeError(f'Unsupported field type {field_type}')
                self.submit_button = dpg.add_button(label='Submit', callback=self.submit_form)

    def submit_form(self, sender, app_data, user_data):
        raw_values = {n: v for n, v in zip(self.field_names, dpg.get_values(self.field_ids))}
        o = self.Model(**raw_values)
        self.submit_callback(o)

    def add_me(self):
        dpg.unstage(self._staging_containter_id)

    def fill(self, obj):
        for field_name in self.field_types:
            if hasattr(obj, field_name):
                value = getattr(obj, field_name)
                field_id = self.field_ids[self.field_names.index(field_name)]
                dpg.set_value(field_id, value)
