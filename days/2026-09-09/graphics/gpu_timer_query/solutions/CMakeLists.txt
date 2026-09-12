cmake_minimum_required(VERSION 3.16)
project(gpu_timer_query CXX)
set(CMAKE_CXX_STANDARD 17)
enable_testing()

add_library(gpu_timer_query_core STATIC core/gpu_timer.cpp)
target_include_directories(gpu_timer_query_core PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/core)

add_executable(test_gpu_timer_query tests/test_gpu_timer_query.cpp)
target_link_libraries(test_gpu_timer_query PRIVATE gpu_timer_query_core)
add_test(NAME test_gpu_timer_query COMMAND test_gpu_timer_query)

if(WIN32)
  add_executable(gpu_timer_sw WIN32 software_win32/main.cpp)
  target_compile_definitions(gpu_timer_sw PRIVATE WIN32_LEAN_AND_MEAN NOMINMAX)
  target_link_libraries(gpu_timer_sw PRIVATE gpu_timer_query_core user32 gdi32)

  add_executable(gpu_timer_gl WIN32 opengl_win32/main.cpp)
  target_compile_definitions(gpu_timer_gl PRIVATE WIN32_LEAN_AND_MEAN NOMINMAX)
  target_link_libraries(gpu_timer_gl PRIVATE gpu_timer_query_core user32 gdi32 opengl32)
endif()
