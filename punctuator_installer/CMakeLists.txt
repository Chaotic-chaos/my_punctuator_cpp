cmake_minimum_required(VERSION 3.4...3.18)
project(punctuator)
set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_EXTENSIONS OFF)

get_filename_component(fc_base "fc_base" REALPATH BASE_DIR "${CMAKE_CURRENT_SOURCE_DIR}")
set(FETCHCONTENT_BASE_DIR ${fc_base})

if(NOT MSVC)
  # Keep the same with openfst, -fPIC or -fpic
  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++14 -pthread -fPIC")
else()
  set(CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS ON)
  add_compile_options("$<$<CXX_COMPILER_ID:MSVC>:/utf-8>")
endif()

# link_directories(/root/projects/Pythons/cpp_punctuator/bind/libtorch/lib)
# find_package(Torch REQUIRED)

set(PYTORCH_VERSION "1.10.0")
# set(LIBTORCH_URL "https://download.pytorch.org/libtorch/cpu/libtorch-shared-with-deps-${PYTORCH_VERSION}%2Bcpu.zip")
# set(URL_HASH "SHA256=16961222938b205a6a767b0b0b9f5e3b1f8740aa1f3475580e33cfd5952b1a44")

# set all varibles with suitable system
if(${CMAKE_SYSTEM_NAME} STREQUAL "Windows")
  if(GPU)
  message(FATAL_ERROR "GPU on Windows is unsupported, you can use CPU version")
  endif()
  if(${CMAKE_BUILD_TYPE} MATCHES "Release")
    # set(LIBTORCH_URL "https://download.pytorch.org/libtorch/cpu/libtorch-win-shared-with-deps-${PYTORCH_VERSION}%2Bcpu.zip")
    # set(URL_HASH "SHA256=d7043b7d7bdb5463e5027c896ac21b83257c32c533427d4d0d7b251548db8f4b")
    set(LIBTORCH_URL "https://download.pytorch.org/libtorch/cpu/libtorch-win-shared-with-deps-debug-${PYTORCH_VERSION}%2Bcpu.zip")
    set(URL_HASH "SHA256=d98c1b6d425ce62a6d65c16d496ef808fb2e7053d706202c536a7e437a5ade86")
  else()
    set(LIBTORCH_URL "https://download.pytorch.org/libtorch/cpu/libtorch-win-shared-with-deps-debug-${PYTORCH_VERSION}%2Bcpu.zip")
    set(URL_HASH "SHA256=d98c1b6d425ce62a6d65c16d496ef808fb2e7053d706202c536a7e437a5ade86")
  endif()
elseif(${CMAKE_SYSTEM_NAME} STREQUAL "Linux")
  if(CXX11_ABI)
    if(NOT GPU)
      set(LIBTORCH_URL "https://download.pytorch.org/libtorch/cpu/libtorch-cxx11-abi-shared-with-deps-${PYTORCH_VERSION}%2Bcpu.zip")
      set(URL_HASH "SHA256=6d7be1073d1bd76f6563572b2aa5548ad51d5bc241d6895e3181b7dc25554426")
    else()
      set(LIBTORCH_URL "https://download.pytorch.org/libtorch/${CUDA_NAME}/libtorch-cxx11-abi-shared-with-deps-${PYTORCH_VERSION}%2B${CUDA_NAME}.zip")
      set(URL_HASH "SHA256=190e963e739d5f7c2dcf94b3994de8fcd335706a4ebb333812ea7d8c841beb06")
    endif()
  else()
    if(NOT GPU)
      set(LIBTORCH_URL "https://download.pytorch.org/libtorch/cpu/libtorch-shared-with-deps-${PYTORCH_VERSION}%2Bcpu.zip")
      set(URL_HASH "SHA256=16961222938b205a6a767b0b0b9f5e3b1f8740aa1f3475580e33cfd5952b1a44")
    else()
      set(LIBTORCH_URL "https://download.pytorch.org/libtorch/${CUDA_NAME}/libtorch-shared-with-deps-${PYTORCH_VERSION}%2B${CUDA_NAME}.zip")
      set(URL_HASH "SHA256=0996a6a4ea8bbc1137b4fb0476eeca25b5efd8ed38955218dec1b73929090053")
    endif()
  endif()
endif()

include(FetchContent)
set(FETCHCONTENT_QUIET OFF)


FetchContent_Declare(
	libtorch
	URL ${LIBTORCH_URL}
	URL_HASH ${URL_HASH}
	)
FetchContent_MakeAvailable(libtorch)
find_package(Torch REQUIRED PATHS ${libtorch_SOURCE_DIR} NO_DEFAULT_PATH)
if(MSVC)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${TORCH_CXX_FLAGS}")

    file(GLOB TORCH_DLLS "${TORCH_INSTALL_PREFIX}/lib/*.dll")
    file(COPY ${TORCH_DLLS} DESTINATION ${CMAKE_BINARY_DIR})
else()
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${TORCH_CXX_FLAGS} -DC10_USE_GLOG")
endif()
add_definitions(-DUSE_TORCH)

FetchContent_Declare(gflags
  URL      https://hub.fastgit.xyz/gflags/gflags/archive/v2.2.2.zip
  URL_HASH SHA256=19713a36c9f32b33df59d1c79b4958434cb005b5b47dc5400a7a4b078111d9b5
)
FetchContent_MakeAvailable(gflags)
include_directories(${gflags_BINARY_DIR}/include)


FetchContent_Declare(
	glog
	URL      https://hub.fastgit.xyz/google/glog/archive/v0.4.0.zip
	URL_HASH SHA256=9e1b54eb2782f53cd8af107ecf08d2ab64b8d0dc2b7f5594472f3bd63ca85cdc
)
FetchContent_MakeAvailable(glog)
include_directories(${glog_SOURCE_DIR}/src ${glog_BINARY_DIR})

FetchContent_Declare(pybind11
    URL      https://hub.fastgit.xyz/pybind/pybind11/archive/refs/tags/v2.9.2.zip
    URL_HASH SHA256=d1646e6f70d8a3acb2ddd85ce1ed543b5dd579c68b8fb8e9638282af20edead8
)
FetchContent_MakeAvailable(pybind11)
add_subdirectory(${pybind11_SOURCE_DIR})
# set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++14 -pthread -fPIC")


#include(libtorch)


# link_directories(src/build)

# target_link_libraries(punctuator "${TORCH_LIBRARIES}")
# include(libtorch) 
# add_subdirectory(pybind11)
# set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++14 -pthread -fPIC")

pybind11_add_module(punctuator binding.cc)
target_link_libraries(punctuator PRIVATE torch)

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
