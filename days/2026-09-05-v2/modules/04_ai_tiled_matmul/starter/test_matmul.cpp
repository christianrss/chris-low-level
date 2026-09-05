// TESTS [AI-MM-NAIVE-01] [AI-MM-TILED-02]
#include "matmul.hpp"
#include <cassert>
#include <cmath>
#include <cstdio>
int main(){std::vector<float>A={1,2,3,4,5,6},B={7,8,9,10,11,12};auto n=matmul_naive(A,B,2,3,2);auto t=matmul_tiled(A,B,2,3,2,2);float e[]={58,64,139,154};for(int i=0;i<4;i++){assert(std::fabs(n[i]-e[i])<1e-5);assert(std::fabs(t[i]-e[i])<1e-5);}puts("OK matmul");}
