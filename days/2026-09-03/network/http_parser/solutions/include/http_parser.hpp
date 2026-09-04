#pragma once
#include <cstddef>
#include <map>
#include <string>

struct HttpRequest {
    std::string method;
    std::string target;
    std::string version;
    std::map<std::string, std::string> headers;
    std::string body;
};

class HttpRequestParser {
public:
    bool feed(const std::string& bytes);
    bool complete() const { return complete_; }
    const HttpRequest& request() const;
    void reset();

private:
    void try_parse();
    std::string buffer_;
    HttpRequest request_;
    bool complete_ = false;
};
