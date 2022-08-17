include_directories(/root/projects/Pythons/cpp_punctuator/bind/libtorch/include)

add_library(punctuator_cpp STATIC punctuator.cc)
target_link_libraries(punctuator_cpp PUBLIC ${TORCH_LIBRARIES})

