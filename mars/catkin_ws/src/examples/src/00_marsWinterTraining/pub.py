#!/usr/bin/env python
import rospy
from std_msgs.msg import Bool

def main():
	b = True
	try:
		rospy.init_node('python_hello_pub_node')
		pub = rospy.Publisher('cmd', Bool, queue_size=1)
		rate = rospy.Rate(1)
		while not rospy.is_shutdown():
			pub.publish(b)
			b = not b
			rate.sleep()
	except rospy.ROSInterruptException:
		print("So sad")

if __name__ == '__main__':
	main()


