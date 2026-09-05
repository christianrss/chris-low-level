// PEDAGOGY-TEST: HTTP-PARSE-01
// Test cases (TESTES_GUIADOS.md):
// Caso 1: Escreva um teste do comportamento mais simples antes de adicionar a feature.
// Caso 2: Rode e observe a falha.
// Caso 3: Implemente apenas o necessario para esse teste.
// Caso 4: Adicione edge case/erro relevante.
// Caso 5: Quando encontrar um bug durante o exercicio, transforme-o em regression test ant
#include "http_parser.hpp"
#include <cassert>
#include <iostream>
#include <stdexcept>

int main() {
    HttpRequestParser parser;
    assert(!parser.feed("GET /hello HTTP/1.1\r\nHost: ex"));
    assert(parser.feed("ample.test\r\n\r\n"));
    assert(parser.request().method == "GET");
    assert(parser.request().target == "/hello");
    assert(parser.request().headers.at("Host") == "example.test");

    parser.reset();
    assert(!parser.feed("POST /x HTTP/1.1\r\nContent-Length: 5\r\n\r\nhe"));
    assert(parser.feed("llo"));
    assert(parser.request().body == "hello");

    bool threw = false;
    try {
        HttpRequestParser bad;
        bad.feed("BROKEN\r\n\r\n");
    } catch (const std::runtime_error&) {
        threw = true;
    }
    assert(threw);

    std::cout << "http parser tests passed\n";
}