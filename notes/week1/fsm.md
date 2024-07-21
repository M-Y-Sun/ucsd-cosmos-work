# Finite State Machines

### Input Devices in Python

The Python `evdev` module is used to interface with an input device.
An instance of an `InputDevice` requires the path to an input device in the form of
`/dev/inputs/eventx` where `x` is the numbered input device. i.e.

```py
gamepad = InputDevice("/dev/inputs/event0")
```

An `InputDevice` has a `stdout` operator that displays information (e.g. IPv6, name, path).

### Motor Movement

- A motor has three states: CW, CCW, and coast, which means it cannot be controlled with a single electrical signal with values of only `0` or `1`.
- A motor driver (specifically an H-bridge) controls the motor speed and direction.
  - Takes in power from the batteries and pins
  - Controlled with the `AIN1` and `AIN2` pins described by a truth table,
    which are outputted to the `AO1` and `AO2` (connected to the motors).
- To drive our robot we need to set the `AIN1`/`AIN2` pins to the mode we want
  and give a PWM value from 0 to 100 to control the motor speed.
- The frequency of a PWM determines the speed of the motor by changing the ratio between the current being on and off.
  e.g. a 90% PWM would cause faster movement than a 50% PWM (water wheel being open 90% of the time).

## FSMs

<i>Finite State Machines (FSM)</i> are a programming paradigm for control flow based on various possible inputs and various possible actions (states).
FSMs have <i>no memory</i>.

- One of the oldest programming concepts for creating automata
  - A Turing machine is an example of a complex FSM.

#### Diagram Conventions

- The possible states of a machine are represented as circles
- Transitions between those states are drawn as arrows
  - Transitions occur due to an action (e.g. button press) and thus have a label on the arrows

1. List all possible states the robot can be in.
2. Find how the states transition between each other.
