#!/usr/bin/env python


import rospy

import strands_tweets.msg
import sensor_msgs.msg #import Image

from mongodb_store.message_store import MessageStoreProxy


class logTweets(object):


    def __init__(self, name):

        rospy.loginfo(" ...starting")

        self.msg_sub = rospy.Subscriber('/strands_tweets/tweet', strands_tweets.msg.Tweeted, self.tweet_callback, queue_size=1)

        rospy.loginfo(" ...done")


        rospy.spin()

    def tweet_callback(self, msg) :
        self.msg_store = MessageStoreProxy(collection='twitter_log')
        
        to_save = strands_tweets.msg.Tweeted()
        try:
            to_save.depth = rospy.wait_for_message('/head_xtion/depth/image_rect_meters', sensor_msgs.msg.Image, timeout=1.0)
        except rospy.ROSException :
           rospy.logwarn("Failed to get camera depth Image")


        try:
            to_save.photo = rospy.wait_for_message('/head_xtion/rgb/image_color', sensor_msgs.msg.Image, timeout=1.0)
        except rospy.ROSException :
            rospy.logwarn("Failed to get camera rgb Image")

        to_save.text = msg.text
        
        meta = {}
        meta["Description"] = "copy of tweeted images"
        self.msg_store.insert(msg, meta)



if __name__ == '__main__':
    rospy.init_node('log_tweets')
    server = logTweets(rospy.get_name())