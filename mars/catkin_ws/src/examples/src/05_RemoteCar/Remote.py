#!/usr/bin/env python
from Input import KBHit

#define variables
has_ros = True
kb = None

#try to import ros python package
try:
	import rospy
	from examples.msg import WheelsCmd
	print("Rospy found")
except ImportError:
	print("Rospy not found")
	hasRos = False

#if no rospy
def no_ROS():
	print('Hit any key, or ESC to exit')
	while True:
		if kb.kbhit():
			c = kb.getch()
			if ord(c) == 27: # ESC
				break
			print(c)

	kb.set_normal_term()

#if there's rospy
import threading
pressedChar = None

def parseCmd():
	if pressedChar == None:
		return 0.0, 0.0
	else:
		if pressedChar == 'w':
			return 1.0, 1.0
		elif pressedChar == 's':
			return -1.0, -1.0
		elif pressedChar == 'a':
			return -0.5, 0.5
		elif pressedChar == 'd':
			return 0.5, -0.5
		else:
			return 0.0, 0.0

def has_ROS():
	rospy.init_node('remote', anonymous=True)
	pub = rospy.Publisher('wheelCmd', WheelsCmd, queue_size=1)
	rate = rospy.Rate(10) #10hz

	#ros main publish loop
	while not rospy.is_shutdown():
		global pressedChar
		if kb.kbhit():
			pressedChar = kb.getch()
		else:
			pressedChar = None
		msg = WheelsCmd()
		msg.vel_left, msg.vel_right = parseCmd()
		pub.publish(msg)
		rate.sleep()

def main():
	global kb
	kb = KBHit()
	if has_ros:
		has_ROS()
	else:
		no_ROS()

if __name__ == "__main__":
	main()

