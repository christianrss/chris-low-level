#include "arena.hpp"
#include <stdexcept>

Arena::Arena(std::size_t capacity) : storage_(capacity) {
    if (capacity == 0) {
        throw std::invalid_argument("arena capacity must be non-zero");
    }
}

bool Arena::is_power_of_two(std::size_t value) noexcept {
    // TODO [D2-ARENA-POWER2]: retorne true apenas para potencias de dois nao nulas.
    return false;
}

std::size_t Arena::align_up(std::size_t value, std::size_t alignment) {
    // TODO [D2-ARENA-ALIGN-UP]: valide alignment e arredonde value para cima.
    (void)value;
    (void)alignment;
    throw std::logic_error("TODO align_up");
}

void* Arena::allocate(std::size_t size, std::size_t alignment) {
    // TODO [D2-ARENA-ALLOCATE]: valide size, alinhe base+offset, teste capacidade,
    // atualize offset_ e retorne o endereço dentro de storage_.
    (void)size;
    (void)alignment;
    throw std::logic_error("TODO allocate");
}

void Arena::reset() noexcept {
    // TODO [D2-ARENA-RESET]: uma arena reseta em O(1), sem liberar bloco por bloco.
}
