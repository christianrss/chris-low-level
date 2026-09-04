cmake_minimum_required(VERSION 3.20)
project(DualBackendLowLevel3D LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

add_library(scene_core common/engine.cpp)
target_include_directories(scene_core PUBLIC common)

if(WIN32)
    add_executable(software_renderer WIN32 software_win32/main.cpp)
    target_compile_definitions(software_renderer PRIVATE WIN32_LEAN_AND_MEAN NOMINMAX)
    target_link_libraries(software_renderer PRIVATE scene_core user32 gdi32)

    add_executable(opengl_renderer WIN32 opengl_win32/main.cpp)
    target_compile_definitions(opengl_renderer PRIVATE WIN32_LEAN_AND_MEAN NOMINMAX)
    target_link_libraries(opengl_renderer PRIVATE scene_core user32 gdi32 opengl32)
else()
    message(STATUS
        "Windows render backends are Win32/WGL. "
        "Only portable tests are built on this host.")
endif()

add_executable(core_tests tests/core_tests.cpp)
target_link_libraries(core_tests PRIVATE scene_core)


enable_testing()
add_test(NAME scene_core_tests COMMAND core_tests)
add_executable(core_benchmark benchmarks/core_benchmark.cpp)
target_link_libraries(core_benchmark PRIVATE scene_core)
