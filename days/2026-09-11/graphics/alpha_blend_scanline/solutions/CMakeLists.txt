cmake_minimum_required(VERSION 3.16)
project(blend CXX)
set(CMAKE_CXX_STANDARD 17)
enable_testing()

add_library(blend_core STATIC core/blend.cpp)
target_include_directories(blend_core PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/core)

add_executable(test_blend tests/test_blend.cpp)
target_link_libraries(test_blend PRIVATE blend_core)
add_test(NAME test_blend COMMAND test_blend)

if(WIN32)
  add_executable(blend_sw WIN32 software_win32/main.cpp)
  target_compile_definitions(blend_sw PRIVATE WIN32_LEAN_AND_MEAN NOMINMAX)
  target_link_libraries(blend_sw PRIVATE blend_core user32 gdi32)

  add_executable(blend_gl WIN32 opengl_win32/main.cpp)
  target_compile_definitions(blend_gl PRIVATE WIN32_LEAN_AND_MEAN NOMINMAX)
  target_link_libraries(blend_gl PRIVATE blend_core user32 gdi32 opengl32)
endif()
