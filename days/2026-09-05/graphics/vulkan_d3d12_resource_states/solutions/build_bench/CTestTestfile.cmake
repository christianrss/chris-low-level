# CMake generated Testfile for 
# Source directory: E:/Aulas/low-level-unified-portfolio/days/2026-09-05/graphics/vulkan_d3d12_resource_states/solutions
# Build directory: E:/Aulas/low-level-unified-portfolio/days/2026-09-05/graphics/vulkan_d3d12_resource_states/solutions/build_bench
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
if(CTEST_CONFIGURATION_TYPE MATCHES "^([Dd][Ee][Bb][Uu][Gg])$")
  add_test(states "E:/Aulas/low-level-unified-portfolio/days/2026-09-05/graphics/vulkan_d3d12_resource_states/solutions/build_bench/Debug/test_states.exe")
  set_tests_properties(states PROPERTIES  _BACKTRACE_TRIPLES "E:/Aulas/low-level-unified-portfolio/days/2026-09-05/graphics/vulkan_d3d12_resource_states/solutions/CMakeLists.txt;6;add_test;E:/Aulas/low-level-unified-portfolio/days/2026-09-05/graphics/vulkan_d3d12_resource_states/solutions/CMakeLists.txt;0;")
elseif(CTEST_CONFIGURATION_TYPE MATCHES "^([Rr][Ee][Ll][Ee][Aa][Ss][Ee])$")
  add_test(states "E:/Aulas/low-level-unified-portfolio/days/2026-09-05/graphics/vulkan_d3d12_resource_states/solutions/build_bench/Release/test_states.exe")
  set_tests_properties(states PROPERTIES  _BACKTRACE_TRIPLES "E:/Aulas/low-level-unified-portfolio/days/2026-09-05/graphics/vulkan_d3d12_resource_states/solutions/CMakeLists.txt;6;add_test;E:/Aulas/low-level-unified-portfolio/days/2026-09-05/graphics/vulkan_d3d12_resource_states/solutions/CMakeLists.txt;0;")
elseif(CTEST_CONFIGURATION_TYPE MATCHES "^([Mm][Ii][Nn][Ss][Ii][Zz][Ee][Rr][Ee][Ll])$")
  add_test(states "E:/Aulas/low-level-unified-portfolio/days/2026-09-05/graphics/vulkan_d3d12_resource_states/solutions/build_bench/MinSizeRel/test_states.exe")
  set_tests_properties(states PROPERTIES  _BACKTRACE_TRIPLES "E:/Aulas/low-level-unified-portfolio/days/2026-09-05/graphics/vulkan_d3d12_resource_states/solutions/CMakeLists.txt;6;add_test;E:/Aulas/low-level-unified-portfolio/days/2026-09-05/graphics/vulkan_d3d12_resource_states/solutions/CMakeLists.txt;0;")
elseif(CTEST_CONFIGURATION_TYPE MATCHES "^([Rr][Ee][Ll][Ww][Ii][Tt][Hh][Dd][Ee][Bb][Ii][Nn][Ff][Oo])$")
  add_test(states "E:/Aulas/low-level-unified-portfolio/days/2026-09-05/graphics/vulkan_d3d12_resource_states/solutions/build_bench/RelWithDebInfo/test_states.exe")
  set_tests_properties(states PROPERTIES  _BACKTRACE_TRIPLES "E:/Aulas/low-level-unified-portfolio/days/2026-09-05/graphics/vulkan_d3d12_resource_states/solutions/CMakeLists.txt;6;add_test;E:/Aulas/low-level-unified-portfolio/days/2026-09-05/graphics/vulkan_d3d12_resource_states/solutions/CMakeLists.txt;0;")
else()
  add_test(states NOT_AVAILABLE)
endif()
