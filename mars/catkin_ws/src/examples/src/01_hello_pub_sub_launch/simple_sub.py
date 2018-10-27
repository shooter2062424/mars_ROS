#!/usr/bin/env python
import rospy
from std_msgs.msg import String

def callback(data):
    rospy.loginfo(data.data)

def main():
    rospy.init_node('python_hello_sub_node')
    sub = rospy.Subscriber('hello', String, callback)
    #run until this node is done
    rospy.spin()

if __name__ == '__main__':
    main()
