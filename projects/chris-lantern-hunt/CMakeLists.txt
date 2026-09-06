cmake_minimum_required(VERSION 3.20)
project(ChrisLanternHunt LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

set(LANTERN_ASSET_DIR "${CMAKE_SOURCE_DIR}/assets")
string(REPLACE "\\" "/" LANTERN_ASSET_DIR "${LANTERN_ASSET_DIR}")
set(LANTERN_SHADER_SOLUTIONS "${CMAKE_SOURCE_DIR}/solutions/src/shaders")
string(REPLACE "\\" "/" LANTERN_SHADER_SOLUTIONS "${LANTERN_SHADER_SOLUTIONS}")
set(LANTERN_SHADER_STARTER "${CMAKE_SOURCE_DIR}/starter/src/shaders")
string(REPLACE "\\" "/" LANTERN_SHADER_STARTER "${LANTERN_SHADER_STARTER}")

function(add_lantern_core target_name source_dir)
    add_library(${target_name} STATIC
        ${source_dir}/src/procgen.cpp
        ${source_dir}/src/collision.cpp
        ${source_dir}/src/game.cpp
        ${source_dir}/src/objectives.cpp
        ${source_dir}/src/checkpoint.cpp
    )
    target_include_directories(${target_name} PUBLIC ${source_dir}/src)
endfunction()

add_lantern_core(lantern_core_solutions solutions)
add_lantern_core(lantern_core_starter starter)

if(WIN32)
    add_executable(lantern_hunt WIN32
        solutions/src/main_win32.cpp
        solutions/src/texture.cpp
        solutions/src/audio.cpp
        solutions/src/font.cpp
        solutions/src/hud.cpp
    )
    target_compile_definitions(lantern_hunt PRIVATE
        WIN32_LEAN_AND_MEAN
        NOMINMAX
        LANTERN_ASSET_ROOT="${LANTERN_ASSET_DIR}"
        LANTERN_SHADER_DIR="${LANTERN_SHADER_SOLUTIONS}"
    )
    target_link_libraries(lantern_hunt PRIVATE lantern_core_solutions user32 gdi32 opengl32 winmm)
    target_include_directories(lantern_hunt PRIVATE solutions/src)

    add_executable(lantern_hunt_starter WIN32
        starter/src/main_win32.cpp
        starter/src/texture.cpp
        starter/src/audio.cpp
        starter/src/font.cpp
        starter/src/hud.cpp
    )
    target_compile_definitions(lantern_hunt_starter PRIVATE
        WIN32_LEAN_AND_MEAN
        NOMINMAX
        LANTERN_ASSET_ROOT="${LANTERN_ASSET_DIR}"
        LANTERN_SHADER_DIR="${LANTERN_SHADER_STARTER}"
    )
    target_link_libraries(lantern_hunt_starter PRIVATE lantern_core_starter user32 gdi32 opengl32 winmm)
    target_include_directories(lantern_hunt_starter PRIVATE starter/src)
else()
    message(STATUS "Lantern Hunt GPU build is Windows/WGL only. Building portable tests.")
endif()

add_executable(test_procgen solutions/tests/test_procgen.cpp)
target_link_libraries(test_procgen PRIVATE lantern_core_solutions)

add_executable(test_collision solutions/tests/test_collision.cpp)
target_link_libraries(test_collision PRIVATE lantern_core_solutions)

add_executable(test_objectives solutions/tests/test_objectives.cpp)
target_link_libraries(test_objectives PRIVATE lantern_core_solutions)

add_executable(test_checkpoint solutions/tests/test_checkpoint.cpp)
target_link_libraries(test_checkpoint PRIVATE lantern_core_solutions)

enable_testing()
add_test(NAME lantern_procgen_seed42 COMMAND test_procgen)
add_test(NAME lantern_collision_slide COMMAND test_collision)
add_test(NAME lantern_objectives_flow COMMAND test_objectives)
add_test(NAME lantern_checkpoint_save COMMAND test_checkpoint)
