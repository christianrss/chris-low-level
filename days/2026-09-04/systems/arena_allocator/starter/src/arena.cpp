#include "arena.hpp"
#include <stdexcept>

Arena::Arena(std::size_t capacity) : storage_(capacity) {
    if (capacity == 0) {
        throw std::invalid_argument("arena capacity must be non-zero");
    }
}

bool Arena::is_power_of_two(std::size_t value) noexcept {
    // TODO ETAPA 1: retorne true apenas para potências de dois não nulas.
    return false;
}

std::size_t Arena::align_up(std::size_t value, std::size_t alignment) {
    // TODO ETAPA 2: valide alignment e arredonde value para cima.
    (void)value;
    (void)alignment;
    throw std::logic_error("TODO align_up");
}

void* Arena::allocate(std::size_t size, std::size_t alignment) {
    // TODO ETAPA 3: valide size, alinhe base+offset, teste capacidade,
    // atualize offset_ e retorne o endereço dentro de storage_.
    (void)size;
    (void)alignment;
    throw std::logic_error("TODO allocate");
}

void Arena::reset() noexcept {
    // TODO ETAPA 4: uma arena reseta em O(1), sem liberar bloco por bloco.
}
