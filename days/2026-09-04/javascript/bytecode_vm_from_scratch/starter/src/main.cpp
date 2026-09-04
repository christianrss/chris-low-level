#include "chris_js.hpp"

#include <iostream>

int main() {
  const std::string source =
      "let x = 10; let y = 20; print(x + y * 2);";
  const auto output = chris::js::run(chris::js::compile(source));
  for (const auto value : output) {
    std::cout << value << '\n';
  }
}
