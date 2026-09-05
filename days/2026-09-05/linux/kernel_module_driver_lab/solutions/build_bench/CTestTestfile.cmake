# CMake generated Testfile for 
# Source directory: E:/Aulas/low-level-unified-portfolio/days/2026-09-05/linux/kernel_module_driver_lab/solutions
# Build directory: E:/Aulas/low-level-unified-portfolio/days/2026-09-05/linux/kernel_module_driver_lab/solutions/build_bench
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
if(CTEST_CONFIGURATION_TYPE MATCHES "^([Dd][Ee][Bb][Uu][Gg])$")
  add_test(kmod_model "E:/Aulas/low-level-unified-portfolio/days/2026-09-05/linux/kernel_module_driver_lab/solutions/build_bench/Debug/kmod_model.exe")
  set_tests_properties(kmod_model PROPERTIES  _BACKTRACE_TRIPLES "E:/Aulas/low-level-unified-portfolio/days/2026-09-05/linux/kernel_module_driver_lab/solutions/CMakeLists.txt;5;add_test;E:/Aulas/low-level-unified-portfolio/days/2026-09-05/linux/kernel_module_driver_lab/solutions/CMakeLists.txt;0;")
elseif(CTEST_CONFIGURATION_TYPE MATCHES "^([Rr][Ee][Ll][Ee][Aa][Ss][Ee])$")
  add_test(kmod_model "E:/Aulas/low-level-unified-portfolio/days/2026-09-05/linux/kernel_module_driver_lab/solutions/build_bench/Release/kmod_model.exe")
  set_tests_properties(kmod_model PROPERTIES  _BACKTRACE_TRIPLES "E:/Aulas/low-level-unified-portfolio/days/2026-09-05/linux/kernel_module_driver_lab/solutions/CMakeLists.txt;5;add_test;E:/Aulas/low-level-unified-portfolio/days/2026-09-05/linux/kernel_module_driver_lab/solutions/CMakeLists.txt;0;")
elseif(CTEST_CONFIGURATION_TYPE MATCHES "^([Mm][Ii][Nn][Ss][Ii][Zz][Ee][Rr][Ee][Ll])$")
  add_test(kmod_model "E:/Aulas/low-level-unified-portfolio/days/2026-09-05/linux/kernel_module_driver_lab/solutions/build_bench/MinSizeRel/kmod_model.exe")
  set_tests_properties(kmod_model PROPERTIES  _BACKTRACE_TRIPLES "E:/Aulas/low-level-unified-portfolio/days/2026-09-05/linux/kernel_module_driver_lab/solutions/CMakeLists.txt;5;add_test;E:/Aulas/low-level-unified-portfolio/days/2026-09-05/linux/kernel_module_driver_lab/solutions/CMakeLists.txt;0;")
elseif(CTEST_CONFIGURATION_TYPE MATCHES "^([Rr][Ee][Ll][Ww][Ii][Tt][Hh][Dd][Ee][Bb][Ii][Nn][Ff][Oo])$")
  add_test(kmod_model "E:/Aulas/low-level-unified-portfolio/days/2026-09-05/linux/kernel_module_driver_lab/solutions/build_bench/RelWithDebInfo/kmod_model.exe")
  set_tests_properties(kmod_model PROPERTIES  _BACKTRACE_TRIPLES "E:/Aulas/low-level-unified-portfolio/days/2026-09-05/linux/kernel_module_driver_lab/solutions/CMakeLists.txt;5;add_test;E:/Aulas/low-level-unified-portfolio/days/2026-09-05/linux/kernel_module_driver_lab/solutions/CMakeLists.txt;0;")
else()
  add_test(kmod_model NOT_AVAILABLE)
endif()
