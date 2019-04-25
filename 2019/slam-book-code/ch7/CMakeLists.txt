cmake_minimum_required(VERSION 3.11)

find_package(OpenCV REQUIRED)
include_directories(${OpenCV_INCLUDE_DIRS})

find_package(CSparse REQUIRED)
include_directories(${CSPARSE_INCLUDE_DIR})

find_package( G2O REQUIRED )
include_directories( 
    ${G2O_INCLUDE_DIRS}
    "/usr/include/eigen3"
)

add_executable(feature_extraction feature_extraction.cpp)
add_executable(pose_estimation_2d2d pose_estimation_2d2d.cpp)
add_executable(triangulation triangulation.cpp)
add_executable(pose_estimation_3d2d pose_estimation_3d2d.cpp)
add_executable(pose_estimation_3d2d_ba pose_estimation_3d2d_ba.cpp)

target_link_libraries(feature_extraction ${OpenCV_LIBS})
target_link_libraries(pose_estimation_2d2d ${OpenCV_LIBS})
target_link_libraries(triangulation ${OpenCV_LIBS})
target_link_libraries(pose_estimation_3d2d ${OpenCV_LIBS})
target_link_libraries(pose_estimation_3d2d_ba g2o_core g2o_stuff ${OpenCV_LIBS})