#! /usr/bin/env python


import copy
import rospy
import cv2
import numpy as np
import rostopic


from datetime import datetime
from sensor_msgs.msg import Image
from std_msgs.msg import Bool
from cv_bridge import CvBridge
from std_msgs.msg import String
from mongodb_store.message_store import MessageStoreProxy

def create_blank(width, height, rgb_color=(0, 0, 0)):
    """Create new image(numpy array) filled with certain color in RGB"""
    # Create black blank image
    image = np.zeros((height, width, 3), np.uint8)

    # Since OpenCV uses BGR, convert the color first
    color = tuple(reversed(rgb_color))
    # Fill image with color
    image[:] = color

    return image


class SuperImposer(object):


    def __init__(self, name):
        
        self.censor_image_name = rospy.get_param("~censor_image_name",'no_filming')
        self.censor_image = self.load_image_from_db(self.censor_image_name)#cv2.imread(self.censor_image_path)
        self.timeout_image_name = rospy.get_param("~timeout_image_name",'off_timer')
        self.timeout_image = self.load_image_from_db(self.timeout_image_name) #cv2.imread(self.timeout_image_path)
        self.log_video=False
        self.closestNode='none'
        self.scheduled_action= 'no schedule'
        rospy.loginfo(" ...starting")

        self.photo_pub = rospy.Publisher('/image_superimposer/output', Image, latch=True)

        
        self.logtim = rospy.get_rostime()
        topics = rospy.get_published_topics()
        topics = [x[0] for x in topics]
        #print topics
        if '/current_schedule' in topics:
            toptyp = rostopic.get_topic_class('/current_schedule')
            rospy.loginfo("Subscribing to /current_schedule")
            rospy.Subscriber('/current_schedule', toptyp[0], self.scheduleCB)
        
        rospy.Subscriber('/closest_node', String, self.NodeCallback)
        rospy.Subscriber('/head_xtion/rgb/image_color', Image, self.ImCallback)
        rospy.Subscriber('/logging_manager/log', Bool, self.ManagerCB)

        rospy.loginfo(" ...done")
        rospy.loginfo("Ready ...")
 
 
        rospy.spin()


    def scheduleCB(self, msg):
        #print msg
        if msg.currently_executing:
            if len(msg.execution_queue)>0:
                self.scheduled_action = msg.execution_queue[0].action + ' @ ' + msg.execution_queue[0].start_node_id
            else:
                self.scheduled_action = 'no task'
        else:
            self.scheduled_action = 'not executing'

    def ManagerCB(self, msg):
        self.log_video= msg.data
        self.logtim = rospy.get_rostime()

    def ImCallback(self, msg):
        bridge = CvBridge()
        now = rospy.get_rostime()
        
        if (now.secs - self.logtim.secs) < 30 :
            if self.log_video :
                photo = bridge.imgmsg_to_cv2(msg, "bgr8")
            else:
                photo = copy.copy(self.censor_image)# cv2.imread(self.censor_image_path)
        else:
            photo = copy.copy(self.timeout_image) #cv2.imread(self.timeout_image_path)            
        
        
        now = rospy.get_rostime()
        ros_time_str = "%i %02i" %(now.secs, now.nsecs/10000000)
        

        dt_text=datetime.now().strftime('%a %b %d %y, %H:%M:%S')

        height, width, depth = photo.shape
        font = cv2.FONT_HERSHEY_SIMPLEX


        size1 = cv2.getTextSize(self.scheduled_action, font, 0.7, 2)
        size2 = cv2.getTextSize(ros_time_str, font, 0.7, 2)
        #print self.closestNode
        

        hval = height-5
        hval2 = size2[0][1]+3
        wval2 = width - (size2[0][0] +3)
        wval1 = width - (size1[0][0] +3)
        #bridge = CvBridge()
        
        
        cv2.putText(photo,dt_text,(3, hval), font, 0.7,(64,64,64),2)
        cv2.putText(photo,ros_time_str,(wval2, hval), font, 0.7,(64,64,64),2)
        cv2.putText(photo,self.closestNode,(3, hval2), font, 0.7,(64,64,64),2)
        cv2.putText(photo,self.scheduled_action,(wval1, hval2), font, 0.7,(64,64,64),2)
        #width/2
        image_message = bridge.cv2_to_imgmsg(photo, encoding="bgr8")
        image_message.header = msg.header
        self.photo_pub.publish(image_message)
        
        #self._result.branded_image = image_message
        
        #result=True
        #return result

    def load_image_from_db(self, name):
        msg_store = MessageStoreProxy(collection='Image_Branding')
    
        query_meta = {}
        query_meta['name'] = name
        message_list = msg_store.query(Image._type, {}, query_meta)
        
        if len(message_list) >0:
            #print message_list[0][1]
            bridge = CvBridge()
            return bridge.imgmsg_to_cv2(message_list[0][0], "bgr8")
        else:
            width, height = 640, 480
            #red = (255, 0, 0)
            image = create_blank(width, height, rgb_color=(255,255,255))
            return image

    def NodeCallback(self, msg):
        self.closestNode=msg.data
    
if __name__ == '__main__':
    rospy.init_node('super_imposer')
    server = SuperImposer(rospy.get_name())
    