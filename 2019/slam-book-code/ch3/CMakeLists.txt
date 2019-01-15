cmake_minimum_required(VERSION 2.8)
project(useEigenGeometry)

include_directories("/usr/include/eigen3")
add_executable(useGeometry useGeometry.cpp)
