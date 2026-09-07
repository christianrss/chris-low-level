cmake_minimum_required(VERSION 3.16)
project(raster_depth_parity CXX)
set(CMAKE_CXX_STANDARD 17)
enable_testing()

add_library(depth_core STATIC extension/depth_buffer.cpp extension/parity.cpp)
target_include_directories(depth_core PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/extension)

add_executable(test_depth tests/test_depth.cpp)
target_link_libraries(test_depth PRIVATE depth_core)
add_test(NAME test_depth COMMAND test_depth)

if(WIN32)
    add_executable(depth_gl WIN32 extension/opengl_depth.cpp)
    target_compile_definitions(depth_gl PRIVATE WIN32_LEAN_AND_MEAN NOMINMAX)
    target_link_libraries(depth_gl PRIVATE depth_core user32 gdi32 opengl32)

    add_executable(depth_sw WIN32 software_win32/main.cpp)
    target_compile_definitions(depth_sw PRIVATE WIN32_LEAN_AND_MEAN NOMINMAX)
    target_link_libraries(depth_sw PRIVATE depth_core user32 gdi32)
endif()
