cmake_minimum_required(VERSION 3.16)
project(chris_compress CXX)
set(CMAKE_CXX_STANDARD 20)
enable_testing()

add_executable(chris_compress
    src/main.cpp
    src/rle.cpp
    src/zlib_stored.cpp
)
target_include_directories(chris_compress PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/src)

add_executable(test_compress tests/test_compress.cpp src/rle.cpp src/zlib_stored.cpp)
target_include_directories(test_compress PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/src)
add_test(NAME compress_roundtrip COMMAND test_compress)
