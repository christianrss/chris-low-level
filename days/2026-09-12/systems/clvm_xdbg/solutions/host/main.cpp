#include "session.hpp"

#include <chrono>
#include <fstream>
#include <iostream>
#include <iterator>
#include <sstream>
#include <string>
#include <vector>

namespace {

const char* status_name(DbgStatus status) {
    switch (status) {
        case DbgStatus::Ready:
            return "ready";
        case DbgStatus::Halted:
            return "halted";
        case DbgStatus::Breakpoint:
            return "breakpoint";
        case DbgStatus::Error:
            return "error";
    }
    return "error";
}

void print_status(const Session& session) {
    std::cout << "pc=" << session.pc << " status=" << status_name(session.status);
    if (session.status == DbgStatus::Error && !session.last_error.empty()) {
        std::cout << "\nerror: " << session.last_error;
    }
    std::cout << '\n';
}

bool load_path(Session& session, const std::string& path) {
    std::ifstream input(path, std::ios::binary);
    if (!input) {
        std::cerr << "error: cannot open file\n";
        return false;
    }
    const std::vector<std::uint8_t> file{
        std::istreambuf_iterator<char>(input),
        std::istreambuf_iterator<char>()};
    if (!session.load(file.data(), file.size())) {
        std::cerr << "parse error: " << session.last_error << '\n';
        return false;
    }
    std::cout << "ready pc=" << session.pc << " bytes=" << session.file.size() << '\n';
    return true;
}

int run_bench(Session& session, std::size_t count) {
    const auto start = std::chrono::steady_clock::now();
    std::size_t executed = 0;
    while (executed < count && session.status == DbgStatus::Ready) {
        session.step();
        ++executed;
    }
    const auto elapsed = std::chrono::steady_clock::now() - start;
    const auto ns = std::chrono::duration_cast<std::chrono::nanoseconds>(elapsed).count();
    std::cout << "steps=" << executed << " ns=" << ns << " status="
              << status_name(session.status) << '\n';
    return session.status == DbgStatus::Error ? 2 : 0;
}

int run_repl(Session& session) {
    std::string line;
    while (std::getline(std::cin, line)) {
        if (!line.empty() && line.back() == '\r') {
            line.pop_back();
        }
        std::istringstream words(line);
        std::string cmd;
        words >> cmd;
        if (cmd.empty()) {
            continue;
        }
        if (cmd == "quit" || cmd == "q") {
            return 0;
        }
        if (cmd == "hex") {
            std::cout << session.hex_dump();
            if (session.hex_dump().empty() || session.hex_dump().back() != '\n') {
                std::cout << '\n';
            }
            continue;
        }
        if (cmd == "disasm") {
            std::cout << session.disasm() << '\n';
            continue;
        }
        if (cmd == "regs") {
            std::cout << session.regs();
            if (session.regs().empty() || session.regs().back() != '\n') {
                std::cout << '\n';
            }
            continue;
        }
        if (cmd == "mem") {
            std::size_t addr = 0;
            std::size_t len = 64;
            words >> addr >> len;
            std::cout << session.mem_view(addr, len);
            if (session.mem_view(addr, len).empty() ||
                session.mem_view(addr, len).back() != '\n') {
                std::cout << '\n';
            }
            continue;
        }
        if (cmd == "step") {
            session.step();
            print_status(session);
            continue;
        }
        if (cmd == "break") {
            std::size_t at = 0;
            if (!(words >> at)) {
                std::cout << "error: break needs a pc\n";
                continue;
            }
            session.set_break(at);
            std::cout << "breakpoint " << at << '\n';
            continue;
        }
        if (cmd == "continue" || cmd == "cont") {
            session.cont();
            print_status(session);
            continue;
        }
        std::cout << "error: unknown command\n";
    }
    return 0;
}

}  // namespace

int main(int argc, char** argv) {
    if (argc < 2) {
        std::cerr << "usage: clvm-xdbg <program.clvm> [--bench N]\n";
        return 1;
    }
    Session session;
    if (!load_path(session, argv[1])) {
        return 1;
    }
    if (argc >= 3 && std::string(argv[2]) == "--bench") {
        const std::size_t count = argc >= 4 ? static_cast<std::size_t>(std::stoul(argv[3])) : 10000U;
        return run_bench(session, count);
    }
    return run_repl(session);
}
