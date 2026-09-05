# CMake generated Testfile for 
# Source directory: E:/Aulas/low-level-unified-portfolio/days/2026-09-05/systems/bitmap_page_allocator/solutions
# Build directory: E:/Aulas/low-level-unified-portfolio/days/2026-09-05/systems/bitmap_page_allocator/solutions/build_bench
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
if(CTEST_CONFIGURATION_TYPE MATCHES "^([Dd][Ee][Bb][Uu][Gg])$")
  add_test(page_allocator "E:/Aulas/low-level-unified-portfolio/days/2026-09-05/systems/bitmap_page_allocator/solutions/build_bench/Debug/test_page.exe")
  set_tests_properties(page_allocator PROPERTIES  _BACKTRACE_TRIPLES "E:/Aulas/low-level-unified-portfolio/days/2026-09-05/systems/bitmap_page_allocator/solutions/CMakeLists.txt;6;add_test;E:/Aulas/low-level-unified-portfolio/days/2026-09-05/systems/bitmap_page_allocator/solutions/CMakeLists.txt;0;")
elseif(CTEST_CONFIGURATION_TYPE MATCHES "^([Rr][Ee][Ll][Ee][Aa][Ss][Ee])$")
  add_test(page_allocator "E:/Aulas/low-level-unified-portfolio/days/2026-09-05/systems/bitmap_page_allocator/solutions/build_bench/Release/test_page.exe")
  set_tests_properties(page_allocator PROPERTIES  _BACKTRACE_TRIPLES "E:/Aulas/low-level-unified-portfolio/days/2026-09-05/systems/bitmap_page_allocator/solutions/CMakeLists.txt;6;add_test;E:/Aulas/low-level-unified-portfolio/days/2026-09-05/systems/bitmap_page_allocator/solutions/CMakeLists.txt;0;")
elseif(CTEST_CONFIGURATION_TYPE MATCHES "^([Mm][Ii][Nn][Ss][Ii][Zz][Ee][Rr][Ee][Ll])$")
  add_test(page_allocator "E:/Aulas/low-level-unified-portfolio/days/2026-09-05/systems/bitmap_page_allocator/solutions/build_bench/MinSizeRel/test_page.exe")
  set_tests_properties(page_allocator PROPERTIES  _BACKTRACE_TRIPLES "E:/Aulas/low-level-unified-portfolio/days/2026-09-05/systems/bitmap_page_allocator/solutions/CMakeLists.txt;6;add_test;E:/Aulas/low-level-unified-portfolio/days/2026-09-05/systems/bitmap_page_allocator/solutions/CMakeLists.txt;0;")
elseif(CTEST_CONFIGURATION_TYPE MATCHES "^([Rr][Ee][Ll][Ww][Ii][Tt][Hh][Dd][Ee][Bb][Ii][Nn][Ff][Oo])$")
  add_test(page_allocator "E:/Aulas/low-level-unified-portfolio/days/2026-09-05/systems/bitmap_page_allocator/solutions/build_bench/RelWithDebInfo/test_page.exe")
  set_tests_properties(page_allocator PROPERTIES  _BACKTRACE_TRIPLES "E:/Aulas/low-level-unified-portfolio/days/2026-09-05/systems/bitmap_page_allocator/solutions/CMakeLists.txt;6;add_test;E:/Aulas/low-level-unified-portfolio/days/2026-09-05/systems/bitmap_page_allocator/solutions/CMakeLists.txt;0;")
else()
  add_test(page_allocator NOT_AVAILABLE)
endif()
