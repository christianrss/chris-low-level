cmake_minimum_required(VERSION 3.16)
project(artillery_trajectory_2d CXX)
set(CMAKE_CXX_STANDARD 17)
enable_testing()

add_library(artillery_core STATIC core/artillery.cpp)
target_include_directories(artillery_core PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/core)

add_executable(test_artillery tests/test_artillery.cpp)
target_link_libraries(test_artillery PRIVATE artillery_core)
add_test(NAME test_artillery COMMAND test_artillery)

if(WIN32)
    add_executable(artillery_sw WIN32 software_win32/main.cpp)
    target_compile_definitions(artillery_sw PRIVATE WIN32_LEAN_AND_MEAN NOMINMAX)
    target_link_libraries(artillery_sw PRIVATE artillery_core user32 gdi32)

    add_executable(artillery_gl WIN32 opengl_win32/main.cpp)
    target_compile_definitions(artillery_gl PRIVATE WIN32_LEAN_AND_MEAN NOMINMAX)
    target_link_libraries(artillery_gl PRIVATE artillery_core user32 gdi32 opengl32)

    add_executable(artillery_d3d WIN32 d3d11_win32/main.cpp)
    target_compile_definitions(artillery_d3d PRIVATE WIN32_LEAN_AND_MEAN NOMINMAX)
    target_link_libraries(artillery_d3d PRIVATE artillery_core user32 gdi32 d3d11 dxgi d3dcompiler)
endif()
