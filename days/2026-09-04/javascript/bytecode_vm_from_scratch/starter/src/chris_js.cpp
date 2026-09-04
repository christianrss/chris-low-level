#include "chris_js.hpp"

#include <cctype>
#include <stdexcept>
#include <utility>

namespace chris::js {
namespace {

enum class Kind {
  End,
  Let,
  Print,
  Identifier,
  Number,
  Equal,
  Plus,
  Minus,
  Star,
  LParen,
  RParen,
  Semicolon,
};

struct Token {
  Kind kind;
  std::string text;
  std::int64_t number{};
};

class Lexer {
 public:
  explicit Lexer(std::string source) : source_(std::move(source)) {}

  Token next() {
    while (pos_ < source_.size() &&
           std::isspace(static_cast<unsigned char>(source_[pos_]))) {
      ++pos_;
    }

    if (pos_ == source_.size()) {
      return {Kind::End, {}};
    }

    const char c = source_[pos_];
    if (std::isdigit(static_cast<unsigned char>(c))) {
      const auto start = pos_;
      std::int64_t value = 0;
      while (pos_ < source_.size() &&
             std::isdigit(static_cast<unsigned char>(source_[pos_]))) {
        value = value * 10 + (source_[pos_] - '0');
        ++pos_;
      }
      return {Kind::Number, source_.substr(start, pos_ - start), value};
    }

    if (std::isalpha(static_cast<unsigned char>(c)) || c == '_') {
      const auto start = pos_++;
      while (pos_ < source_.size() &&
             (std::isalnum(static_cast<unsigned char>(source_[pos_])) ||
              source_[pos_] == '_')) {
        ++pos_;
      }

      auto text = source_.substr(start, pos_ - start);
      if (text == "let") {
        return {Kind::Let, text};
      }
      if (text == "print") {
        return {Kind::Print, text};
      }
      return {Kind::Identifier, text};
    }

    ++pos_;
    switch (c) {
      case '=':
        return {Kind::Equal, "="};
      case '+':
        return {Kind::Plus, "+"};
      case '-':
        return {Kind::Minus, "-"};
      case '*':
        return {Kind::Star, "*"};
      case '(':
        return {Kind::LParen, "("};
      case ')':
        return {Kind::RParen, ")"};
      case ';':
        return {Kind::Semicolon, ";"};
      default:
        throw std::runtime_error("unexpected character");
    }
  }

 private:
  std::string source_;
  std::size_t pos_{};
};

class Compiler {
 public:
  explicit Compiler(const std::string& source) : lexer_(source) { advance(); }

  Program compile_program() {
    while (current_.kind != Kind::End) {
      statement();
    }
    emit(Op::Halt);
    return std::move(program_);
  }

 private:
  void advance() { current_ = lexer_.next(); }

  void expect(Kind kind) {
    if (current_.kind != kind) {
      throw std::runtime_error("unexpected token: " + current_.text);
    }
    advance();
  }

  std::int64_t name_index(const std::string& name) {
    for (std::size_t i = 0; i < program_.names.size(); ++i) {
      if (program_.names[i] == name) {
        return static_cast<std::int64_t>(i);
      }
    }
    program_.names.push_back(name);
    return static_cast<std::int64_t>(program_.names.size() - 1);
  }

  void emit(Op op, std::int64_t operand = 0) {
    program_.code.push_back({op, operand});
  }

  void statement() {
    if (current_.kind == Kind::Let) {
      advance();
      if (current_.kind != Kind::Identifier) {
        throw std::runtime_error("expected identifier");
      }
      const auto idx = name_index(current_.text);
      advance();
      expect(Kind::Equal);
      expression();
      expect(Kind::Semicolon);
      emit(Op::StoreGlobal, idx);
      return;
    }

    if (current_.kind == Kind::Print) {
      advance();
      expect(Kind::LParen);
      expression();
      expect(Kind::RParen);
      expect(Kind::Semicolon);
      emit(Op::Print);
      return;
    }

    throw std::runtime_error("expected statement");
  }

  void expression() {
    term();
    while (current_.kind == Kind::Plus || current_.kind == Kind::Minus) {
      const auto kind = current_.kind;
      advance();
      term();
      emit(kind == Kind::Plus ? Op::Add : Op::Sub);
    }
  }

  void term() {
    factor();
    while (current_.kind == Kind::Star) {
      advance();
      factor();
      emit(Op::Mul);
    }
  }

  void factor() {
    if (current_.kind == Kind::Number) {
      const auto idx = static_cast<std::int64_t>(program_.constants.size());
      program_.constants.push_back(current_.number);
      advance();
      emit(Op::PushConst, idx);
      return;
    }

    if (current_.kind == Kind::Identifier) {
      const auto idx = name_index(current_.text);
      advance();
      emit(Op::LoadGlobal, idx);
      return;
    }

    if (current_.kind == Kind::LParen) {
      advance();
      expression();
      expect(Kind::RParen);
      return;
    }

    throw std::runtime_error("expected expression");
  }

  Lexer lexer_;
  Token current_{};
  Program program_{};
};

}  // namespace

Program compile(const std::string& source) {
  return Compiler(source).compile_program();
}

std::vector<std::int64_t> run(const Program& program) {
  std::vector<std::int64_t> stack;
  std::vector<std::int64_t> globals(program.names.size());
  std::vector<std::int64_t> output;

  auto pop = [&]() {
    if (stack.empty()) {
      throw std::runtime_error("VM stack underflow");
    }
    const auto value = stack.back();
    stack.pop_back();
    return value;
  };

  for (std::size_t ip = 0; ip < program.code.size(); ++ip) {
    const auto ins = program.code[ip];
    switch (ins.op) {
      case Op::PushConst:
        stack.push_back(program.constants.at(static_cast<std::size_t>(ins.operand)));
        break;
      case Op::LoadGlobal:
        stack.push_back(globals.at(static_cast<std::size_t>(ins.operand)));
        break;
      case Op::StoreGlobal:
        globals.at(static_cast<std::size_t>(ins.operand)) = pop();
        break;
      case Op::Add: {
        const auto b = pop();
        const auto a = pop();
        // TODO DAY02: push a + b instead of only a.
        stack.push_back(a);
        (void)b;
        break;
      }
      case Op::Sub: {
        const auto b = pop();
        const auto a = pop();
        stack.push_back(a - b);
        break;
      }
      case Op::Mul: {
        const auto b = pop();
        const auto a = pop();
        stack.push_back(a * b);
        break;
      }
      case Op::Print:
        output.push_back(pop());
        break;
      case Op::Halt:
        return output;
    }
  }

  throw std::runtime_error("program terminated without Halt");
}

}  // namespace chris::js
