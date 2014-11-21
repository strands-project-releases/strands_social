cmake_minimum_required(VERSION 2.8.3)
project(card_image_tweet)

## Find catkin macros and libraries
## if COMPONENTS list like find_package(catkin REQUIRED COMPONENTS xyz)
## is used, also find other catkin packages
find_package(catkin REQUIRED COMPONENTS
  actionlib
  cv_bridge
  fake_camera_effects
  image_branding
  rospy
  sensor_msgs
  social_card_reader
  std_msgs
  strands_tweets
)


## Uncomment this if the package has a setup.py. This macro ensures
## modules and global scripts declared therein get installed
## See http://ros.org/doc/api/catkin/html/user_guide/setup_dot_py.html
# catkin_python_setup()

################################################
## Declare ROS messages, services and actions ##
################################################

#add_message_files(
#  FILES
#  Tweet.msg
#)

## Generate added messages and services with any dependencies listed here
#generate_messages(
#  DEPENDENCIES
#  sensor_msgs
#)

###################################
## catkin specific configuration ##
###################################

## The catkin_package macro generates cmake config files for your package
## Declare things to be passed to dependent projects

catkin_package(
#  INCLUDE_DIRS include
#  LIBRARIES card_image_tweet
#  CATKIN_DEPENDS actionlib cv_bridge fake_camera_effects image_branding rospy sensor_msgs social_card_reader std_msgs strands_tweets
#  DEPENDS system_lib
)

###########
## Build ##
###########

include_directories(
  ${catkin_INCLUDE_DIRS}
)

#############
## Install ##
#############

## Mark executable scripts (Python etc.) for installation
## in contrast to setup.py, you can choose the destination
 install(PROGRAMS
   scripts/tweet_card.py
   DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
 )


