# Merlin_Gerin_PM500
A library for reading values ​​from Merlin Gerin PM500 via Modbus RS485 (Module: Merlin Gerin 50982 RS485 MODBUS)

# Example

```python
from PM500 import PM500

pm500 = PM500(port='/dev/ttyACM2', baudrate=19200, unit_id=1, currentScale=1/5)
if pm500.check_connection():
	print(pm500)
	print("Single phase:  ", pm500.getSinglePhase())
	print("THD:           ", pm500.getSinglePhaseTHD())
	print("Voltage:       ", pm500.getVoltage())
	print("Current:       ", pm500.getCurrent())
	print("Power:         ", pm500.getTotalPower())
	print("Active power:  ", pm500.getActivePower())
	print("Reactive power:", pm500.getReactivePower())
	print("Apparent power:", pm500.getApparentPower())
	print("Energy:        ", pm500.getEnergy())
	print("Cosfi:         ", pm500.getCosfi())
	print("Freq:          ", pm500.getFrequency())
	print("Hour:          ", pm500.getHour())
	print("THD:           ", pm500.getTHD())
	print("\nTotal active power: {:.2f} kW".format(pm500.getTotalPower()['P']))
	print("Total reactive power: {:.2f} kVAr".format(pm500.getTotalPower()['Q']))
	print("Cosfi: {:.3f}".format(pm500.getCosfi()['Cosfi tot']))
	pm500.disconnect()
else:
	print("Non connesso") 

```
Result of executing the above code:
```
PM500 port: /dev/ttyACM2, baudrate: 19200, unit_id: 1, Connected: True
Single phase:      {'U': 236.44, 'I': 0.1236, 'P': 0.028, 'Q': 0.006, 'S': 0.028, 'Cosfi': 0.97}
Single phase THD:  {'THD U': 0.028, 'THD I': 0.164}
Voltage:           {'U12': 0.0, 'U23': 0.0, 'U31': 0.0, 'U1': 236.44, 'U2': 0.0, 'U3': 0.0}
Current:           {'I1': 0.618, 'I2': 0.0, 'I3': 0.0, 'In': 0.0}
Power:             {'P': 0.14, 'Q': 0.03, 'S': 0.14}
Active power:      {'P1': 0.14, 'P2': 0.0, 'P3': 0.0}
Reactive power:    {'Q1': 0.03, 'Q2': 0.0, 'Q3': 0.0}
Apparent power:    {'S1': 0.14, 'S2': 0.0, 'S3': 0.0}
Energy:            {'E active': 0, 'E reactive': 0, 'E apparent': 0, 'E active-': 0, 'E reactive-': 0}
Cosfi:             {'Cosfi tot': 0.97, 'Cosfi 1': 0.97, 'Cosfi 2': 1.0, 'Cosfi 3': 1.0}
Freq:              50.0
Hour:              0.45
THD:               {'THD U12': 0.0, 'THD U23': 0.0, 'THD U31': 0.0, 'THD U1': 0.028, 'THD U2': 0.0, 'THD U3': 0.0, 'THD I1': 0.164, 'THD I2': 0.0, 'THD I3': 0.0, 'THD In': 0.0}

Total active power: 0.14 kW
Total reactive power: 0.03 kVAr
Cosfi: 0.976

```
The unit of measurement are:
```
Voltage:        Volt
Current:        A
Power:          kW, kVAr, kVA
Active power:   kW
Reactive power: kVAr
Apparent power: kVA
Energy:         kWh, kVARh, kVAh
Cosfi:          Unitless
Freq:           Herz
Hour:           Hour
THD:            Unitless
```
