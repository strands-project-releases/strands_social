#! /usr/bin/env python

import rospy

import actionlib
import image_branding.msg
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge


class brandingServer(object):

    _feedback = image_branding.msg.ImageBrandingFeedback()
    _result   = image_branding.msg.ImageBrandingResult()

    def __init__(self, name):
        self.cancelled = False
        self._action_name = name
        
        #self.brand_image_path = rospy.get_param("~brand_image_path",'/tmp/Tweeter_branding.png')
        rospy.loginfo("Creating action servers.")
        print self._action_name
        self._as = actionlib.SimpleActionServer(self._action_name, image_branding.msg.ImageBrandingAction, execute_cb = self.executeCallback, auto_start = False)
        self._as.register_preempt_callback(self.preemptCallback)


        rospy.loginfo(" ...starting")
        self._as.start()
        rospy.loginfo(" ...done")

        rospy.loginfo("Ready ...")

        self.photo_pub = rospy.Publisher('/nhm/twitter/image', Image, latch=True)

        rospy.spin()


        
    def executeCallback(self, goal):
        rospy.loginfo("branding...")
        self._feedback.progress = 'branding...'
        self._as.publish_feedback(self._feedback)


        result=self._brand_photo(goal)

        
        if not self.cancelled :
            self._result.success = result
            self._as.publish_feedback(self._feedback)
            self._as.set_succeeded(self._result)



    def _brand_photo(self, goal):
        self.cancelled = False

        #photo = open('/home/jaime/Linderva.png', 'rb')
        bridge = CvBridge()
        photo = bridge.imgmsg_to_cv2(goal.photo, "bgr8")
        
        #height, width, depth = photo.shape
        #print height, width, depth
        
        #cv2.imwrite('/tmp/temp_tweet.png', photo)
        brand_image_path = rospy.get_param("~brand_image_path",'/tmp/Tweeter_branding.png')
        #print "loading"
        
        bgphoto = cv2.imread(brand_image_path)
        #print "Done"

        #height, width, depth = bgphoto.shape
        #print height, width, depth
        
        dst = cv2.addWeighted(photo,1.0,bgphoto,0.7,0)

        bridge = CvBridge()
        image_message = bridge.cv2_to_imgmsg(dst, encoding="bgr8")
        
        self.photo_pub.publish(image_message)
        
        self._result.branded_image = image_message
        
        result=True
        return result


    def preemptCallback(self):
        self.cancelled = True
        self._result.success = False
        self._as.set_preempted(self._result)


if __name__ == '__main__':
    rospy.init_node('image_branding')
    server = brandingServer(rospy.get_name())
    