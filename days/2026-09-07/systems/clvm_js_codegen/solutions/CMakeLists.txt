cmake_minimum_required(VERSION 3.20)
project(clvm_js_codegen LANGUAGES NONE)
enable_testing()
find_package(Python3 COMPONENTS Interpreter REQUIRED)
add_test(NAME js_codegen_integration
  COMMAND ${Python3_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/tests/integration_test.py)
