#pragma once
#include <atomic>
#include <cstddef>
#include <vector>
class SpscRing {
public:
 explicit SpscRing(std::size_t capacity);
 bool push(int value);
 bool pop(int& out);
 std::size_t size_approx() const;
private:
 std::vector<int> storage_;
 std::atomic<std::size_t> head_{0}, tail_{0};
};