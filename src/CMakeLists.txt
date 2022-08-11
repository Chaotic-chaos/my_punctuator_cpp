cmake_minimum_required(VERSION 3.0 FATAL_ERROR)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -g")
project(punctuator_cpp)

find_package(Torch REQUIRED)

add_executable(punctuator_cpp deve.cc)
target_link_libraries(punctuator_cpp "${TORCH_LIBRARIES}")
set_property(TARGET punctuator_cpp PROPERTY CXX_STANDARD 14)