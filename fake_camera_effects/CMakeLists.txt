cmake_minimum_required(VERSION 2.8.3)
project(fake_camera_effects)

find_package(catkin REQUIRED COMPONENTS
  actionlib
  actionlib_msgs
  message_generation
  rospy
  scitos_msgs
  sensor_msgs
  std_msgs
)

catkin_python_setup()

################################################
## Declare ROS messages, services and actions ##
################################################

add_action_files(
  DIRECTORY action
  FILES
  CameraEffects.action
)

 generate_messages(
   DEPENDENCIES
   actionlib_msgs
   std_msgs
 )

###################################
## catkin specific configuration ##
###################################
catkin_package(
  CATKIN_DEPENDS
  actionlib
  actionlib_msgs
  rospy
  scitos_msgs
  sensor_msgs
  sound_play
  std_msgs
)

#############
## Install ##
#############

install(PROGRAMS
  scripts/fake_camera.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

install(DIRECTORY sounds
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)

install(DIRECTORY launch 
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)
