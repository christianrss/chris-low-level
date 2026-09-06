# CMake generated Testfile for 
# Source directory: E:/Aulas/low-level-unified-portfolio/days/2026-09-04/debugger/protocol_v1/solutions
# Build directory: E:/Aulas/low-level-unified-portfolio/days/2026-09-04/debugger/protocol_v1/solutions/build_ci
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
if(CTEST_CONFIGURATION_TYPE MATCHES "^([Dd][Ee][Bb][Uu][Gg])$")
  add_test([=[debugger_tests]=] "E:/Aulas/low-level-unified-portfolio/days/2026-09-04/debugger/protocol_v1/solutions/build_ci/Debug/debugger_tests.exe")
  set_tests_properties([=[debugger_tests]=] PROPERTIES  _BACKTRACE_TRIPLES "E:/Aulas/low-level-unified-portfolio/days/2026-09-04/debugger/protocol_v1/solutions/CMakeLists.txt;25;add_test;E:/Aulas/low-level-unified-portfolio/days/2026-09-04/debugger/protocol_v1/solutions/CMakeLists.txt;0;")
elseif(CTEST_CONFIGURATION_TYPE MATCHES "^([Rr][Ee][Ll][Ee][Aa][Ss][Ee])$")
  add_test([=[debugger_tests]=] "E:/Aulas/low-level-unified-portfolio/days/2026-09-04/debugger/protocol_v1/solutions/build_ci/Release/debugger_tests.exe")
  set_tests_properties([=[debugger_tests]=] PROPERTIES  _BACKTRACE_TRIPLES "E:/Aulas/low-level-unified-portfolio/days/2026-09-04/debugger/protocol_v1/solutions/CMakeLists.txt;25;add_test;E:/Aulas/low-level-unified-portfolio/days/2026-09-04/debugger/protocol_v1/solutions/CMakeLists.txt;0;")
elseif(CTEST_CONFIGURATION_TYPE MATCHES "^([Mm][Ii][Nn][Ss][Ii][Zz][Ee][Rr][Ee][Ll])$")
  add_test([=[debugger_tests]=] "E:/Aulas/low-level-unified-portfolio/days/2026-09-04/debugger/protocol_v1/solutions/build_ci/MinSizeRel/debugger_tests.exe")
  set_tests_properties([=[debugger_tests]=] PROPERTIES  _BACKTRACE_TRIPLES "E:/Aulas/low-level-unified-portfolio/days/2026-09-04/debugger/protocol_v1/solutions/CMakeLists.txt;25;add_test;E:/Aulas/low-level-unified-portfolio/days/2026-09-04/debugger/protocol_v1/solutions/CMakeLists.txt;0;")
elseif(CTEST_CONFIGURATION_TYPE MATCHES "^([Rr][Ee][Ll][Ww][Ii][Tt][Hh][Dd][Ee][Bb][Ii][Nn][Ff][Oo])$")
  add_test([=[debugger_tests]=] "E:/Aulas/low-level-unified-portfolio/days/2026-09-04/debugger/protocol_v1/solutions/build_ci/RelWithDebInfo/debugger_tests.exe")
  set_tests_properties([=[debugger_tests]=] PROPERTIES  _BACKTRACE_TRIPLES "E:/Aulas/low-level-unified-portfolio/days/2026-09-04/debugger/protocol_v1/solutions/CMakeLists.txt;25;add_test;E:/Aulas/low-level-unified-portfolio/days/2026-09-04/debugger/protocol_v1/solutions/CMakeLists.txt;0;")
else()
  add_test([=[debugger_tests]=] NOT_AVAILABLE)
endif()
