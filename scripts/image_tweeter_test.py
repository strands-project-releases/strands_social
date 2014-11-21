#! /usr/bin/env python

import rospy
import actionlib
from strands_tweets.msg import GrabImageThenTweetAction, GrabImageThenTweetGoal

class ImageTweeterTest(object):
    
    def __init__(self) :
        
        self.client = actionlib.SimpleActionClient('strands_image_tweets', GrabImageThenTweetAction)
        
        self.client.wait_for_server()
        rospy.loginfo(" ... Init done")
    
        tweet = GrabImageThenTweetGoal(text = 'Hello world', topic='head_xtion/rgb/image_mono')
        
        self.client.send_goal_and_wait(tweet)
    
        print self.client.get_result()  


if __name__ == '__main__':
    rospy.init_node('image_tweeter_test')
    ps = ImageTweeterTest()