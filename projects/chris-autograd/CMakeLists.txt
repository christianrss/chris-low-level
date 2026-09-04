cmake_minimum_required(VERSION 3.20)
project(ai_linear_lowlevel C)

set(CMAKE_C_STANDARD 11)
set(CMAKE_C_STANDARD_REQUIRED ON)

add_executable(linear_train src/linear_train.c)
if(MSVC)
    target_compile_options(linear_train PRIVATE /W4 /permissive-)
else()
    target_compile_options(linear_train PRIVATE -Wall -Wextra -Wpedantic)
endif()


enable_testing()
add_test(NAME c_linear_train COMMAND linear_train)
find_package(Python3 COMPONENTS Interpreter REQUIRED)
add_test(NAME python_autograd_tests COMMAND ${Python3_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/tests/test_autograd.py)
