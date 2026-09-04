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
