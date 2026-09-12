cmake_minimum_required(VERSION 3.16)
project(pipeline_state_object CXX)
set(CMAKE_CXX_STANDARD 17)
enable_testing()

add_library(pso_core STATIC core/pso.cpp)
target_include_directories(pso_core PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/core)

add_executable(test_pso tests/test_pso.cpp)
target_link_libraries(test_pso PRIVATE pso_core)
add_test(NAME test_pso COMMAND test_pso)

if(WIN32)
    add_executable(pso_sw WIN32 software_win32/main.cpp)
    target_compile_definitions(pso_sw PRIVATE WIN32_LEAN_AND_MEAN NOMINMAX)
    target_link_libraries(pso_sw PRIVATE pso_core user32 gdi32)

    add_executable(pso_gl WIN32 opengl_win32/main.cpp)
    target_compile_definitions(pso_gl PRIVATE WIN32_LEAN_AND_MEAN NOMINMAX)
    target_link_libraries(pso_gl PRIVATE pso_core user32 gdi32 opengl32)
endif()
