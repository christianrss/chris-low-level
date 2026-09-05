#include "matmul.hpp"
#include <stdexcept>
std::vector<float> matmul_naive(const std::vector<float>&A,const std::vector<float>&B,std::size_t M,std::size_t K,std::size_t N){/* TODO [AI-MM-NAIVE-01] */return std::vector<float>(M*N);}
std::vector<float> matmul_tiled(const std::vector<float>&A,const std::vector<float>&B,std::size_t M,std::size_t K,std::size_t N,std::size_t tile){/* TODO [AI-MM-TILED-02] */return std::vector<float>(M*N);}
