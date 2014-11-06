#! /usr/bin/env python

import rospy
import sys
# Brings in the SimpleActionClient
import actionlib
import strands_tweets.msg
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

class tweet_test_client(object):
    
    def __init__(self, text, filename) :
        
        rospy.on_shutdown(self._on_node_shutdown)
        self.client = actionlib.SimpleActionClient('strands_tweets', strands_tweets.msg.SendTweetAction)
        
        self.client.wait_for_server()
        rospy.loginfo(" ... Init done")
    
        tweetgoal = strands_tweets.msg.SendTweetGoal()
    
        print "tweeting %s" %text
    
        tweetgoal.text = text
        #navgoal.origin = orig
        tweetgoal.with_photo = True
        img = cv2.imread(filename)


        bridge = CvBridge()
        image_message = bridge.cv2_to_imgmsg(img, encoding="bgr8")
        tweetgoal.photo = image_message
        
        # Sends the goal to the action server.
        self.client.send_goal(tweetgoal)
    
        # Waits for the server to finish performing the action.
        self.client.wait_for_result()
    
        # Prints out the result of executing the action
        ps = self.client.get_result()  
        print ps

    def _on_node_shutdown(self):
        self.client.cancel_all_goals()
        #sleep(2)


if __name__ == '__main__':
    print 'Argument List:',str(sys.argv)
    if len(sys.argv) < 3 :
	sys.exit(2)
    rospy.init_node('tweet_image_test')
    ps = tweet_test_client(sys.argv[1], sys.argv[2])