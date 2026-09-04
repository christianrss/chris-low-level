#include "chris_js.hpp"

#include <iostream>
#include <stdexcept>

static void require(bool condition, const char* message) {
  if (!condition) {
    throw std::runtime_error(message);
  }
}

int main() {
  const auto program = chris::js::compile(
      "let x = 10; let y = 20; "
      "print(x + y * 2); print((y - x) * 3);");
  const auto output = chris::js::run(program);

  require(output.size() == 2, "output size");
  require(output[0] == 50, "precedence failed");
  require(output[1] == 30, "parentheses/sub failed");

  bool rejected = false;
  try {
    (void)chris::js::compile("let = 1;");
  } catch (const std::runtime_error&) {
    rejected = true;
  }
  require(rejected, "syntax error must fail");

  std::cout << "chris-js tests passed\n";
}
