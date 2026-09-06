cmake_minimum_required(VERSION 3.16)
project(png_idat_pipeline CXX)
set(CMAKE_CXX_STANDARD 17)
enable_testing()
add_executable(test_png
    bit_stream.cpp
    deflate_stored.cpp
    adler32.cpp
    crc32.cpp
    zlib_min.cpp
    png.cpp
    test_png.cpp)
add_test(NAME png_idat COMMAND test_png)
