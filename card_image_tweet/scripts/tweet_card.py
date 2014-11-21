#! /usr/bin/env python

import rospy
import sys
from time import sleep

import actionlib
#import json

#from random import randint
#from threading import Timer

import strands_tweets.msg
import image_branding.msg
import card_image_tweet.msg

#import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import dynamic_reconfigure.client
#import nhm.srv


class read_and_tweet(object):

    def __init__(self):
#        rospy.on_shutdown(self._on_node_shutdown)

        self.msg_sub = rospy.Subscriber('/socialCardReader/commands', String, self.command_callback, queue_size=1)

        self.client = actionlib.SimpleActionClient('strands_tweets', strands_tweets.msg.SendTweetAction)
        self.brandclient = actionlib.SimpleActionClient('/image_branding', image_branding.msg.ImageBrandingAction)


        self.client.wait_for_server()
        self.brandclient.wait_for_server()

        self.tw_pub = rospy.Publisher('/card_image_tweet/tweet', card_image_tweet.msg.Tweet)

        rospy.loginfo(" ... Init done")


    def command_callback(self, msg):
        command_msg = msg.data
        if command_msg == 'PHOTO' :
            self.msg_sub.unregister()
            #/head_xtion/depth/image_rect_meters #store this
            try:
                msg = rospy.wait_for_message('/head_xtion/rgb/image_color', Image, timeout=1.0)
            except rospy.ROSException :
                rospy.logwarn("Failed to get camera rgb Image")
            
            tweetgoal = strands_tweets.msg.SendTweetGoal()
            brandgoal = image_branding.msg.ImageBrandingGoal()
       
            #text = tweets[randint(0, len(tweets)-1)]
            text = "Look who is here"
            print "tweeting %s" %text
    
            brandgoal.photo = msg
            self.brandclient.send_goal(brandgoal)
            self.brandclient.wait_for_result()
            br_ph = self.brandclient.get_result()
    
   
    
            tweetgoal.text = text
            tweetgoal.with_photo = True
            tweetgoal.photo = br_ph.branded_image

            self.client.send_goal(tweetgoal)

            tweettext=card_image_tweet.msg.Tweet()
            tweettext.text = text
            tweettext.photo = br_ph.branded_image
            self.tw_pub.publish(tweettext)
    
            self.client.wait_for_result()
            ps = self.client.get_result()
            print ps
            sleep(10)   
            self.msg_sub = rospy.Subscriber('/socialCardReader/commands', String, self.command_callback, queue_size=1)
    




if __name__ == '__main__':
    rospy.init_node('card_image_tweet')
    ps = read_and_tweet()
    rospy.spin()