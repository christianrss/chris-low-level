# CMake generated Testfile for 
# Source directory: E:/Aulas/low-level-unified-portfolio/days/2026-09-05/ai/tiled_matmul_cache/solutions
# Build directory: E:/Aulas/low-level-unified-portfolio/days/2026-09-05/ai/tiled_matmul_cache/solutions/build_ci
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
if(CTEST_CONFIGURATION_TYPE MATCHES "^([Dd][Ee][Bb][Uu][Gg])$")
  add_test(matmul "E:/Aulas/low-level-unified-portfolio/days/2026-09-05/ai/tiled_matmul_cache/solutions/build_ci/Debug/test_matmul.exe")
  set_tests_properties(matmul PROPERTIES  _BACKTRACE_TRIPLES "E:/Aulas/low-level-unified-portfolio/days/2026-09-05/ai/tiled_matmul_cache/solutions/CMakeLists.txt;6;add_test;E:/Aulas/low-level-unified-portfolio/days/2026-09-05/ai/tiled_matmul_cache/solutions/CMakeLists.txt;0;")
elseif(CTEST_CONFIGURATION_TYPE MATCHES "^([Rr][Ee][Ll][Ee][Aa][Ss][Ee])$")
  add_test(matmul "E:/Aulas/low-level-unified-portfolio/days/2026-09-05/ai/tiled_matmul_cache/solutions/build_ci/Release/test_matmul.exe")
  set_tests_properties(matmul PROPERTIES  _BACKTRACE_TRIPLES "E:/Aulas/low-level-unified-portfolio/days/2026-09-05/ai/tiled_matmul_cache/solutions/CMakeLists.txt;6;add_test;E:/Aulas/low-level-unified-portfolio/days/2026-09-05/ai/tiled_matmul_cache/solutions/CMakeLists.txt;0;")
elseif(CTEST_CONFIGURATION_TYPE MATCHES "^([Mm][Ii][Nn][Ss][Ii][Zz][Ee][Rr][Ee][Ll])$")
  add_test(matmul "E:/Aulas/low-level-unified-portfolio/days/2026-09-05/ai/tiled_matmul_cache/solutions/build_ci/MinSizeRel/test_matmul.exe")
  set_tests_properties(matmul PROPERTIES  _BACKTRACE_TRIPLES "E:/Aulas/low-level-unified-portfolio/days/2026-09-05/ai/tiled_matmul_cache/solutions/CMakeLists.txt;6;add_test;E:/Aulas/low-level-unified-portfolio/days/2026-09-05/ai/tiled_matmul_cache/solutions/CMakeLists.txt;0;")
elseif(CTEST_CONFIGURATION_TYPE MATCHES "^([Rr][Ee][Ll][Ww][Ii][Tt][Hh][Dd][Ee][Bb][Ii][Nn][Ff][Oo])$")
  add_test(matmul "E:/Aulas/low-level-unified-portfolio/days/2026-09-05/ai/tiled_matmul_cache/solutions/build_ci/RelWithDebInfo/test_matmul.exe")
  set_tests_properties(matmul PROPERTIES  _BACKTRACE_TRIPLES "E:/Aulas/low-level-unified-portfolio/days/2026-09-05/ai/tiled_matmul_cache/solutions/CMakeLists.txt;6;add_test;E:/Aulas/low-level-unified-portfolio/days/2026-09-05/ai/tiled_matmul_cache/solutions/CMakeLists.txt;0;")
else()
  add_test(matmul NOT_AVAILABLE)
endif()
