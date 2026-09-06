cmake_minimum_required(VERSION 3.16)
project(portal_verlet_starter CXX)
set(CMAKE_CXX_STANDARD 17)
enable_testing()

add_library(portal_core STATIC
    src/math.cpp
    src/portal.cpp
    src/verlet.cpp
    src/sphere_portal.cpp
)
target_include_directories(portal_core PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/src)

function(add_portal_test name)
    add_executable(${name} tests/${name}.cpp)
    target_link_libraries(${name} PRIVATE portal_core)
    add_test(NAME ${name} COMMAND ${name})
endfunction()

add_portal_test(test_portal_transform)
add_portal_test(test_verlet_rope)
add_portal_test(test_sphere_portal)

if(WIN32)
    option(PORTAL_OPENGL "Build portal_demo OpenGL executable" ON)
    if(PORTAL_OPENGL)
        add_executable(portal_demo WIN32 src/main_opengl.cpp src/render_gl.cpp)
        target_link_libraries(portal_demo PRIVATE portal_core user32)
        target_compile_definitions(portal_demo PRIVATE NOMINMAX)
    endif()
endif()
