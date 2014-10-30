cmake_minimum_required(VERSION 2.8.3)
project(datamatrix_read)

## Find catkin macros and libraries
## if COMPONENTS list like find_package(catkin REQUIRED COMPONENTS xyz)
## is used, also find other catkin packages
find_package(catkin REQUIRED COMPONENTS
  cv_bridge
  image_transport
  roscpp
  sensor_msgs
  std_msgs
)


###################################
## catkin specific configuration ##
###################################
## The catkin_package macro generates cmake config files for your package
## Declare things to be passed to dependent projects
## INCLUDE_DIRS: uncomment this if you package contains header files
## LIBRARIES: libraries you create in this project that dependent projects also need
## CATKIN_DEPENDS: catkin_packages dependent projects also need
## DEPENDS: system dependencies of this project that dependent projects also need
catkin_package(
  INCLUDE_DIRS include
#  LIBRARIES datamatrix_read
#  CATKIN_DEPENDS actionlib actionlib_msgs cv_bridge image_transport message_generation roscpp sensor_msgs std_msgs
#  DEPENDS system_lib
)

###########
## Build ##
###########

include_directories(
  ${catkin_INCLUDE_DIRS}
)

add_executable(data_matrix_node src/data_matrix.cpp src/dataimage.cpp)

add_dependencies(data_matrix_node ${catkin_EXPORTED_TARGETS})

target_link_libraries(data_matrix_node
   dmtx
   ${catkin_LIBRARIES}
)

#############
## Install ##
#############

install(TARGETS data_matrix_node
	RUNTIME DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

