# CMake generated Testfile for 
# Source directory: E:/Aulas/low-level-unified-portfolio/days/2026-09-06/tooling/png_idat_pipeline/solutions
# Build directory: E:/Aulas/low-level-unified-portfolio/days/2026-09-06/tooling/png_idat_pipeline/solutions/build_ci
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
if(CTEST_CONFIGURATION_TYPE MATCHES "^([Dd][Ee][Bb][Uu][Gg])$")
  add_test(png_idat "E:/Aulas/low-level-unified-portfolio/days/2026-09-06/tooling/png_idat_pipeline/solutions/build_ci/Debug/test_png.exe")
  set_tests_properties(png_idat PROPERTIES  _BACKTRACE_TRIPLES "E:/Aulas/low-level-unified-portfolio/days/2026-09-06/tooling/png_idat_pipeline/solutions/CMakeLists.txt;13;add_test;E:/Aulas/low-level-unified-portfolio/days/2026-09-06/tooling/png_idat_pipeline/solutions/CMakeLists.txt;0;")
elseif(CTEST_CONFIGURATION_TYPE MATCHES "^([Rr][Ee][Ll][Ee][Aa][Ss][Ee])$")
  add_test(png_idat "E:/Aulas/low-level-unified-portfolio/days/2026-09-06/tooling/png_idat_pipeline/solutions/build_ci/Release/test_png.exe")
  set_tests_properties(png_idat PROPERTIES  _BACKTRACE_TRIPLES "E:/Aulas/low-level-unified-portfolio/days/2026-09-06/tooling/png_idat_pipeline/solutions/CMakeLists.txt;13;add_test;E:/Aulas/low-level-unified-portfolio/days/2026-09-06/tooling/png_idat_pipeline/solutions/CMakeLists.txt;0;")
elseif(CTEST_CONFIGURATION_TYPE MATCHES "^([Mm][Ii][Nn][Ss][Ii][Zz][Ee][Rr][Ee][Ll])$")
  add_test(png_idat "E:/Aulas/low-level-unified-portfolio/days/2026-09-06/tooling/png_idat_pipeline/solutions/build_ci/MinSizeRel/test_png.exe")
  set_tests_properties(png_idat PROPERTIES  _BACKTRACE_TRIPLES "E:/Aulas/low-level-unified-portfolio/days/2026-09-06/tooling/png_idat_pipeline/solutions/CMakeLists.txt;13;add_test;E:/Aulas/low-level-unified-portfolio/days/2026-09-06/tooling/png_idat_pipeline/solutions/CMakeLists.txt;0;")
elseif(CTEST_CONFIGURATION_TYPE MATCHES "^([Rr][Ee][Ll][Ww][Ii][Tt][Hh][Dd][Ee][Bb][Ii][Nn][Ff][Oo])$")
  add_test(png_idat "E:/Aulas/low-level-unified-portfolio/days/2026-09-06/tooling/png_idat_pipeline/solutions/build_ci/RelWithDebInfo/test_png.exe")
  set_tests_properties(png_idat PROPERTIES  _BACKTRACE_TRIPLES "E:/Aulas/low-level-unified-portfolio/days/2026-09-06/tooling/png_idat_pipeline/solutions/CMakeLists.txt;13;add_test;E:/Aulas/low-level-unified-portfolio/days/2026-09-06/tooling/png_idat_pipeline/solutions/CMakeLists.txt;0;")
else()
  add_test(png_idat NOT_AVAILABLE)
endif()
