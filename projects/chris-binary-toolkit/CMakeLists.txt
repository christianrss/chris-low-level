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


enable_testing()
find_package(Python3 COMPONENTS Interpreter REQUIRED)
add_test(NAME ascii_string_tests COMMAND ${Python3_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/tests/test_ascii_strings.py)

add_test(NAME elf64_tests COMMAND ${Python3_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/tests/test_elf64.py)
