#!/usr/bin/env python
import cv2
import numpy as np
hasRos = True
try:
    import rospy
    from sensor_msgs.msg import Image
    from cv_bridge import CvBridge, CvBridgeError
    from examples.msg import example02
    print("Found ROS")
except ImportError:
    print("Rospy not found")
    hasRos = False

def track(image):
    # Blur the image to reduce noise
    blur = cv2.GaussianBlur(image, (5,5),0)

    # Convert BGR to HSV
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

    #target color HSV range
    lower_red_range1 = np.array([0, 70, 50])
    upper_red_range1 = np.array([10, 255, 255])
    lower_red_range2 = np.array([170, 70, 50])
    upper_red_range2 = np.array([180, 255, 255])

    #red has two range!
    mask1 = cv2.inRange(hsv, lower_red_range1, upper_red_range1)/255.0
    mask2 = cv2.inRange(hsv, lower_red_range2, upper_red_range2)/255.0
    #culling method to get union
    mask = ((1-mask1) * mask2 + mask1) * 255.0
    
    # Blur the mask
    bmask = cv2.GaussianBlur(mask, (5,5), 0)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(3, 3))
    #Morphological opening remove small pieces
    bmask = cv2.erode(bmask, kernel, iterations=5)
    bmask = cv2.dilate(bmask, kernel, iterations=7)
    #Morphological closing fill the small holes
    bmask = cv2.dilate(bmask, kernel)  
    bmask = cv2.erode(bmask, kernel)

    # Take the moments to get the centroid
    #https://blog.csdn.net/kuweicai/article/details/79027388
    moments = cv2.moments(bmask)
    m00 = moments['m00']
    centroid_x, centroid_y = None, None
    if m00 >= 100: #100 means red dominate 100pixels area
        centroid_x = int(moments['m10']/m00)
        centroid_y = int(moments['m01']/m00)

    # Assume no centroid
    ctr = (-1,-1)

    # Use centroid if it exists
    if centroid_x != None and centroid_y != None:
        ctr = (centroid_x, centroid_y)

        # Put black circle in at centroid in image
        cv2.circle(image, ctr, 4, (255,255,255), -1)

    
    # Return coordinates of centroid
    return ctr, bmask, image

def noROS_main():
    capture = cv2.VideoCapture(0)
    while True:
        okay, image = capture.read()
        if okay:

            ctr, _, _ = track(image)
            print(ctr)
            if cv2.waitKey(1) & 0xFF == 27:
                break
        else:
           print('Capture failed')
           break
    capture.release()

def ROS_main():
    rospy.init_node('Color_Tracker', anonymous=True)
    pub = rospy.Publisher('Tracker_Info', example02, queue_size=10)
    rate = rospy.Rate(10) #10hz
    capture = cv2.VideoCapture(0)
    bridge = CvBridge()
    while not rospy.is_shutdown():
        okay, image = capture.read()
        if okay:
            ctr, bmask, res = track(image)
            msg = example02()
            msg.centroidX = ctr[0]
            msg.centroidY = ctr[1]
            msg.mask = bridge.cv2_to_imgmsg(bmask)
            msg.result = bridge.cv2_to_imgmsg(image)
            pub.publish(msg)
            rate.sleep()
            
        
# Test with input from camera
if __name__ == '__main__':
    if hasRos:
        try:
            ROS_main()
        except rospy.ROSInterruptException:
            pass
    else:
        noROS_main()
        
    
       
             
        
