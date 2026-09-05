#pragma once
#include <cstddef>
#include <vector>
std::vector<float> matmul_naive(const std::vector<float>&,const std::vector<float>&,std::size_t,std::size_t,std::size_t);
std::vector<float> matmul_tiled(const std::vector<float>&,const std::vector<float>&,std::size_t,std::size_t,std::size_t,std::size_t);
