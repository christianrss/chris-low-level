cmake_minimum_required(VERSION 3.16)
project(matmul_test LANGUAGES CXX)
set(CMAKE_CXX_STANDARD 17)
add_executable(matmul_test matmul.cpp test_matmul.cpp)
enable_testing()
add_test(NAME matmul_test_test COMMAND matmul_test)

add_executable(matmul_bench matmul.cpp bench_matmul.cpp)
