cmake_minimum_required(VERSION 3.16)
project(explicit_barriers CXX)
set(CMAKE_CXX_STANDARD 17)
enable_testing()

add_library(explicit_barriers_core STATIC core/barriers.cpp)
target_include_directories(explicit_barriers_core PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/core)

add_executable(test_explicit_barriers tests/test_explicit_barriers.cpp)
target_link_libraries(test_explicit_barriers PRIVATE explicit_barriers_core)
add_test(NAME test_explicit_barriers COMMAND test_explicit_barriers)

if(WIN32)
  add_executable(barriers_sw WIN32 software_win32/main.cpp)
  target_compile_definitions(barriers_sw PRIVATE WIN32_LEAN_AND_MEAN NOMINMAX)
  target_link_libraries(barriers_sw PRIVATE explicit_barriers_core user32 gdi32)

  add_executable(barriers_gl WIN32 opengl_win32/main.cpp)
  target_compile_definitions(barriers_gl PRIVATE WIN32_LEAN_AND_MEAN NOMINMAX)
  target_link_libraries(barriers_gl PRIVATE explicit_barriers_core user32 gdi32 opengl32)
endif()
