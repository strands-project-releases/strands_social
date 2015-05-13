#! /usr/bin/env python

import rospy


from datetime import datetime
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge


class SuperImposer(object):


    def __init__(self, name):
        
        #self.brand_image_path = rospy.get_param("~brand_image_path",'/tmp/Tweeter_branding.png')


        rospy.loginfo(" ...starting")

        self.photo_pub = rospy.Publisher('/image_superimposer/output', Image, latch=True)
        rospy.Subscriber('/head_xtion/rgb/image_color', Image, self.ImCallback)

        rospy.loginfo(" ...done")
        rospy.loginfo("Ready ...")
 
 
        rospy.spin()


    def ImCallback(self, msg):
        bridge = CvBridge()
        photo = bridge.imgmsg_to_cv2(msg, "bgr8")
        
        now = rospy.get_rostime()
        ros_time_str = "%i %i" %(now.secs, now.nsecs)
        

        dt_text=datetime.now().strftime('%A, %B %d %Y, at %H:%M:%S hours')

        height, width, depth = photo.shape
        hval = int(0.99*height)
        hval2 = int(0.05*height)
        #bridge = CvBridge()
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(photo,dt_text,(0, hval), font, 0.7,(64,64,64),2)
        cv2.putText(photo,ros_time_str,(width/2, hval2), font, 0.7,(64,64,64),2)
        #width/2
        image_message = bridge.cv2_to_imgmsg(photo, encoding="bgr8")
        image_message.header = msg.header
        self.photo_pub.publish(image_message)
        
        #self._result.branded_image = image_message
        
        #result=True
        #return result


if __name__ == '__main__':
    rospy.init_node('super_imposer')
    server = SuperImposer(rospy.get_name())
    