cmake_minimum_required(VERSION 3.13)
project(ClapackTest CXX)

find_package(CLAPACK MODULE REQUIRED)

add_executable(example example.cpp)
target_link_libraries(example CLAPACK::CLAPACK)
