#!/usr/bin/env python
# license removed for brevity
import rospy
import time
from std_msgs.msg import Int32MultiArray
from std_msgs.msg import UInt16
from geometry_msgs.msg import Twist
from roboclaw import Roboclaw as motorDriver

# control mode
global control_modes, control_mode_chosen, sign_stoped
control_modes = ["autonav_A", "break_B", "gamepad_X", "Y"]	# 0123-ABXY buttons on gamepad
control_mode_chosen = 1
sign_stoped = 0

# autonav parameters
global cmd_vel_linear_x_gain,	cmd_vel_linear_y_gain,	cmd_vel_angular_z_gain
cmd_vel_linear_x_gain  = 5000
cmd_vel_linear_y_gain  = 5000
cmd_vel_angular_z_gain = 5000

# print out settings
print("control_mode: " + control_modes[control_mode_chosen])

def callback_control_mode(data):
	global control_mode_chosen, sign_stoped
	control_mode_chosen = data.data
	if control_mode_chosen == 1 and sign_stoped == 0:
		rc.SpeedAccelM1M2(add_motorDriver_front,16000,0,-0)
		rc.SpeedAccelM1M2(add_motorDriver_rear, 16000,0,-0)
		sign_stoped = 1
	rospy.loginfo(rospy.get_caller_id() + "control_mode: %s", control_modes[data.data])

def callback_cmd_vel_mecanum(data):
	if control_mode_chosen == 2:
		rc.SpeedAccelM1M2(add_motorDriver_front,data.data[4], data.data[1], data.data[0])	#acceleration, M1_speed(right_front), M2_speed(left_front)
		rc.SpeedAccelM1M2(add_motorDriver_rear, data.data[5], data.data[3], data.data[2])	#acceleration, M1_speed(right_back),  M2_speed(left_back)
		rospy.loginfo(rospy.get_caller_id() + "cmd_vel_mecanum: %s", data.data)

def callback_cmd_vel(data):
	if control_mode_chosen == 0:
		speed_right_front =    int(data.linear.y*cmd_vel_linear_y_gain - data.linear.x*cmd_vel_linear_x_gain + data.angular.z*cmd_vel_angular_z_gain)
		speed_left_front  = -1*int(data.linear.y*cmd_vel_linear_y_gain + data.linear.x*cmd_vel_linear_x_gain - data.angular.z*cmd_vel_angular_z_gain)
		speed_right_back  =    int(data.linear.y*cmd_vel_linear_y_gain + data.linear.x*cmd_vel_linear_x_gain + data.angular.z*cmd_vel_angular_z_gain)
		speed_left_back   = -1*int(data.linear.y*cmd_vel_linear_y_gain - data.linear.x*cmd_vel_linear_x_gain - data.angular.z*cmd_vel_angular_z_gain)
		rc.SpeedAccelM1M2(add_motorDriver_front,16000, speed_right_front, speed_left_front)	#acceleration, M1_speed(right_front), M2_speed(left_front)
		rc.SpeedAccelM1M2(add_motorDriver_rear, 16000, speed_right_back,  speed_left_back)	#acceleration, M1_speed(right_back),  M2_speed(left_back)
		rospy.loginfo(rospy.get_caller_id() + "cmd_vel(linear/angular): %s", [data.linear, data.angular])

def listener():
	rospy.init_node('vel_mecanum_listener', anonymous=True)
	rospy.Subscriber("control_mode", UInt16, callback_control_mode)
	rospy.Subscriber("cmd_vel_mecanum", Int32MultiArray, callback_cmd_vel_mecanum)		# control from tprobot_roboclaw_teleop
	rospy.Subscriber("cmd_vel", Twist, callback_cmd_vel)								# control from autonav
	print(time.time())
	rospy.spin()

if __name__ == '__main__':
	# roboclaw motor driver init.
	rc = motorDriver("/dev/ttyTHS2",115200)
	rc.Open()
	add_motorDriver_front = 0x80
	add_motorDriver_rear = 0x81
	
	# stop all motors
	rc.SpeedAccelM1M2(add_motorDriver_front,8000,0,-0)
	rc.SpeedAccelM1M2(add_motorDriver_rear, 8000,0,-0)
	listener()
