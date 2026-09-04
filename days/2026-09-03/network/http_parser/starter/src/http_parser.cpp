#include "http_parser.hpp"
#include <stdexcept>

bool HttpRequestParser::feed(const std::string& bytes) {
    buffer_ += bytes;
    try_parse();
    return complete_;
}

void HttpRequestParser::try_parse() {
    // TODO: find CRLF CRLF, parse request line/headers and wait for Content-Length bytes.
}

const HttpRequest& HttpRequestParser::request() const {
    if (!complete_) throw std::logic_error("request is not complete");
    return request_;
}

void HttpRequestParser::reset() {
    buffer_.clear();
    request_ = HttpRequest{};
    complete_ = false;
}
