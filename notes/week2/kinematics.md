# Robotic Kinematics

Kinematics is the mathematical description of something's spatial orientation and movement.
This study is very useful for planning the motion of a robot.

The robots used in Cluster 10 are <i>differential drive</i> robots because there are
two independent motors controlling its motion.

### Wheels

Wheels leverage friction to move. When we are planning motion, we assume that the wheels don't slip.
Specifically, the center of the wheel is only allowed to move in the forward and backward
direction of the wheel's orientation. This means that the velocity vector can only point in the direction of the wheel.

# Introduction to Control

Control is the field of analyzing <i>dynamic systems</i>

- A dynamic system is a system that varies in time and is influenced by external forces
- Control systems typically use feedback to stablize the behavior of a dynamic system.
- <i>Negative feedback</i> is feedback that we use to stablize something.

### Proportional Control

Proportional control controls something in a degree in proportion to some heuristic.

$$\omega = -k_p \Delta E$$

Where $\omega$ is the turning rate, $k_p$ is the proportionality constant, and $\Delta E$ is the error from the target.

For example, if there is a sticky note to the far left, the robot turns fast to the left,
and as the sticky note gets closer, the turn speed slows down.

Practicallly, proportional control itself will cause the system to never reach its goal since error, and therefore speed, approaches zero when time approaches infinity.

### PID

Stands for proportional - integral - derivative.

- <b>Proportional:</b> uses proportional control
- <b>Integral:</b> graphs the curve of the errors over time and uses that instead of the current error.
- <b>Derivative:</b> the difference between the errors and history of errors.
