# CMake generated Testfile for 
# Source directory: E:/Aulas/low-level-unified-portfolio/days/2026-09-06/systems/rle_byte_codec/solutions
# Build directory: E:/Aulas/low-level-unified-portfolio/days/2026-09-06/systems/rle_byte_codec/solutions/build_ci
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
if(CTEST_CONFIGURATION_TYPE MATCHES "^([Dd][Ee][Bb][Uu][Gg])$")
  add_test(test_rle "E:/Aulas/low-level-unified-portfolio/days/2026-09-06/systems/rle_byte_codec/solutions/build_ci/Debug/test_rle.exe")
  set_tests_properties(test_rle PROPERTIES  _BACKTRACE_TRIPLES "E:/Aulas/low-level-unified-portfolio/days/2026-09-06/systems/rle_byte_codec/solutions/CMakeLists.txt;6;add_test;E:/Aulas/low-level-unified-portfolio/days/2026-09-06/systems/rle_byte_codec/solutions/CMakeLists.txt;0;")
elseif(CTEST_CONFIGURATION_TYPE MATCHES "^([Rr][Ee][Ll][Ee][Aa][Ss][Ee])$")
  add_test(test_rle "E:/Aulas/low-level-unified-portfolio/days/2026-09-06/systems/rle_byte_codec/solutions/build_ci/Release/test_rle.exe")
  set_tests_properties(test_rle PROPERTIES  _BACKTRACE_TRIPLES "E:/Aulas/low-level-unified-portfolio/days/2026-09-06/systems/rle_byte_codec/solutions/CMakeLists.txt;6;add_test;E:/Aulas/low-level-unified-portfolio/days/2026-09-06/systems/rle_byte_codec/solutions/CMakeLists.txt;0;")
elseif(CTEST_CONFIGURATION_TYPE MATCHES "^([Mm][Ii][Nn][Ss][Ii][Zz][Ee][Rr][Ee][Ll])$")
  add_test(test_rle "E:/Aulas/low-level-unified-portfolio/days/2026-09-06/systems/rle_byte_codec/solutions/build_ci/MinSizeRel/test_rle.exe")
  set_tests_properties(test_rle PROPERTIES  _BACKTRACE_TRIPLES "E:/Aulas/low-level-unified-portfolio/days/2026-09-06/systems/rle_byte_codec/solutions/CMakeLists.txt;6;add_test;E:/Aulas/low-level-unified-portfolio/days/2026-09-06/systems/rle_byte_codec/solutions/CMakeLists.txt;0;")
elseif(CTEST_CONFIGURATION_TYPE MATCHES "^([Rr][Ee][Ll][Ww][Ii][Tt][Hh][Dd][Ee][Bb][Ii][Nn][Ff][Oo])$")
  add_test(test_rle "E:/Aulas/low-level-unified-portfolio/days/2026-09-06/systems/rle_byte_codec/solutions/build_ci/RelWithDebInfo/test_rle.exe")
  set_tests_properties(test_rle PROPERTIES  _BACKTRACE_TRIPLES "E:/Aulas/low-level-unified-portfolio/days/2026-09-06/systems/rle_byte_codec/solutions/CMakeLists.txt;6;add_test;E:/Aulas/low-level-unified-portfolio/days/2026-09-06/systems/rle_byte_codec/solutions/CMakeLists.txt;0;")
else()
  add_test(test_rle NOT_AVAILABLE)
endif()
