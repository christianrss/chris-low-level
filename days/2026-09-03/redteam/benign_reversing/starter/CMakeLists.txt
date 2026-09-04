cmake_minimum_required(VERSION 3.20)
project(benign_reversing_lab C)

set(CMAKE_C_STANDARD 11)
set(CMAKE_C_STANDARD_REQUIRED ON)

add_executable(lab_target src/lab_target.c)

if(MSVC)
    target_compile_options(lab_target PRIVATE /W4)
else()
    target_compile_options(lab_target PRIVATE -Wall -Wextra -Wpedantic)
endif()
