cmake_minimum_required(VERSION 2.8)
project(useEigen)

include_directories("/usr/include/eigen3")
add_executable(eigenMatrix eigenMatrix.cpp)
