# CMake generated Testfile for 
# Source directory: E:/Aulas/low-level-unified-portfolio/days/2026-09-04/os/graphics_reference/solutions
# Build directory: E:/Aulas/low-level-unified-portfolio/days/2026-09-04/os/graphics_reference/solutions/build_ci
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
if(CTEST_CONFIGURATION_TYPE MATCHES "^([Dd][Ee][Bb][Uu][Gg])$")
  add_test([=[os_graphics_tests]=] "E:/Aulas/low-level-unified-portfolio/days/2026-09-04/os/graphics_reference/solutions/build_ci/Debug/os_graphics_tests.exe")
  set_tests_properties([=[os_graphics_tests]=] PROPERTIES  _BACKTRACE_TRIPLES "E:/Aulas/low-level-unified-portfolio/days/2026-09-04/os/graphics_reference/solutions/CMakeLists.txt;25;add_test;E:/Aulas/low-level-unified-portfolio/days/2026-09-04/os/graphics_reference/solutions/CMakeLists.txt;0;")
elseif(CTEST_CONFIGURATION_TYPE MATCHES "^([Rr][Ee][Ll][Ee][Aa][Ss][Ee])$")
  add_test([=[os_graphics_tests]=] "E:/Aulas/low-level-unified-portfolio/days/2026-09-04/os/graphics_reference/solutions/build_ci/Release/os_graphics_tests.exe")
  set_tests_properties([=[os_graphics_tests]=] PROPERTIES  _BACKTRACE_TRIPLES "E:/Aulas/low-level-unified-portfolio/days/2026-09-04/os/graphics_reference/solutions/CMakeLists.txt;25;add_test;E:/Aulas/low-level-unified-portfolio/days/2026-09-04/os/graphics_reference/solutions/CMakeLists.txt;0;")
elseif(CTEST_CONFIGURATION_TYPE MATCHES "^([Mm][Ii][Nn][Ss][Ii][Zz][Ee][Rr][Ee][Ll])$")
  add_test([=[os_graphics_tests]=] "E:/Aulas/low-level-unified-portfolio/days/2026-09-04/os/graphics_reference/solutions/build_ci/MinSizeRel/os_graphics_tests.exe")
  set_tests_properties([=[os_graphics_tests]=] PROPERTIES  _BACKTRACE_TRIPLES "E:/Aulas/low-level-unified-portfolio/days/2026-09-04/os/graphics_reference/solutions/CMakeLists.txt;25;add_test;E:/Aulas/low-level-unified-portfolio/days/2026-09-04/os/graphics_reference/solutions/CMakeLists.txt;0;")
elseif(CTEST_CONFIGURATION_TYPE MATCHES "^([Rr][Ee][Ll][Ww][Ii][Tt][Hh][Dd][Ee][Bb][Ii][Nn][Ff][Oo])$")
  add_test([=[os_graphics_tests]=] "E:/Aulas/low-level-unified-portfolio/days/2026-09-04/os/graphics_reference/solutions/build_ci/RelWithDebInfo/os_graphics_tests.exe")
  set_tests_properties([=[os_graphics_tests]=] PROPERTIES  _BACKTRACE_TRIPLES "E:/Aulas/low-level-unified-portfolio/days/2026-09-04/os/graphics_reference/solutions/CMakeLists.txt;25;add_test;E:/Aulas/low-level-unified-portfolio/days/2026-09-04/os/graphics_reference/solutions/CMakeLists.txt;0;")
else()
  add_test([=[os_graphics_tests]=] NOT_AVAILABLE)
endif()
