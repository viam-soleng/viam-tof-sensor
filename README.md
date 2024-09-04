# TOF Range-finding Sensor (VL53L0X)

The VL53L0X sensor is attached to the i2c bus. See documentation [here](https://docs.circuitpython.org/projects/vl53l0x/en/latest/index.html).


This is a [Viam module](https://docs.viam.com/manage/configuration/#modules) for the [VL53L0X](https://www.st.com/en/imaging-and-photonics-solutions/vl53l0x.html) range-finding sensors. This module using an i2c bus to allow multiple sensors to be connected in series. The output of the sensor is in millimeters.

> [!NOTE]
> For more information on modules, see [Modular Resources](https://docs.viam.com/registry/#modular-resources).

## Configure your VL53L0X Sensor

> [!NOTE]
> Before configuring your Kuka Arm, you must [add a machine](https://docs.viam.com/fleet/machines/#add-a-new-machine).

Navigate to the **CONFIGURE** tab of your machine’s page in [the Viam app](https://app.viam.com/). Click the **+** icon next to your machine part in the left-hand menu and select **Component**. Select the `sensor` type, then search for and select the `sensor / vl53l0x` model. Click **Add module**, then enter a name or use the suggested name for your arm and click **Create**.

On the new component panel, copy and paste the following attribute template into your arm’s attributes field:

```json
{
  "pin_names": ["sensor1", "sensor2"],
  "pin_values": ["D5", "D6"],
  "default_address": "0x29",
  "free_address_offset": 7
}
```

> [!NOTE]
> For more information, see [Configure a Machine](https://docs.viam.com/build/configure/).

## Attributes

The following attributes are available:

| Name | Type | Inclusion | Default | Description |
| ---- | ---- | --------- | ------- | ----------- |
| `pin_names` | list | **Required** | N/A | A list of names for each sensor/pin. these names will be in the output struct of `GetReadings`. Note: This must have the same length as `pin_values`.  |
| `pin_values` | list | **Required**  | N/A | The board pin number of the `X_SHUT` connection to each sensor. This is used to re-register sensors away from default value. If only one sensor is used this can be anything from D1-D20. Note: This must have the same length as `pin_names`.  |
| `default_address` | string | Optional | "0x29" | The default i2c address for the sensor when turned on. For VL53L0X this is 0x29. |
| `free_address_offset` | int | Optional | 7 | The address offset to the available i2c region. The default is 7 as there is a free range from 0x30-0x34.  |

## Known Supported Hardware

Support for the following devices has been confirmed.

| Devices               | Linux (aarch64) | Linux (amd64) | 
|-----------------------|-----------------|---------------|
| Raspberry Pi 4        |         X       |        X      |

