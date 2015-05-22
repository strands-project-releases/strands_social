#! /usr/bin/env python

import rospy
import sys
from time import sleep

import actionlib
import yaml

from random import randint
#from threading import Timer

import strands_tweets.msg
import image_branding.msg


from std_msgs.msg import String
from sensor_msgs.msg import Image
#from cv_bridge import CvBridge, CvBridgeError
#import dynamic_reconfigure.client



class read_and_tweet(object):

    def __init__(self, filename):
#        rospy.on_shutdown(self._on_node_shutdown)

        self.msg_sub = rospy.Subscriber('/socialCardReader/commands', String, self.command_callback, queue_size=1)

        self.client = actionlib.SimpleActionClient('strands_tweets', strands_tweets.msg.SendTweetAction)
        self.brandclient = actionlib.SimpleActionClient('/image_branding', image_branding.msg.ImageBrandingAction)


        self.client.wait_for_server()
        self.brandclient.wait_for_server()
        text_file = open(filename, "r")
        
        texts = yaml.load(text_file)
        self.tweets_texts = texts['tweets']['card']
        #self.tw_pub = rospy.Publisher('/card_image_tweet/tweet', card_image_tweet.msg.Tweet)

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
       
            text = self.tweets_texts[randint(0, len(self.tweets_texts)-1)]
            
            #text = "Look who is here"
            print "tweeting %s" %text
    
            brandgoal.photo = msg
            self.brandclient.send_goal(brandgoal)
            self.brandclient.wait_for_result()
            br_ph = self.brandclient.get_result()
    
       
            tweetgoal.text = text
            tweetgoal.with_photo = True
            tweetgoal.photo = br_ph.branded_image

            self.client.send_goal(tweetgoal)

   
            #self.client.wait_for_result()
            #ps = self.client.get_result()
            #print ps
            sleep(10)   
            self.msg_sub = rospy.Subscriber('/socialCardReader/commands', String, self.command_callback, queue_size=1)
    




if __name__ == '__main__':
    if len(sys.argv) < 2 :
        print "usage: tweet_card file_texts.yaml"
	sys.exit(2)

    filename=str(sys.argv[1])
    
    rospy.init_node('card_image_tweet')
    ps = read_and_tweet(filename)
    rospy.spin()