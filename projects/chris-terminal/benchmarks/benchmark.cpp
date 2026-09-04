#include "terminal.hpp"
#include <chrono>
#include <iostream>
#include <string>

int main() {
    std::string stream;
    stream.reserve(1 << 20);
    while (stream.size() < (1u << 20)) {
        stream += "hello\x1b[2D!\x1b[2Cworld\r\n";
    }
    Terminal term(120, 40);
    const auto start = std::chrono::steady_clock::now();
    for (int i = 0; i < 20; ++i) {
        term.feed(stream);
    }
    const auto end = std::chrono::steady_clock::now();
    const double seconds = std::chrono::duration<double>(end - start).count();
    const double mib = (stream.size() * 20.0) / (1024.0 * 1024.0);
    std::cout << "MiB=" << mib << " seconds=" << seconds << " MiB/s=" << (mib / seconds) << "\n";
}
