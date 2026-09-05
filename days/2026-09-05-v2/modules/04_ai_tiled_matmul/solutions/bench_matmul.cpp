#include "matmul.hpp"
#include <chrono>
#include <iostream>
int main(){
    size_t n=128;
    std::vector<float>A(n*n,1.0f),B(n*n,1.0f);
    for(bool tiled: {false,true}){
        auto s=std::chrono::steady_clock::now();
        auto C=tiled?matmul_tiled(A,B,n,n,n,32):matmul_naive(A,B,n,n,n);
        auto e=std::chrono::steady_clock::now();
        std::cout<<(tiled?"tiled":"naive")<<" ms="
                 <<std::chrono::duration<double,std::milli>(e-s).count()
                 <<" check="<<C[0]<<"\n";
    }
}
