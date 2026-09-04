#include "http_parser.hpp"
#include <chrono>
#include <iostream>
#include <string>

int main() {
    const std::string request = "GET /bench HTTP/1.1\r\nHost: localhost\r\nUser-Agent: chris-http\r\nAccept: */*\r\n\r\n";
    constexpr int iterations = 200000;
    const auto start = std::chrono::steady_clock::now();
    std::size_t checksum = 0;
    for (int i = 0; i < iterations; ++i) {
        HttpRequestParser parser;
        parser.feed(request);
        checksum += parser.request().target.size();
    }
    const auto end = std::chrono::steady_clock::now();
    const double seconds = std::chrono::duration<double>(end - start).count();
    std::cout << "requests=" << iterations << " seconds=" << seconds
              << " req/s=" << (iterations / seconds) << " checksum=" << checksum << "\n";
}
