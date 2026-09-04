#include "descriptor_ring.hpp"
#include <cassert>
#include <iostream>

int main() {
    DescriptorRing ring(2);
    assert(ring.submit(64));
    assert(ring.submit(128));
    assert(!ring.submit(256));
    assert(!ring.reclaim().has_value());

    assert(ring.device_complete_one());
    auto first = ring.reclaim();
    assert(first.has_value() && *first == 64);

    assert(ring.submit(256));
    assert(ring.device_complete_one());
    auto second = ring.reclaim();
    assert(second.has_value() && *second == 128);
    assert(ring.device_complete_one());
    auto third = ring.reclaim();
    assert(third.has_value() && *third == 256);
    assert(ring.outstanding() == 0);

    std::cout << "descriptor ring tests passed\n";
}
