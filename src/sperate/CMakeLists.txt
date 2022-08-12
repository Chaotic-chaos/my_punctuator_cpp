cmake_minimum_required(VERSION 3.0 FATAL_ERROR)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -g")
project(punctuator)

find_package(Torch REQUIRED)
add_subdirectory(pybind11)
pybind11_add_module(punctuator punctuator.cc)

include_directories(/root/projects/Pythons/cpp_punctuator/src/sperate/libtorch/include/)


target_compile_definitions(punctuator PUBLIC "${TORCH_LIBRARIES}")
set_property(TARGET punctuator PROPERTY CXX_STANDARD 14)