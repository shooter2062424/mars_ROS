#!/usr/bin/env python
import rospy
from std_msgs.msg import String

def main():
    try:
        rospy.init_node('python_hello_pub_node')
        pub = rospy.Publisher('hello', String, queue_size=10)
        rate = rospy.Rate(10)
        while not rospy.is_shutdown():
            pub.publish("hello")
            rate.sleep()
    except rospy.ROSInterruptException:
        print("So sad")

if __name__ == '__main__':
    main()


