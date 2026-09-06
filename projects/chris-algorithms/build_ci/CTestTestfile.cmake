# CMake generated Testfile for 
# Source directory: E:/Aulas/low-level-unified-portfolio/projects/chris-algorithms
# Build directory: E:/Aulas/low-level-unified-portfolio/projects/chris-algorithms/build_ci
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
if(CTEST_CONFIGURATION_TYPE MATCHES "^([Dd][Ee][Bb][Uu][Gg])$")
  add_test([=[algorithm_tests]=] "E:/Aulas/low-level-unified-portfolio/projects/chris-algorithms/build_ci/Debug/algorithm_tests.exe")
  set_tests_properties([=[algorithm_tests]=] PROPERTIES  _BACKTRACE_TRIPLES "E:/Aulas/low-level-unified-portfolio/projects/chris-algorithms/CMakeLists.txt;25;add_test;E:/Aulas/low-level-unified-portfolio/projects/chris-algorithms/CMakeLists.txt;0;")
elseif(CTEST_CONFIGURATION_TYPE MATCHES "^([Rr][Ee][Ll][Ee][Aa][Ss][Ee])$")
  add_test([=[algorithm_tests]=] "E:/Aulas/low-level-unified-portfolio/projects/chris-algorithms/build_ci/Release/algorithm_tests.exe")
  set_tests_properties([=[algorithm_tests]=] PROPERTIES  _BACKTRACE_TRIPLES "E:/Aulas/low-level-unified-portfolio/projects/chris-algorithms/CMakeLists.txt;25;add_test;E:/Aulas/low-level-unified-portfolio/projects/chris-algorithms/CMakeLists.txt;0;")
elseif(CTEST_CONFIGURATION_TYPE MATCHES "^([Mm][Ii][Nn][Ss][Ii][Zz][Ee][Rr][Ee][Ll])$")
  add_test([=[algorithm_tests]=] "E:/Aulas/low-level-unified-portfolio/projects/chris-algorithms/build_ci/MinSizeRel/algorithm_tests.exe")
  set_tests_properties([=[algorithm_tests]=] PROPERTIES  _BACKTRACE_TRIPLES "E:/Aulas/low-level-unified-portfolio/projects/chris-algorithms/CMakeLists.txt;25;add_test;E:/Aulas/low-level-unified-portfolio/projects/chris-algorithms/CMakeLists.txt;0;")
elseif(CTEST_CONFIGURATION_TYPE MATCHES "^([Rr][Ee][Ll][Ww][Ii][Tt][Hh][Dd][Ee][Bb][Ii][Nn][Ff][Oo])$")
  add_test([=[algorithm_tests]=] "E:/Aulas/low-level-unified-portfolio/projects/chris-algorithms/build_ci/RelWithDebInfo/algorithm_tests.exe")
  set_tests_properties([=[algorithm_tests]=] PROPERTIES  _BACKTRACE_TRIPLES "E:/Aulas/low-level-unified-portfolio/projects/chris-algorithms/CMakeLists.txt;25;add_test;E:/Aulas/low-level-unified-portfolio/projects/chris-algorithms/CMakeLists.txt;0;")
else()
  add_test([=[algorithm_tests]=] NOT_AVAILABLE)
endif()
