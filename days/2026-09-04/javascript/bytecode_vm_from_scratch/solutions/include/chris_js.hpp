#pragma once
#include <cstdint>
#include <string>
#include <unordered_map>
#include <vector>

namespace chris::js {
enum class Op : std::uint8_t { PushConst, LoadGlobal, StoreGlobal, Add, Sub, Mul, Print, Halt };
struct Instruction { Op op; std::int64_t operand{}; };
struct Program { std::vector<Instruction> code; std::vector<std::int64_t> constants; std::vector<std::string> names; };
Program compile(const std::string& source);
std::vector<std::int64_t> run(const Program& program);
}
