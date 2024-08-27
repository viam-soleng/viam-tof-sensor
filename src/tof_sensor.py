# Standard library
import board
import busio
import time

import subprocess
import re
from digitalio import DigitalInOut
from adafruit_vl53l0x import VL53L0X
from typing import Any, Dict, Mapping, Optional
from typing_extensions import Self

# Viam module
from viam.components.board import Board
from viam.components.sensor import Sensor
from viam.logging import getLogger
from viam.module.types import Reconfigurable, Stoppable
from viam.proto.app.robot import ComponentConfig
from viam.proto.common import ResourceName
from viam.resource.base import ResourceBase
from viam.resource.types import Model, ModelFamily

LOGGER = getLogger(__name__)

class TOFSensor(Sensor, Reconfigurable, Stoppable):
    family = ModelFamily("viam-soleng", "sensor")
    MODEL = Model(family, "tof")
    
    # --------- NEW -------- 
    @classmethod
    def new(cls, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]) -> Self:
        service = cls(config.name)
        service.validate(config)
        service.reconfigure(config, dependencies)
        return service

    # ------ VALIDATE ------- 
    @classmethod
    def validate(cls, config: ComponentConfig) -> None:
        return None

    # ----- RECONFIGURE ----- 
    def reconfigure(self, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]) -> None:

        def get_attribute_from_config(attribute_name: str, default, of_type=None):
            if attribute_name not in config.attributes.fields:
                return default

            if default is None:
                if of_type is None:
                    raise Exception(
                        "If default value is None, of_type argument can't be empty"
                    )
                type_default = of_type
            else:
                type_default = type(default)

            if type_default == bool:
                return config.attributes.fields[attribute_name].bool_value
            elif type_default == int:
                return int(config.attributes.fields[attribute_name].number_value)
            elif type_default == float:
                return config.attributes.fields[attribute_name].number_value
            elif type_default == str:
                return config.attributes.fields[attribute_name].string_value
            elif type_default == list:
                return list(config.attributes.fields[attribute_name].list_value)
            elif type_default == dict:
                return dict(config.attributes.fields[attribute_name].struct_value)
    
        # Parse config 
        self.pin_values = get_attribute_from_config("pin_values", None, list)
        self.pin_names = get_attribute_from_config("pin_names", None, list)
        self.default_address = get_attribute_from_config("default_address", "0x29", str)
        self.free_address_offset = get_attribute_from_config("free_address_offset", 7, int)

        # Open I2C and pin connections
        i2c = busio.I2C(board.SCL, board.SDA)

        power_pins = []
        for val in self.pin_values:
            power_pins.append(DigitalInOut(get_board_pin(val)))

        # Resets all sensors to have an i2c address of 0x29
        self._reset_addresses(power_pins)
        time.sleep(.5)

        # Create sensors and set address to free range (0x30-0x34)
        self.sensors = []
        self._create_sensors(i2c, power_pins)

    #  ---- GET READINGS ---- 
    async def get_readings(self, extra: Optional[Dict[str, Any]] = None, **kwargs) -> Mapping[str, Any]:
        readings = {}

        for i, sensor in enumerate(self.sensors):
            readings[self.pin_names[i]] = sensor.range

        return readings

    # ---- GET GEOMETRIES ---- 
    async def get_geometries(self):
        raise NotImplementedError


    # Reset address by turning power pins off
    def _reset_addresses(self, power_pins):
        for pin in power_pins:
            pin.switch_to_output(value = False)

    # Set sensors to new i2c addresses by turning power pins on, creating a sensor and updating its address
    def _create_sensors(self, i2c, power_pins):
        for i, pin in enumerate(power_pins):
            pin.switch_to_output(value = True)

            sensor = VL53L0X(i2c, address=int(self.default_address, 16))
            new_address = int(self.default_address, 16) + self.free_address_offset + i
            sensor.set_address(new_address)

            self.sensors.append(sensor)

            time.sleep(.5)

# Get board pins from names
def get_board_pin(pin_name):
    pin = board.D0
    if pin_name == "D0":
        pin = board.D0
    elif pin_name == "D1":
        pin = board.D1
    elif pin_name == "D2":
        pin = board.D2
    elif pin_name == "D3":
        pin = board.D3
    elif pin_name == "D4":
        pin = board.D4
    elif pin_name == "D5":
        pin = board.D5
    elif pin_name == "D6":
        pin = board.D6
    elif pin_name == "D7":
        pin = board.D7
    elif pin_name == "D8":
        pin = board.D8
    elif pin_name == "D9":
        pin = board.D9
    elif pin_name == "D10":
        pin = board.D10
    elif pin_name == "D11":
        pin = board.D11
    elif pin_name == "D12":
        pin = board.D12
    elif pin_name == "D13":
        pin = board.D13
    elif pin_name == "D14":
        pin = board.D14
    elif pin_name == "D15":
        pin = board.D15   
    elif pin_name == "D16":
        pin = board.D16
    elif pin_name == "D17":
        pin = board.D17
    elif pin_name == "D18":
        pin = board.D18
    elif pin_name == "D19":
        pin = board.D19
    else:
        pin = board.D20
    
    return pin
