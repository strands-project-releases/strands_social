#! /usr/bin/env python

import rospy
import sys

from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge
from mongodb_store.message_store import MessageStoreProxy

class LoadImage(object):

    def __init__(self, path, image_name):

        rospy.loginfo(" ...starting")
        msg_store = MessageStoreProxy(collection='Image_Branding')
        
        image = cv2.imread(path)
        bridge = CvBridge()
        image_message = bridge.cv2_to_imgmsg(image, encoding="bgr8")
        meta={}
        meta['name'] = image_name
        msg_store.insert(image_message,meta)
        
        rospy.loginfo(" ...done")



    def preemptCallback(self):
        self.cancelled = True
        self._result.success = False
        self._as.set_preempted(self._result)


if __name__ == '__main__':
    if len(sys.argv) < 3 :
        print "usage: load_image_in_db input_file.png image_name"
        sys.exit(2)

    filename=str(sys.argv[1])
    name=str(sys.argv[2])
    
    rospy.init_node('image_loader')
    server = LoadImage(filename, name)
    #server = LoadImage('/home/jaime/deploy_ws/src/strands_social/image_branding/resources/nofilming.jpg', 'no_filming')