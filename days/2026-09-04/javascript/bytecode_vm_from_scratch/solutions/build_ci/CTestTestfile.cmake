# CMake generated Testfile for 
# Source directory: E:/Aulas/low-level-unified-portfolio/days/2026-09-04/javascript/bytecode_vm_from_scratch/solutions
# Build directory: E:/Aulas/low-level-unified-portfolio/days/2026-09-04/javascript/bytecode_vm_from_scratch/solutions/build_ci
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
if(CTEST_CONFIGURATION_TYPE MATCHES "^([Dd][Ee][Bb][Uu][Gg])$")
  add_test([=[chris_js_tests]=] "E:/Aulas/low-level-unified-portfolio/days/2026-09-04/javascript/bytecode_vm_from_scratch/solutions/build_ci/Debug/chris_js_tests.exe")
  set_tests_properties([=[chris_js_tests]=] PROPERTIES  _BACKTRACE_TRIPLES "E:/Aulas/low-level-unified-portfolio/days/2026-09-04/javascript/bytecode_vm_from_scratch/solutions/CMakeLists.txt;18;add_test;E:/Aulas/low-level-unified-portfolio/days/2026-09-04/javascript/bytecode_vm_from_scratch/solutions/CMakeLists.txt;0;")
elseif(CTEST_CONFIGURATION_TYPE MATCHES "^([Rr][Ee][Ll][Ee][Aa][Ss][Ee])$")
  add_test([=[chris_js_tests]=] "E:/Aulas/low-level-unified-portfolio/days/2026-09-04/javascript/bytecode_vm_from_scratch/solutions/build_ci/Release/chris_js_tests.exe")
  set_tests_properties([=[chris_js_tests]=] PROPERTIES  _BACKTRACE_TRIPLES "E:/Aulas/low-level-unified-portfolio/days/2026-09-04/javascript/bytecode_vm_from_scratch/solutions/CMakeLists.txt;18;add_test;E:/Aulas/low-level-unified-portfolio/days/2026-09-04/javascript/bytecode_vm_from_scratch/solutions/CMakeLists.txt;0;")
elseif(CTEST_CONFIGURATION_TYPE MATCHES "^([Mm][Ii][Nn][Ss][Ii][Zz][Ee][Rr][Ee][Ll])$")
  add_test([=[chris_js_tests]=] "E:/Aulas/low-level-unified-portfolio/days/2026-09-04/javascript/bytecode_vm_from_scratch/solutions/build_ci/MinSizeRel/chris_js_tests.exe")
  set_tests_properties([=[chris_js_tests]=] PROPERTIES  _BACKTRACE_TRIPLES "E:/Aulas/low-level-unified-portfolio/days/2026-09-04/javascript/bytecode_vm_from_scratch/solutions/CMakeLists.txt;18;add_test;E:/Aulas/low-level-unified-portfolio/days/2026-09-04/javascript/bytecode_vm_from_scratch/solutions/CMakeLists.txt;0;")
elseif(CTEST_CONFIGURATION_TYPE MATCHES "^([Rr][Ee][Ll][Ww][Ii][Tt][Hh][Dd][Ee][Bb][Ii][Nn][Ff][Oo])$")
  add_test([=[chris_js_tests]=] "E:/Aulas/low-level-unified-portfolio/days/2026-09-04/javascript/bytecode_vm_from_scratch/solutions/build_ci/RelWithDebInfo/chris_js_tests.exe")
  set_tests_properties([=[chris_js_tests]=] PROPERTIES  _BACKTRACE_TRIPLES "E:/Aulas/low-level-unified-portfolio/days/2026-09-04/javascript/bytecode_vm_from_scratch/solutions/CMakeLists.txt;18;add_test;E:/Aulas/low-level-unified-portfolio/days/2026-09-04/javascript/bytecode_vm_from_scratch/solutions/CMakeLists.txt;0;")
else()
  add_test([=[chris_js_tests]=] NOT_AVAILABLE)
endif()
