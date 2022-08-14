cmake_minimum_required(VERSION 3.4...3.18)
project(punctuator)
add_definitions(-std=c++14)

# link_directories(/root/projects/Pythons/cpp_punctuator/bind/libtorch/lib)
# find_package(Torch REQUIRED)

set(PYTORCH_VERSION "1.10.0")
set(LIBTORCH_URL "https://download.pytorch.org/libtorch/cpu/libtorch-shared-with-deps-${PYTORCH_VERSION}%2Bcpu.zip")
set(URL_HASH "SHA256=16961222938b205a6a767b0b0b9f5e3b1f8740aa1f3475580e33cfd5952b1a44")

include(FetchContent)
set(FETCHCONTENT_QUIET OFF)


FetchContent_Declare(
	libtorch
	URL ${LIBTORCH_URL}
	URL_HASH ${URL_HASH}
	)
FetchContent_MakeAvailable(libtorch)
find_package(Torch REQUIRED PATHS ${libtorch_SOURCE_DIR} NO_DEFAULT_PATH)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${TORCH_CXX_FLAGS} -DC10_USE_GLOG")


FetchContent_Declare(glog
	  URL      https://github.com/google/glog/archive/v0.4.0.zip
	  URL_HASH SHA256=9e1b54eb2782f53cd8af107ecf08d2ab64b8d0dc2b7f5594472f3bd63ca85cdc
 )
FetchContent_MakeAvailable(glog)
include_directories(${glog_SOURCE_DIR}/src ${glog_BINARY_DIR})

FetchContent_Declare(pybind11
    URL      https://github.com/pybind/pybind11/archive/refs/tags/v2.9.2.zip
    URL_HASH SHA256=d1646e6f70d8a3acb2ddd85ce1ed543b5dd579c68b8fb8e9638282af20edead8
)
FetchContent_MakeAvailable(pybind11)
add_subdirectory(${pybind11_SOURCE_DIR})
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++14 -pthread -fPIC")


#include(libtorch)


link_directories(src/build)

# target_link_libraries(punctuator "${TORCH_LIBRARIES}")
# include(libtorch) 
# add_subdirectory(pybind11)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++14 -pthread -fPIC")

pybind11_add_module(punctuator binding.cc)
target_link_libraries(punctuator PRIVATE ${TORCH_LIBRARIES})

#include_directories(/root/projects/Pythons/cpp_punctuator/bind/libtorch/include)


# EXAMPLE_VERSION_INFO is defined by setup.py and passed into the C++ code as a
# define (VERSION_INFO) here.
# target_compile_definitions(punctuator
#                            PRIVATE VERSION_INFO=0.0.1)
# target_link_libraries(punctuator PRIVATE libtorch)
# set_property(TARGET Torch PROPERTY IMPORTED_LOCATION /root/projects/Pythons/cpp_punctuator/bind/libtorch/lib/libtorch.so)
# add_library(Torch SHARED IMPORTED)
#target_compile_definitions(punctuator PUBLIC "${TORCH_LIBRARIES}")
# target_link_libraries(punctuator PUBLIC torch)
# target_link_libraries(punctuator PUBLIC torch asmjit backend_with_compiler benchmark caffe2_protos clog cpuinfo cpuinfo_internals dnnl dnnl_graph fbgemm fbjni fmt foxi_loader gloo gmock gmock_main jitbackend_test nnapi_backend nnpack nnpack_reference_layers onnx onnx_proto protobuf protobuf-lite protoc pthreadpool pytorch_jni pytorch_qnnpack nnpack shm tensorpipe tensorpipe_uv torchbind_test torch_cpu torch_global_deps torch_python XNNPACK)
