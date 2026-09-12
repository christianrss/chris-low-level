# Resolucao guiada — shader_stage_fsm

## Mapa exato starter → resolucao

| TODO ID | Arquivo starter | Funcao / ancora | Substituir |
|---------|-----------------|-----------------|------------|
| `GFX-SH-ADVANCE` | `starter/core/shader_fsm.cpp` | `ShaderFsm::advance` | stub `TODO [GFX-SH-ADVANCE]` |
| `GFX-SH-RESET` | `starter/core/shader_fsm.cpp` | `ShaderFsm::reset` | stub `TODO [GFX-SH-RESET]` |
| `GFX-SH-COLOR` | `starter/core/shader_fsm.cpp` | `ShaderFsm::stage_color` | stub `TODO [GFX-SH-COLOR]` |

---

## Baseline

```powershell
cd days/2026-09-08/graphics/shader_stage_fsm/starter
cmake -S . -B build_ci -G Ninja -DCMAKE_BUILD_TYPE=Release
cmake --build build_ci
ctest --test-dir build_ci --output-on-failure
```

**Esperado antes dos TODOs:** compila; `test_shader_stage_fsm` falha no primeiro `assert` de `advance` (permanece Edit).

---

## Relatorio de resolucao

Preencha apos passar o ctest:

| TODO | Status | Notas |
|------|--------|-------|
| GFX-SH-ADVANCE | | |
| GFX-SH-RESET | | |
| GFX-SH-COLOR | | |

---

## GFX-SH-ADVANCE — `advance`

### Onde colocar (ADVANCE)

| Campo | Valor |
|-------|-------|
| **Arquivo** | `starter/core/shader_fsm.cpp` |
| **Funcao / ancora** | `ShaderFsm::advance` |
| **Substituir** | corpo com `TODO [GFX-SH-ADVANCE]` |
| **Nao mexer** | construtor, `stage()` |

### 1. O problema (ADVANCE)

Sem `advance`, o triangulo fica amarelo (Edit) para sempre e o Caso 1 falha.

### Escreva o codigo (ADVANCE)

```cpp
void ShaderFsm::advance() {
    switch (stage_) {
    case Stage::Edit:
        stage_ = Stage::Compile;
        break;
    case Stage::Compile:
        stage_ = Stage::Link;
        break;
    case Stage::Link:
        stage_ = Stage::Ready;
        break;
    case Stage::Ready:
        stage_ = Stage::Edit;
        break;
    }
}
```

### Por que funciona (ADVANCE)

Cada estado tem exatamente um sucessor; Ready volta a Edit para fechar o ciclo pedagogico.

### Verifique (ADVANCE)

Caso 1: quatro `advance` a partir de Edit terminam em Edit novamente.

---

## GFX-SH-RESET — `reset`

### Onde colocar (RESET)

| Campo | Valor |
|-------|-------|
| **Arquivo** | `starter/core/shader_fsm.cpp` |
| **Funcao / ancora** | `ShaderFsm::reset` |
| **Substituir** | corpo com `TODO [GFX-SH-RESET]` |
| **Nao mexer** | `advance` ja resolvido |

### 1. O problema (RESET)

Sem reset, tecla R na demo e o Caso 2 nao restauram o editor.

### Escreva o codigo (RESET)

```cpp
void ShaderFsm::reset() {
    stage_ = Stage::Edit;
}
```

### Por que funciona (RESET)

Atribuicao direta ignora o caminho ciclico — espelha “discard shader” em toolchains.

### Verifique (RESET)

Caso 2: apos dois advances (Link), `reset()` → Edit.

---

## GFX-SH-COLOR — `stage_color`

### Onde colocar (COLOR)

| Campo | Valor |
|-------|-------|
| **Arquivo** | `starter/core/shader_fsm.cpp` |
| **Funcao / ancora** | `ShaderFsm::stage_color` |
| **Substituir** | corpo com `TODO [GFX-SH-COLOR]` |
| **Nao mexer** | backends (ja leem a API) |

### 1. O problema (COLOR)

Sem cores corretas, HUD e triangulo ficam pretos; asserts RGB falham.

### Escreva o codigo (COLOR)

```cpp
Rgb ShaderFsm::stage_color() const {
    switch (stage_) {
    case Stage::Edit:
        return {0.95f, 0.75f, 0.20f};
    case Stage::Compile:
        return {0.25f, 0.55f, 0.95f};
    case Stage::Link:
        return {0.70f, 0.35f, 0.90f};
    case Stage::Ready:
        return {0.25f, 0.85f, 0.40f};
    }
    return {1.0f, 1.0f, 1.0f};
}
```

### Por que funciona (COLOR)

Constantes batem com a tabela da TEORIA e com `near()` no teste — contrato unico CPU/GL.

### Verifique (COLOR)

Caso 3: cores Edit/Compile/Link/Ready batem com tolerancia 1e-4.

---

## Debug

| Sintoma | Causa | Acao |
|---------|-------|------|
| assert Compile falhou | esquceu break / fallthrough | use break em cada case |
| cor Link != roxo | valores trocados | copie a tabela literal |
| ctest OK mas janela MessageBox | so resolveu core | rode `solutions` sw/gl |
| triangulo nao gira | dt=0 / Sleep demais | confira loop PeekMessage |

**Esperado final:** `ctest` PASS; VISUAL-01 mostra triangulo rotativo mudando de cor a cada ~1.5s.
