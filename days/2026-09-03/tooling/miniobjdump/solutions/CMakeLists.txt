cmake_minimum_required(VERSION 3.20)
project(miniobjdump C CXX)

set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_executable(test_target tests/test_target.c)
add_executable(miniobjdump src/main.cpp)

if(MSVC)
    target_compile_options(miniobjdump PRIVATE /W4 /permissive-)
    target_compile_options(test_target PRIVATE /W4)
else()
    target_compile_options(miniobjdump PRIVATE -Wall -Wextra -Wpedantic)
    target_compile_options(test_target PRIVATE -Wall -Wextra -Wpedantic)
endif()


enable_testing()
find_package(Python3 COMPONENTS Interpreter REQUIRED)
add_test(
    NAME inspect_own_target
    COMMAND ${Python3_EXECUTABLE}
        ${CMAKE_CURRENT_SOURCE_DIR}/tests/integration_test.py
        $<TARGET_FILE:miniobjdump>
        $<TARGET_FILE:test_target>
)
