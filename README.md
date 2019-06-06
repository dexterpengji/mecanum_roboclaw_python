# mecanum_roboclaw_python
A ROS pkg using 2 roboclaws to drive 4 mecanum wheels.

### This pkg accepts topics below:
* cmd_vel
* a vector of 4 speeds for 4 wheels

### Before using this pkg:
1. update your firmware of roboclaw to the latest version
2. make sure that you wired roboclaws to your computer/MCU exactly same as the diagram on [roboclaw_user_manual.pdf](http://downloads.ionmc.com/docs/roboclaw_user_manual.pdf)
3. make sure that you have already set up your roboclaws correctly using BasicmicroMotionStudio(Read the roboclaw_user_manual.pdf carefully)

### After the above works:
1. clone this pkg to you catkin_ws/src
2. then use catkin_make or catkin_make_isolated (--install[optional], --use-ninja[optional]) to compile.
3. start your roscore
4. source catkin_ws(your work space)/devel/setup.bash
5. rosrun mecanum_roboclaw_python mecanum_listener.py

### Enjoy!
