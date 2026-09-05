// SOLVES [AI-MM-NAIVE-01] [AI-MM-TILED-02]
#include "matmul.hpp"
#include <algorithm>
#include <stdexcept>
static void check(const std::vector<float>&A,const std::vector<float>&B,std::size_t M,std::size_t K,std::size_t N){if(A.size()!=M*K||B.size()!=K*N)throw std::invalid_argument("shape mismatch");}
std::vector<float> matmul_naive(const std::vector<float>&A,const std::vector<float>&B,std::size_t M,std::size_t K,std::size_t N){check(A,B,M,K,N);std::vector<float>C(M*N,0);for(std::size_t i=0;i<M;++i)for(std::size_t j=0;j<N;++j){float s=0;for(std::size_t k=0;k<K;++k)s+=A[i*K+k]*B[k*N+j];C[i*N+j]=s;}return C;}
std::vector<float> matmul_tiled(const std::vector<float>&A,const std::vector<float>&B,std::size_t M,std::size_t K,std::size_t N,std::size_t tile){check(A,B,M,K,N);if(!tile)throw std::invalid_argument("tile 0");std::vector<float>C(M*N,0);for(std::size_t ii=0;ii<M;ii+=tile)for(std::size_t kk=0;kk<K;kk+=tile)for(std::size_t jj=0;jj<N;jj+=tile)for(std::size_t i=ii;i<std::min(ii+tile,M);++i)for(std::size_t k=kk;k<std::min(kk+tile,K);++k){float a=A[i*K+k];for(std::size_t j=jj;j<std::min(jj+tile,N);++j)C[i*N+j]+=a*B[k*N+j];}return C;}
