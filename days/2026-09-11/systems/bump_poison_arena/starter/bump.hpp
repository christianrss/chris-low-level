#pragma once
#include <cstddef>
#include <cstdint>
constexpr std::size_t ARENA_CAP = 64;
constexpr std::uint8_t POISON = 0xA5;
constexpr std::uint8_t CANARY = 0xC3;
struct BumpArena { std::uint8_t buf[ARENA_CAP]; std::size_t used; };
void arena_reset(BumpArena &a);
void *arena_alloc(BumpArena &a, std::size_t n);
int arena_check_canary(const BumpArena &a, const void *p, std::size_t n);
