cmake_minimum_required(VERSION 3.16)
project(shader_stage_fsm CXX)
set(CMAKE_CXX_STANDARD 17)
enable_testing()

add_library(shader_stage_fsm_core STATIC core/shader_fsm.cpp)
target_include_directories(shader_stage_fsm_core PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/core)

add_executable(test_shader_stage_fsm tests/test_shader_stage_fsm.cpp)
target_link_libraries(test_shader_stage_fsm PRIVATE shader_stage_fsm_core)
add_test(NAME test_shader_stage_fsm COMMAND test_shader_stage_fsm)

if(WIN32)
  add_executable(shader_fsm_sw WIN32 software_win32/main.cpp)
  target_compile_definitions(shader_fsm_sw PRIVATE WIN32_LEAN_AND_MEAN NOMINMAX)
  target_link_libraries(shader_fsm_sw PRIVATE shader_stage_fsm_core user32 gdi32)

  add_executable(shader_fsm_gl WIN32 opengl_win32/main.cpp)
  target_compile_definitions(shader_fsm_gl PRIVATE WIN32_LEAN_AND_MEAN NOMINMAX)
  target_link_libraries(shader_fsm_gl PRIVATE shader_stage_fsm_core user32 gdi32 opengl32)
endif()
