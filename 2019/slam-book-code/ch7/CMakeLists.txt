cmake_minimum_required(VERSION 3.11)

find_package(OpenCV REQUIRED)
include_directories(${OpenCV_INCLUDE_DIRS})

add_executable(feature_extraction feature_extraction.cpp)
add_executable(pose_estimation_2d2d pose_estimation_2d2d.cpp)
add_executable(triangulation triangulation.cpp)

target_link_libraries(feature_extraction ${OpenCV_LIBS})
target_link_libraries(pose_estimation_2d2d ${OpenCV_LIBS})
target_link_libraries(triangulation ${OpenCV_LIBS})