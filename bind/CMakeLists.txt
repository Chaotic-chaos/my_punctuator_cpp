cmake_minimum_required(VERSION 3.4...3.18)
project(punctuator)
add_definitions(-std=c++14)
add_definitions(-D_GLIBCXX_USE_CXX11_ABI=1)

find_package(Torch REQUIRED)

# target_link_libraries(punctuator "${TORCH_LIBRARIES}")
# 
add_subdirectory(pybind11)
pybind11_add_module(punctuator binding.cc)

include_directories(/root/projects/Pythons/cpp_punctuator/bind/libtorch/include)

# EXAMPLE_VERSION_INFO is defined by setup.py and passed into the C++ code as a
# define (VERSION_INFO) here.
# target_compile_definitions(punctuator
#                            PRIVATE VERSION_INFO=0.0.1)
# target_link_libraries(punctuator PUBLIC "${TORCH_LIBRARIES}")
target_compile_definitions(punctuator PUBLIC "${TORCH_LIBRARIES}")