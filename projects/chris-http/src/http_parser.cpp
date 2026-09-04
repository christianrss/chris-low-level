#include "http_parser.hpp"
#include <algorithm>
#include <cctype>
#include <sstream>
#include <stdexcept>

static std::string trim(std::string value) {
    while (!value.empty() && std::isspace(static_cast<unsigned char>(value.front()))) {
        value.erase(value.begin());
    }
    while (!value.empty() && std::isspace(static_cast<unsigned char>(value.back()))) {
        value.pop_back();
    }
    return value;
}

bool HttpRequestParser::feed(const std::string& bytes) {
    if (complete_) {
        throw std::logic_error("parser is already complete; call reset first");
    }
    buffer_ += bytes;
    try_parse();
    return complete_;
}

void HttpRequestParser::try_parse() {
    const std::size_t header_end = buffer_.find("\r\n\r\n");
    if (header_end == std::string::npos) {
        return;
    }

    std::istringstream stream(buffer_.substr(0, header_end));
    std::string line;
    if (!std::getline(stream, line)) {
        throw std::runtime_error("missing request line");
    }
    if (!line.empty() && line.back() == '\r') {
        line.pop_back();
    }
    std::istringstream first(line);
    if (!(first >> request_.method >> request_.target >> request_.version)) {
        throw std::runtime_error("malformed request line");
    }
    if (request_.version.rfind("HTTP/", 0) != 0) {
        throw std::runtime_error("unsupported request version syntax");
    }

    request_.headers.clear();
    while (std::getline(stream, line)) {
        if (!line.empty() && line.back() == '\r') {
            line.pop_back();
        }
        const auto colon = line.find(':');
        if (colon == std::string::npos) {
            throw std::runtime_error("malformed header");
        }
        request_.headers[trim(line.substr(0, colon))] = trim(line.substr(colon + 1));
    }

    std::size_t content_length = 0;
    const auto it = request_.headers.find("Content-Length");
    if (it != request_.headers.end()) {
        content_length = static_cast<std::size_t>(std::stoull(it->second));
    }
    const std::size_t body_start = header_end + 4;
    if (buffer_.size() < body_start + content_length) {
        return;
    }
    request_.body = buffer_.substr(body_start, content_length);
    complete_ = true;
}

const HttpRequest& HttpRequestParser::request() const {
    if (!complete_) {
        throw std::logic_error("request is not complete");
    }
    return request_;
}

void HttpRequestParser::reset() {
    buffer_.clear();
    request_ = HttpRequest{};
    complete_ = false;
}
