import dearpygui.dearpygui as dpg
from typing import Callable, get_type_hints
from datetime import datetime


def datetime_from_date_picker_value(value):
    return datetime(value['year']+1900, value['month']+1, value['month_day'])

def date_picker_value_from_datetime(value: datetime):
    return {'year': value.year - 1900, 'month': value.month - 1, 'month_day': value.day}

type_field_mapping = {
    str: dpg.add_input_text,
    int: dpg.add_input_int,
    float: dpg.add_input_double,
    bool: dpg.add_checkbox,
    datetime: dpg.add_date_picker
}

default_adapters = {
    datetime: datetime_from_date_picker_value
}

default_fillers = {
    datetime: date_picker_value_from_datetime
}

class BaseForm:
    Model: type
    field_types: dict
    field_names: list
    field_ids: list
    submit_callback: Callable
    value_adapters: dict
    def __init_subclass__(cls, model, callback,
        type_hints_patch=None,
        value_adapters=None) -> None:
        cls.Model = model
        cls.field_types = get_type_hints(model)
        if type_hints_patch is not None:
            cls.field_types.update(type_hints_patch)

        cls.value_adapters = dict()
        if value_adapters is not None:
            cls.value_adapters.update(value_adapters)
        cls.submit_callback = callback

    def __init__(self, label=''):
        self.field_ids = []
        self.field_names = []
        with dpg.stage() as self._staging_containter_id:
            with dpg.group(label=label) as group_id:
                for field_name in self.field_types.keys():
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
        raw_values = {n: self.adapt_value(n, v) for n, v in zip(self.field_names, dpg.get_values(self.field_ids))}
        o = self.Model(**raw_values)
        self.submit_callback(o)

    def adapt_value(self, field_name, value):
        adapter = self.value_adapters.get(field_name) or default_adapters.get(self.field_types[field_name])
        if adapter is not None:
            return adapter(value)
        else:
            return value

    def add_me(self):
        dpg.unstage(self._staging_containter_id)

    def fill(self, obj):
        for field_name in self.field_types:
            if hasattr(obj, field_name):
                value = getattr(obj, field_name)
                self.fill_value(field_name, value)

    def fill_value(self, field_name, value):
        field_id = self.field_ids[self.field_names.index(field_name)]
        filler = default_fillers.get(self.field_types[field_name])
        if filler is not None:
            value = filler(value)
        print('Fill', field_id, value)
        dpg.set_value(field_id, value)
