# Standard library
import board
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
    
    @classmethod
    def new(cls, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]) -> Self:
        service = cls(config.name)
        service.validate(config)
        service.reconfigure(config, dependencies)
        return service

    @classmethod
    def validate(cls, config: ComponentConfig) -> None:
        return None

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
    
        # Extract config info
        board_name = get_attribute_from_config("board", None, str)
        self.board = dependencies[Board.get_resource_name(board_name)]

        name_to_gpio_map = get_attribute_from_config("gpio_map", None, dict)
        self.gpio_pins = []
        self.sensor_names = []
        for key, value in name_to_gpio_map:
            self.gpio_pins.append(key)
            self.sensor_names.append(value)

        # Define board
        self.i2c = board.I2C()

        # Define and initialize xShut pins
        pins = []
        for gpio_pin in self.gpio_pins:
            pin = DigitalInOut(gpio_pin)

            pins.append(pin)
            pin.switch_to_output(value=False)
        
        # Define TOF sensors (VL53L0X)
        self.sensors = []
        for i, pin in enumerate(pins):
            pin.value = True
            self.sensors.insert(i, VL53L0X(self.i2c))

            if i < len(self.pins) - 1:
                self.sensors[i].set_address(i + 0x30)

    async def get_readings(self, extra: Optional[Dict[str, Any]] = None, **kwargs) -> Mapping[str, Any]:
        readings = {}

        # Iterate through sensors
        for i, sensor in self.sensors:
            readings[self.sensor_names[i]] = sensor.range

        return readings

    async def get_geometries(self):
        raise NotImplementedError
    