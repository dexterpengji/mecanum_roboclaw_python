#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import String
from std_msgs.msg import UInt32MultiArray

def mecanum_enCounter_arr():
	pub = rospy.Publisher('mecanum_enCounter_arr', String, queue_size=10)
	rospy.init_node('mecanum_enCounter_arr_node', anonymous=True)
	rate = rospy.Rate(10) # 10hz
	while not rospy.is_shutdown():
		hello_str = "try %s" % rospy.get_time()
		rospy.loginfo(hello_str)
		pub.publish(hello_str)
		rate.sleep()
		
if __name__ == '__main__':
	try:
		mecanum_enCounter_arr()
	except rospy.ROSInterruptException:
		pass
