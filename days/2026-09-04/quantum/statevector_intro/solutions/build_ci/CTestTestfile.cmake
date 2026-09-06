# CMake generated Testfile for 
# Source directory: E:/Aulas/low-level-unified-portfolio/days/2026-09-04/quantum/statevector_intro/solutions
# Build directory: E:/Aulas/low-level-unified-portfolio/days/2026-09-04/quantum/statevector_intro/solutions/build_ci
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
if(CTEST_CONFIGURATION_TYPE MATCHES "^([Dd][Ee][Bb][Uu][Gg])$")
  add_test([=[qsim_tests]=] "E:/Aulas/low-level-unified-portfolio/days/2026-09-04/quantum/statevector_intro/solutions/build_ci/Debug/qsim_tests.exe")
  set_tests_properties([=[qsim_tests]=] PROPERTIES  _BACKTRACE_TRIPLES "E:/Aulas/low-level-unified-portfolio/days/2026-09-04/quantum/statevector_intro/solutions/CMakeLists.txt;25;add_test;E:/Aulas/low-level-unified-portfolio/days/2026-09-04/quantum/statevector_intro/solutions/CMakeLists.txt;0;")
elseif(CTEST_CONFIGURATION_TYPE MATCHES "^([Rr][Ee][Ll][Ee][Aa][Ss][Ee])$")
  add_test([=[qsim_tests]=] "E:/Aulas/low-level-unified-portfolio/days/2026-09-04/quantum/statevector_intro/solutions/build_ci/Release/qsim_tests.exe")
  set_tests_properties([=[qsim_tests]=] PROPERTIES  _BACKTRACE_TRIPLES "E:/Aulas/low-level-unified-portfolio/days/2026-09-04/quantum/statevector_intro/solutions/CMakeLists.txt;25;add_test;E:/Aulas/low-level-unified-portfolio/days/2026-09-04/quantum/statevector_intro/solutions/CMakeLists.txt;0;")
elseif(CTEST_CONFIGURATION_TYPE MATCHES "^([Mm][Ii][Nn][Ss][Ii][Zz][Ee][Rr][Ee][Ll])$")
  add_test([=[qsim_tests]=] "E:/Aulas/low-level-unified-portfolio/days/2026-09-04/quantum/statevector_intro/solutions/build_ci/MinSizeRel/qsim_tests.exe")
  set_tests_properties([=[qsim_tests]=] PROPERTIES  _BACKTRACE_TRIPLES "E:/Aulas/low-level-unified-portfolio/days/2026-09-04/quantum/statevector_intro/solutions/CMakeLists.txt;25;add_test;E:/Aulas/low-level-unified-portfolio/days/2026-09-04/quantum/statevector_intro/solutions/CMakeLists.txt;0;")
elseif(CTEST_CONFIGURATION_TYPE MATCHES "^([Rr][Ee][Ll][Ww][Ii][Tt][Hh][Dd][Ee][Bb][Ii][Nn][Ff][Oo])$")
  add_test([=[qsim_tests]=] "E:/Aulas/low-level-unified-portfolio/days/2026-09-04/quantum/statevector_intro/solutions/build_ci/RelWithDebInfo/qsim_tests.exe")
  set_tests_properties([=[qsim_tests]=] PROPERTIES  _BACKTRACE_TRIPLES "E:/Aulas/low-level-unified-portfolio/days/2026-09-04/quantum/statevector_intro/solutions/CMakeLists.txt;25;add_test;E:/Aulas/low-level-unified-portfolio/days/2026-09-04/quantum/statevector_intro/solutions/CMakeLists.txt;0;")
else()
  add_test([=[qsim_tests]=] NOT_AVAILABLE)
endif()
