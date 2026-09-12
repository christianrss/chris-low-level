cmake_minimum_required(VERSION 3.20)
project(clvm_xdbg LANGUAGES C CXX)
set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)

add_library(clvm_loader host/clvm_loader.c)
target_include_directories(clvm_loader PUBLIC include)

add_library(clvm_xdbg_core src/session.cpp)
target_include_directories(clvm_xdbg_core PUBLIC include)
target_link_libraries(clvm_xdbg_core PUBLIC clvm_loader)

add_executable(clvm-xdbg host/main.cpp)
target_link_libraries(clvm-xdbg PRIVATE clvm_xdbg_core)

if(MSVC)
  target_compile_options(clvm_loader PRIVATE /W4)
  target_compile_options(clvm_xdbg_core PRIVATE /W4)
  target_compile_options(clvm-xdbg PRIVATE /W4)
else()
  target_compile_options(clvm_loader PRIVATE -Wall -Wextra -Wpedantic)
  target_compile_options(clvm_xdbg_core PRIVATE -Wall -Wextra -Wpedantic)
  target_compile_options(clvm-xdbg PRIVATE -Wall -Wextra -Wpedantic)
endif()

enable_testing()
find_package(Python3 COMPONENTS Interpreter REQUIRED)
add_test(
    NAME xdbg_session
    COMMAND ${Python3_EXECUTABLE}
            ${CMAKE_CURRENT_SOURCE_DIR}/tests/test_xdbg.py
            $<TARGET_FILE:clvm-xdbg>
            ${CMAKE_CURRENT_SOURCE_DIR})
