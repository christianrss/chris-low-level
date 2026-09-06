#include "checkpoint.hpp"
#include "game.hpp"

namespace lantern {

void checkpoint_save(const GameState& /*state*/, CheckpointData& out) {
    // TODO [LANTERN-CHK-16]: salvar posição, vida, respiração e progresso.
    out.valid = false;
}

void checkpoint_restore(GameState& /*state*/, const CheckpointData& /*data*/) {
    // TODO [LANTERN-CHK-16]: restaurar estado do último altar ativado.
}

} // namespace lantern
