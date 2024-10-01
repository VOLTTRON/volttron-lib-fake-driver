# -*- coding: utf-8 -*- {{{
# ===----------------------------------------------------------------------===
#
#                 Installable Component of Eclipse VOLTTRON
#
# ===----------------------------------------------------------------------===
#
# Copyright 2022 Battelle Memorial Institute
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy
# of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
#
# ===----------------------------------------------------------------------===
# }}}

import datetime
import logging
import math
import random

from collections.abc import KeysView
from math import pi
from pydantic import Field

from volttron.driver.base.interfaces import (BaseInterface, BaseRegister, BasicRevert)
from volttron.driver.base.config import PointConfig, RemoteConfig

_log = logging.getLogger(__name__)
type_mapping = {
    "string": str,
    "int": int,
    "integer": int,
    "float": float,
    "bool": bool,
    "boolean": bool
}

class FakeRemoteConfig(RemoteConfig):
    remote_id: str | None = None


class FakePointConfig(PointConfig):
    # TODO: string starting_value.
    starting_value: int | float | bool | str = Field(default='sin', alias='Starting Value')
    type: str = Field(default='string', alias='Type')


class FakeRegister(BaseRegister):

    def __init__(self, read_only, point_name, units, reg_type, default_value=None, description=''):
        #     register_type, read_only, pointName, units, description = ''):
        super(FakeRegister, self).__init__("byte", read_only, point_name, units, description='')
        self.reg_type = reg_type

        if default_value is None:
            self.value = self.reg_type(random.uniform(0, 100))
        else:
            try:
                self.value = self.reg_type(default_value)
            except ValueError:
                self.value = self.reg_type()


class EKGregister(BaseRegister):

    def __init__(self, read_only, point_name, units, reg_type, default_value=None, description=''):
        super(EKGregister, self).__init__("byte", read_only, point_name, units, description='')
        self._value = 1

        math_functions = ('acos', 'acosh', 'asin', 'asinh', 'atan', 'atan2', 'atanh', 'sin',
                          'sinh', 'sqrt', 'tan', 'tanh')
        if default_value in math_functions:
            self.math_func = getattr(math, default_value)
        else:
            _log.error('Invalid default_value in EKGregister.')
            _log.warning('Defaulting to sin(x)')
            self.math_func = math.sin

    @property
    def value(self):
        now = datetime.datetime.now()
        seconds_in_radians = pi * float(now.second) / 30.0

        yval = self.math_func(seconds_in_radians)

        return self._value * yval

    @value.setter
    def value(self, x):
        self._value = x


class Fake(BasicRevert, BaseInterface):

    REGISTER_CONFIG_CLASS = FakePointConfig
    INTERFACE_CONFIG_CLASS = FakeRemoteConfig

    def __init__(self, config: FakeRemoteConfig, *args, **kwargs):
        BasicRevert.__init__(self, **kwargs)
        BaseInterface.__init__(self, config, *args, **kwargs)

    def get_point(self, point_name, **kwargs):
        register: FakeRegister = self.get_register_by_name(point_name)
        return register.value

    def _get_multiple_points(self, topics: KeysView[str], **kwargs) -> (dict, dict):
        return BaseInterface.get_multiple_points(self, topics, **kwargs)

    def _set_point(self, point_name, value):
        register: FakeRegister = self.get_register_by_name(point_name)
        if register.read_only:
            raise RuntimeError("Trying to write to a point configured read only: " + point_name)

        register.value = register.reg_type(value)
        return register.value

    def create_register(self, register_definition: FakePointConfig) -> FakeRegister:
        read_only = register_definition.writable is not True
        description = register_definition.notes
        units = register_definition.units
        default_value = register_definition.starting_value.strip()
        if not default_value:
            default_value = None
        reg_type = type_mapping.get(register_definition.type, str)

        register_type = FakeRegister if not register_definition.volttron_point_name.startswith(
            'EKG') else EKGregister

        register = register_type(read_only,
                                 register_definition.volttron_point_name,
                                 units,
                                 reg_type,
                                 default_value=default_value,
                                 description=description)

        if default_value is not None:
            self.set_default(register_definition.volttron_point_name, register.value)
        return register

    @classmethod
    def unique_remote_id(cls, config_name: str, config: RemoteConfig) -> tuple:
        """Unique Remote ID
        Subclasses should use this class method to return a hashable identifier which uniquely identifies a single
         remote -- e.g., if multiple remotes may exist at a single IP address, but on different ports,
         the unique ID might be the tuple: (ip_address, port).
        The base class returns the name of the device configuration file, requiring a separate DriverAgent for each.
        """
        return (config_name,) if config.remote_id is None else (config.remote_id,)
