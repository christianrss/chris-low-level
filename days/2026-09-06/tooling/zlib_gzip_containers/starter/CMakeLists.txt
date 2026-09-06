cmake_minimum_required(VERSION 3.16)
project(zlib_gzip_containers CXX)
set(CMAKE_CXX_STANDARD 17)
enable_testing()
add_executable(test_zlib
    bit_stream.cpp
    deflate_stored.cpp
    adler32.cpp
    crc32.cpp
    zlib_wrap.cpp
    gzip_wrap.cpp
    test_zlib.cpp)
add_test(NAME zlib_gzip COMMAND test_zlib)
