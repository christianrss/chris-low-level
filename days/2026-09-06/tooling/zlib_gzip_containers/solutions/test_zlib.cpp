// PEDAGOGY-TEST: COMP-ZLIB-01: Adler32 conhecido
// PEDAGOGY-TEST: COMP-ZLIB-02: zlib compress CMF/FLG
// PEDAGOGY-TEST: COMP-ZLIB-03: zlib decompress + Adler
// PEDAGOGY-TEST: COMP-ZLIB-04: gzip CRC32 roundtrip
#include "adler32.hpp"
#include "crc32.hpp"
#include "gzip_wrap.hpp"
#include "zlib_wrap.hpp"
#include <iostream>
#include <string>
#include <vector>

#define REQUIRE(cond) \
    do { \
        if (!(cond)) { \
            std::cerr << "FAIL: " << __FILE__ << ":" << __LINE__ << "\n"; \
            return 1; \
        } \
    } while (0)

int main() {
    const std::string wiki = "Wikipedia";
    std::vector<std::uint8_t> wiki_bytes(wiki.begin(), wiki.end());
    REQUIRE(adler32(wiki_bytes) == 0x11e60398u);

    const std::vector<std::uint8_t> payload = {'z', 'l', 'i', 'b'};
    const auto pkt = zlib_compress(payload);
    REQUIRE(pkt.cmf == 0x78);
    REQUIRE(((pkt.cmf << 8) + pkt.flg) % 31 == 0);
    const auto blob = zlib_blob_from_packet(pkt);
    const auto out = zlib_decompress(blob);
    REQUIRE(out == payload);

    const auto gz = gzip_compress(payload);
    REQUIRE(gz[0] == 0x1F && gz[1] == 0x8B);
    const auto gunz = gzip_decompress(gz);
    REQUIRE(gunz == payload);

    std::cout << "OK zlib gzip containers\n";
    return 0;
}
