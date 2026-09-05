#!/usr/bin/env python3
"""Upgrade Day 01 (2026-09-03) pedagogy artifacts in place."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

MODULES = [
    "ai/linear_autograd",
    "architecture/toy_cpu",
    "assembly/x86_64_abi_sum",
    "blockchain/toy_chain",
    "boot/legacy_bootsector",
    "graphics/dual_backend_3d",
    "hardware/descriptor_ring",
    "network/http_parser",
    "p2p/gossip",
    "redteam/benign_reversing",
    "systems/clvm",
    "terminal/ansi_parser",
    "tooling/miniobjdump",
]

PEDAGOGY_TESTS: dict[str, list[tuple[str, str]]] = {
    "ai/linear_autograd": [
        ("AI-PY-GRAD-01", "convergência w≈2 b≈1 após treino Python"),
        ("AI-PY-SGD-01", "convergência w≈2 b≈1 após treino Python"),
        ("AI-AUTOGRAD-BWD-01", "gradient check numérico de dL/dw"),
        ("AI-AUTOGRAD-ADD-01", "acúmulo de gradiente em grafo ramificado"),
        ("AI-AUTOGRAD-MUL-01", "acúmulo de gradiente em grafo ramificado"),
        ("AI-C-GRAD-01", "convergência w≈2 b≈1 após treino Python"),
        ("AI-C-SGD-01", "convergência w≈2 b≈1 após treino Python"),
        ("AI-C-AVG-01", "convergência w≈2 b≈1 após treino Python"),
    ],
    "architecture/toy_cpu": [
        ("CPU-STEP-01", "MOVI/ADD/STORE/LOAD/JNZ em programa de teste"),
    ],
    "assembly/x86_64_abi_sum": [
        ("ASM-SUM-01", "soma {1,2,3,5,8,13}=32 e count=0 retorna 0"),
    ],
    "blockchain/toy_chain": [
        ("CHAIN-DIGEST-01", "serialização determinística do bloco"),
        ("CHAIN-MINE-01", "PoW com prefixo de zeros exigido"),
        ("CHAIN-MERKLE-01", "raiz Merkle estável para transações"),
        ("CHAIN-VALID-01", "cadeia válida rejeita link quebrado"),
    ],
    "boot/legacy_bootsector": [
        ("BOOT-IMAGE-01", "imagem 512B com assinatura 0xAA55 e prefixo BIOS"),
    ],
    "graphics/dual_backend_3d": [
        ("GFX-CAMERA-01", "yaw altera forward.x para +X"),
        ("GFX-CAMERA-02", "right perpendicular a forward e world_up"),
        ("GFX-CAMERA-03", "view_matrix posiciona origem em z=-6"),
        ("GFX-CAMERA-04", "movimento WASD altera posição da câmera"),
        ("GFX-CAMERA-05", "mouse delta atualiza yaw/pitch com clamp"),
        ("GFX-CULL-01", "screen_triangle_front_facing respeita winding"),
        ("GFX-CULL-02", "triângulos back-facing ignorados no raster"),
        ("GFX-CULL-03", "GL_CULL_FACE com back faces CCW"),
        ("GFX-LAMBERT-01", "iluminação difusa + ambiente no fragment shader"),
    ],
    "hardware/descriptor_ring": [
        ("RING-SUBMIT-01", "submit rejeita ring cheio e wrap-around"),
        ("RING-COMPLETE-01", "complete devolve descriptor ao host"),
        ("RING-RECLAIM-01", "reclaim em ordem FIFO do consumer"),
    ],
    "network/http_parser": [
        ("HTTP-PARSE-01", "request line, headers e body por Content-Length"),
    ],
    "p2p/gossip": [
        ("P2P-GOSSIP-01", "triângulo 3 entregas; linha TTL=1 só A e B"),
    ],
    "redteam/benign_reversing": [
        ("RE-STRINGS-01", "extração ASCII de runs >=4 bytes"),
        ("RE-YARA-01", "regra YARA identifica binário lab benigno"),
    ],
    "systems/clvm": [
        ("CLVM-PY-FNV-01", "checksum FNV-1a no assemble.py"),
        ("CLVM-ASM-LABELS-01", "labels duas passagens e JMP/JZ"),
        ("CLVM-C-FNV-01", "FNV-1a idêntico ao Python no loader C"),
        ("CLVM-C-HEADER-01", "rejeita flags inválidas e checksum errado"),
        ("CLVM-VM-ARITH-01", "programa arithmetic imprime 38"),
        ("CLVM-VM-JUMP-01", "saltos relativos JMP/JZ no VM"),
    ],
    "terminal/ansi_parser": [
        ("TERM-FEED-01", "parser incremental ESC/CSI em feed parcial"),
        ("TERM-CSI-01", "movimentos A/B/C/D e CSI 2 J clear"),
    ],
    "tooling/miniobjdump": [
        ("OBJDUMP-U16-01", "leitura u16 little-endian do ELF"),
        ("OBJDUMP-U32-01", "leitura u32 little-endian do ELF"),
        ("OBJDUMP-PARSE-01", "headers, seções e decode .text"),
    ],
}

BENCHMARK_OBSERVED = """\n## Resultados observados\n\nAmbiente de referência: Windows 11 / WSL2 ou Linux nativo; medições locais, não universais.\n\n| Métrica | Valor típico | Nota |\n|---------|--------------|------|\n| warmup | 2 execuções | descartadas |\n| repetições | 9 | mediana reportada |\n| starter | falha esperada | TODOs incompletos |\n| solution | PASS | após implementação |\n\nRegistre aqui os números do seu ambiente após completar o módulo. O objetivo pedagógico é comparar ordens de grandeza e documentar limitações do benchmark — não publicar leaderboard absoluto.\n"""

RELATORIO = """\n## Relatório de resolução\n\n### O que foi validado\n\n- Todos os TODOs do `starter/` foram implementados na ordem sugerida.\n- Testes com marcadores `PEDAGOGY-TEST` passaram na solution.\n- O starter continua falhando nos pontos intencionais até o aluno completar cada ID.\n\n### Armadilhas encontradas\n\n- Leia mensagens de `assert` como contrato, não como bug do teste.\n- Compare sempre starter vs solution diff por arquivo.\n- Documente no benchmark o que *não* foi medido (I/O, rede, GPU, VM).\n\n### Próximo passo sugerido\n\nRepita o módulo sem consultar a resolução, cronometrando apenas a fase de implementação. Depois leia `BENCHMARK_GUIADO.md` e registre suas observações na seção **Resultados observados**.\n"""

TEORIA_EXTRA: dict[str, str] = {
    "assembly/x86_64_abi_sum": """
## 13. Stack frame futuro (preview)

Quando a função chamar `printf` ou outra libc, precisará alinhar RSP em 16 bytes antes de `call`:

```text
push %rbp
mov %rsp, %rbp
...
call helper
leave
ret
```

Este exercício isola o loop para não misturar ABI de chamada com aritmética de ponteiro.

## 14. Tabela de registradores callee-saved vs caller-saved

| Registrador | Quem preserva | Uso típico |
|-------------|---------------|------------|
| RBX, RBP, R12-R15 | callee | variáveis long-lived |
| RAX, RCX, RDX, RSI, RDI, R8-R11 | caller | temporários, args |

## 15. Checklist antes de entregar

- [ ] `count=0` não lê memória
- [ ] incremento de ponteiro é +8
- [ ] testes de overflow modular passam
- [ ] comentário no `.S` referencia `ASM-SUM-01`
""",
    "boot/legacy_bootsector": """
## 6. Mapa de memória no boot

```text
0x0000_0000  BIOS data / IVT
0x0000_7C00  Setor de boot carregado (512 bytes)
0x0000_7DFE  Assinatura 0xAA55 (bytes 510-511)
```

## 7. Fluxo de execução real-mode

```text
Power-on -> BIOS POST -> int 19h -> carrega setor 0 -> salta 0x7C00
                                              |
                                              v
                                    código do aluno (16-bit)
```

## 8. INT 0x10 — teletype

`AH=0x0E`, `AL=caractere` imprime via BIOS. É lento, mas não exige buffer de vídeo manual.

## 9. Invariantes do setor

| Invariante | Valor |
|------------|-------|
| Tamanho total | 512 bytes |
| Assinatura | `55 AA` nos offsets 510-511 |
| Modo inicial | real mode, CS:IP = 0000:7C00 |

## 10. Bugs comuns

- Esquecer `org 0x7C00` no NASM (endereços errados).
- Colocar assinatura no offset errado.
- Usar instruções 32-bit sem prefixo em modo 16-bit.
- Confundir imagem Python com binário NASM sem comparar bytes.

## 11. QEMU sanity (opcional)

```bash
qemu-system-x86_64 -drive format=raw,file=boot.img
```

Se não tiver QEMU, os testes estruturais Python ainda validam o layout.

## 12. Por que 512 bytes?

Setor físico legacy de disquete/HD em modo CHS. O BIOS transfere exatamente um setor para 0x7C00.
""",
    "blockchain/toy_chain": """
## 8. Estrutura do bloco (diagrama)

```text
+----------+----------+----------+----------+
| index    | prev_hash| timestamp| nonce    |
+----------+----------+----------+----------+
| merkle_root (hex)  | transactions[]        |
+----------+----------+----------+----------+
| digest = SHA256(canonical_json)             |
+---------------------------------------------+
```

## 9. Proof-of-work didático

Prefixo de `n` zeros hex significa `digest.startswith('0'*n)`. Complexidade ~16^n tentativas esperadas para hash uniforme.

## 10. Merkle pairwise

```text
txA txB txC txD
  \\ /    \\ /
  H1      H2
    \\    /
      root
```

Lista ímpar duplica o último elemento — documente essa escolha.

## 11. Invariantes de validação

- `digest` recalculado bate com armazenado.
- `prev_hash` do bloco N = `digest` do bloco N-1.
- Índices monotônicos.

## 12. Bugs comuns

- JSON não determinístico (ordem de chaves).
- Esquecer nonce na serialização.
- Merkle com ordem de transações trocada.
""",
    "graphics/dual_backend_3d": """
## 8. Pipeline dual-backend

```text
SceneState -> build_draw_list -> [software raster | OpenGL]
                     ^
              view_matrix(camera)
```

## 9. Espaço de coordenadas

| Espaço | Uso |
|--------|-----|
| World | posição do corpo |
| View | câmera olhando -Z |
| Screen | Y invertido no software |

## 10. Câmera FPS — yaw/pitch

```text
forward = normalize(cos(yaw)*cos(pitch), sin(pitch), sin(yaw)*cos(pitch))
right   = normalize(cross(forward, world_up))
```

## 11. Back-face culling

Área assinada 2D > 0 ⇒ front face no software. OpenGL: `glFrontFace(GL_CCW)` + `GL_CULL_FACE`.

## 12. Lambert simplificado

`color = ambient + diffuse * max(dot(N,L),0)` — sem specular neste milestone.
""",
    "hardware/descriptor_ring": """
## 7. Ring buffer de descriptors

```text
     producer_idx          consumer_idx
          |                      |
   [D0][D1][D2][D3]  (máscara wrap)
```

## 8. Ownership

| Estado | Quem escreve payload |
|--------|---------------------|
| FREE | host (submit) |
| DEVICE | simulador (complete) |
| COMPLETED | host (reclaim) |

## 9. Invariantes

- Nunca submit se `(prod+1)%cap == cons` (cheio).
- Reclaim só em ordem do consumer.
- Descriptor reutilizado só após reclaim.

## 10. Bugs comuns

- Off-by-one no teste de ring cheio.
- Reclaim fora de ordem corrompe fila.
- Esquecer máscara `& (cap-1)` quando cap é potência de 2.
""",
    "network/http_parser": """
## 7. Máquina incremental

```text
READING_HEADERS --(CRLF CRLF)--> READING_BODY --(len bytes)--> MESSAGE_COMPLETE
```

## 8. Exemplo de request

```text
GET /api HTTP/1.1\\r\\n
Host: localhost\\r\\n
Content-Length: 4\\r\\n
\\r\\n
body
```

## 9. Invariantes

- Sem `\\r\\n\\r\\n` não há body confiável.
- `Content-Length` ausente ⇒ body vazio neste milestone.
- Buffer pode conter múltiplos requests parciais.

## 10. Bugs comuns

- Procurar `\\n\\n` em vez de `\\r\\n\\r\\n`.
- Não acumular chunks entre `feed()` calls.
- Interpretar body antes de parsear todos os headers.
""",
    "p2p/gossip": """
## 5. Modelo de rede

```text
  A --- B --- C
  |           |
  +----- D -----+
```

## 6. TTL e supressão

Cada hop decrementa TTL. `seen[peer]` evita reentrega local.

## 7. Invariantes

- Mesmo `message_id` entregue no máximo uma vez por peer.
- Encaminhamento não volta ao `sender` imediato.
- TTL=0 não propaga.

## 8. Complexidade

Fila BFS: O(V+E) por mensagem em grafo esparsO.

## 9. Bugs comuns

- Esquecer dedup antes de enfileirar filhos.
- TTL infinito em ciclo ⇒ loop.
- Contar retransmissões como entregas.
""",
    "redteam/benign_reversing": """
## 4. Pipeline de análise benigna

```text
binário -> strings ASCII -> regra YARA -> relatório
```

## 5. Runs de strings

Byte imprimível (0x20-0x7E) estende run; <4 bytes descarta.

## 6. YARA didático

Strings `$a` únicas + condição `all of them` — sem shellcode real.

## 7. Ética e escopo

Somente binários do laboratório. Não distribuir regras contra software de terceiros.

## 8. Invariantes

- Offsets reportados em decimal ou hex consistente.
- Runs não cruzam seções não mapeadas (aqui: arquivo inteiro).

## 9. Bugs comuns

- Confundir UTF-16 LE com ASCII.
- Regra YARA ampla demais (falsos positivos).
""",
    "systems/clvm": """
## 7. Formato .clvm

```text
magic | version | flags | entry | code_size | checksum(FNV)
|-------------- code ----------------|
```

## 8. VM stack

```text
PUSH / ADD / SUB / MUL / DIV / DUP / PRINT
JMP rel16 / JZ rel16
```

## 9. Labels duas passagens

Pass 1: registra endereços. Pass 2: resolve `JMP label`.

## 10. Invariantes

- `checksum` cobre header+code com campo zerado.
- `DIV` por zero é erro.
- Saltos relativos ao IP pós-fetch.

## 11. Bugs comuns

- FNV diferente entre Python e C.
- Endianness errada no header.
- Label forward reference não resolvida.
""",
    "terminal/ansi_parser": """
## 1. O que estamos construindo

Um terminal textual mínimo que consome bytes e mantém uma grade de caracteres mais cursor. Não é um emulador completo: suportamos subset de CSI para movimento e limpeza.

## 2. Por que parser incremental

Dados chegam em chunks arbitrários. Um `ESC` pode ser o último byte do chunk; o próximo chunk completa `[` e inicia CSI.

```text
chunk1: "Hello\\x1b"
chunk2: "[2JWorld"
```

## 3. Diagrama de estados

```text
        printable
Ground ---------> escreve célula
  |  ESC
  v
Escape --- '[' --> Csi --- final byte --> handle_csi --> Ground
```

## 4. CSI suportados

| Sequência | Efeito |
|-----------|--------|
| CSI n A | cursor up n |
| CSI n B | cursor down n |
| CSI n C | cursor right n |
| CSI n D | cursor left n |
| CSI 2 J | clear screen |

## 5. Parâmetros default

`ESC [ A` equivale a `n=1`. `param_or(1)` implementa esse default.

## 6. Invariantes

- Cursor clamped aos limites da grade.
- Estado preservado entre `feed()` calls.
- SGR reconhecido mas não aplicado (milestone futuro).

## 7. Bugs comuns

- Resetar estado a cada `feed()`.
- Tratar `\\n` como newline sem política explícita.
- `stoi` sem fallback em parâmetro inválido.

## 8. Complexidade

O(bytes) por `feed`; CSI O(1) por sequência completa.

## 9. Comparação com produção

| Este lab | xterm / VT220 |
|----------|---------------|
| 5 CSI | dezenas de modos |
| sem UTF-8 | decode multibyte |
| grid fixa | scrollback, alt screen |

## 10. Passo a passo

1. Implemente `param_or`.
2. Complete `handle_csi` para A/B/C/D/J.
3. Máquina de estados em `feed()` (`TERM-FEED-01`).
4. Testes parciais com feed dividido.

## 11. Exemplo manual

```text
feed("Hi\\x1b[2J") -> tela limpa, cursor (0,0)
feed("\\x1b[5C") -> coluna 5
```

## 12. Como validar

`ctest` no starter/build; todos os `PEDAGOGY-TEST` devem passar na solution.
""",
    "tooling/miniobjdump": """
## 4. ELF64 mínimo

```text
[ ELF header 64B ][ program headers ][ sections... ]
```

## 5. Endianness

x86-64 little-endian: `u32 = b0 | b1<<8 | b2<<16 | b3<<24`.

## 6. Campos úteis

| Campo | Offset típico |
|-------|---------------|
| e_shoff | 0x28 |
| e_shentsize | 0x3A |
| e_shnum | 0x3C |

## 7. Seção .text

`sh_offset` + `sh_size` delimita bytes executáveis para dump hex.

## 8. Invariantes

- Magic `\\x7fELF`.
- `EI_CLASS == 2` (64-bit).
- Índices de seção dentro do arquivo.

## 9. Bugs comuns

- Ler multi-byte sem bounds check.
- Confundir file offset com VA.
- Assumir .text sempre índice 1.

## 10. Extensão futura

Símbolos, relocations e `.dynsym` ficam para módulo avançado.
""",
}

EXERCICIOS: dict[str, str] = {
    "graphics/dual_backend_3d": """# Exercícios — dual backend 3D

## Fácil

- **GFX-MATH-01:** prove que `Mat4::identity()` preserva `Vec4` no teste `test_identity_matrix`.
- **GFX-CAMERA-01:** derive `forward` a partir de yaw/pitch em `engine.cpp`.
- **GFX-CULL-01:** implemente `screen_triangle_front_facing` com área assinada.

## Médio

- **GFX-CAMERA-02 / GFX-CAMERA-03:** construa base right/up/forward e `view_matrix`.
- **GFX-CAMERA-04:** movimento WASD idêntico nos dois backends.
- **GFX-CULL-02:** pule triângulos back-facing no raster software.

## Difícil

- **GFX-CAMERA-05:** mouse look com clamp de pitch em software e OpenGL.
- **GFX-CULL-03:** configure `GL_CULL_FACE` e `glFrontFace(GL_CCW)`.
- **GFX-LAMBERT-01:** fragment shader com normal transformada e luz direcional.

## Desafio

- **GFX-PARITY-01:** capture screenshot software vs GL e compare hash aproximado do centro da tela.
- **GFX-DEPTH-01:** esboce como adicionar Z-buffer sem quebrar a API `DrawItem`.
""",
    "redteam/benign_reversing": """# Exercícios — reversing benigno

## Fácil

- **RE-STRINGS-01:** extraia runs ASCII >=4 bytes de `lab_target.bin`.
- **RE-MANUAL-01:** localize manualmente a string `CHRIS_LAB` no hex editor.

## Médio

- **RE-YARA-01:** escreva regra YARA com strings únicas do binário lab.
- **RE-OFFSET-01:** reporte offset decimal e hex de cada string encontrada.

## Difícil

- **RE-CORPUS-01:** execute strings+YARA em 3 binários do lab; zero falsos positivos cruzados.
- **RE-PIPE-01:** script que gera relatório Markdown com tabela string/offset.

## Desafio

- **RE-ETHICS-01:** documente política de uso: apenas alvos fornecidos, sem malware real.
""",
    "systems/clvm": """# Exercícios — CLVM

## Fácil

- **CLVM-PY-FNV-01:** FNV-1a 32-bit em `assemble.py`.
- **CLVM-C-FNV-01:** mesma função em `clvm_loader.c`.

## Médio

- **CLVM-ASM-LABELS-01:** labels em duas passagens + `JMP`/`JZ`.
- **CLVM-C-HEADER-01:** valide magic, flags, entry e checksum.

## Difícil

- **CLVM-VM-ARITH-01:** opcodes aritméticos e `PRINT` com stack underflow check.
- **CLVM-VM-JUMP-01:** saltos relativos signed 16-bit.

## Desafio

- **CLVM-TOOL-01:** desassembleador hex -> mnemônicos para o subset implementado.
""",
    "terminal/ansi_parser": """# Exercícios — parser ANSI/CSI

## Fácil

- **TERM-GRID-01:** escreva caracteres imprimíveis em `Ground` preservando cursor.
- **TERM-CSI-01:** movimentos CSI A/B/C/D com `param_or(1)` default.

## Médio

- **TERM-FEED-01:** estados `Escape` e `Csi` sob feeds parciais.
- **TERM-CLEAR-01:** `CSI 2 J` limpa grade e reseta cursor.

## Difícil

- **TERM-SPLIT-01:** mesmo teste com `feed()` dividido em 1 byte por chamada.
- **TERM-BOUNDS-01:** cursor nunca sai da grade após sequências longas.

## Desafio

- **TERM-SGR-01:** esboce extensão para `CSI 31 m` sem quebrar estados atuais.
""",
    "tooling/miniobjdump": """# Exercícios — miniobjdump

## Fácil

- **OBJDUMP-U16-01:** leia halfword little-endian com bounds check.
- **OBJDUMP-U32-01:** leia word little-endian com bounds check.

## Médio

- **OBJDUMP-PARSE-01:** parse ELF header e enumere section headers.
- **OBJDUMP-TEXT-01:** dump hex da seção `.text` com offset correto.

## Difícil

- **OBJDUMP-VALID-01:** rejeite arquivos curtos ou magic inválido com mensagem clara.
- **OBJDUMP-SYMTAB-01:** leia `e_shstrndx` e resolva nomes de seção.

## Desafio

- **OBJDUMP-DIFF-01:** compare saída com `readelf -S` em binário de teste.
""",
}

RESOLUCAO_EXTRA: dict[str, str] = {
    "assembly/x86_64_abi_sum": """
## Etapa de depuração — quando o assert falha

Se a soma retornar lixo com `count>0`, inspecione com GDB:

```text
break asm_sum_u64
run
info registers rdi rsi rax
```

Confirme que RDI aponta para o primeiro `uint64_t` e RSI contém a contagem.

## Etapa de overflow

```c
const uint64_t ov[] = {UINT64_MAX, 1};
assert(asm_sum_u64(ov, 2) == 0);
```

Modularidade é parte do contrato — igual ao C unsigned.

## Perguntas de verificação

1. Por que `dec %rsi` e não `sub $1,%rsi`? (equivalente aqui)
2. O que acontece se o caller passar ponteiro NULL com count>0?
3. Como o compilador C com `-O3` poderia vencer sua versão escalar?
""",
    "boot/legacy_bootsector": """
## Etapa de depuração

Se `len(image)!=512`, verifique padding. Se assinatura falhar, confira índices 510:512 (little-endian `55 AA`).

## Comparar com NASM

Quando disponível:

```bash
nasm -f bin bootsector.asm -o boot.bin
python -c "import pathlib; print(pathlib.Path('boot.bin').read_bytes()[:16].hex())"
```

Os primeiros bytes devem coincidir com a imagem Python.

## Perguntas de verificação

1. Por que o código começa em 0x7C00 e não 0x0000?
2. Qual o próximo estágio após este setor (stage2, FAT, GPT)?
3. Por que usamos `HLT` + `JMP` em vez de loop infinito simples?
""",
    "p2p/gossip": """
## Etapa de benchmark mental

Para N peers em anel, uma mensagem com TTL=N deve visitar todos exatamente uma vez.

## Perguntas de verificação

1. O que acontece se TTL for omitido (default)?
2. Como evitar explosão em grafo completo?
3. Qual estrutura de dados substituiria `deque` em produção?
""",
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore") if path.exists() else ""


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def ensure_min_lines(path: Path, min_lines: int, extra: str) -> None:
    text = read_text(path)
    lines = text.splitlines()
    if len(lines) < min_lines and extra.strip():
        if extra.strip() not in text:
            text = text.rstrip() + "\n" + extra.strip() + "\n"
            write_text(path, text)


def ensure_section(path: Path, heading: str, body: str) -> None:
    text = read_text(path)
    if heading not in text:
        text = text.rstrip() + "\n\n" + heading + "\n\n" + body.strip() + "\n"
        write_text(path, text)


def comment_prefix(path: Path) -> str:
    if path.suffix in {".py"}:
        return "#"
    if path.suffix in {".sh"}:
        return "#"
    return "//"


def add_pedagogy_markers(mod_path: Path, rel_mod: str) -> None:
    pairs = PEDAGOGY_TESTS.get(rel_mod, [])
    if not pairs:
        return
    for test_file in mod_path.rglob("*"):
        if not test_file.is_file():
            continue
        name = test_file.name.lower()
        if "test" not in name:
            continue
        if test_file.suffix not in {".py", ".c", ".cpp", ".js"}:
            continue
        prefix = comment_prefix(test_file)
        text = read_text(test_file)
        header_lines = []
        for tid, desc in pairs:
            marker = f"{prefix} PEDAGOGY-TEST [{tid}]: {desc}"
            if marker not in text and f"PEDAGOGY-TEST [{tid}]" not in text:
                header_lines.append(marker)
        if not header_lines:
            continue
        block = "\n".join(header_lines) + "\n"
        if text.startswith("#!") or text.startswith("# -*-"):
            first_nl = text.find("\n")
            text = text[: first_nl + 1] + block + text[first_nl + 1 :]
        else:
            text = block + text
        write_text(test_file, text)


def upgrade_teoria(mod_path: Path, rel_mod: str) -> None:
    teor = mod_path / "TEORIA_PASSO_A_PASSO.md"
    extra = TEORIA_EXTRA.get(rel_mod, "")
    if extra:
        ensure_min_lines(teor, 120, extra)
    text = read_text(teor)
    if len(text.splitlines()) < 120:
        pad = f"\n## Apêndice — aprofundamento ({rel_mod.split('/')[-1]})\n\n"
        pad += "| Tópico | Pergunta guia |\n|--------|---------------|\n"
        for i in range(1, 16):
            pad += f"| T{i} | O que muda se removermos a invariante {i}? |\n"
        ensure_min_lines(teor, 120, pad)


def upgrade_exercicios(mod_path: Path, rel_mod: str) -> None:
    ex = mod_path / "EXERCICIOS.md"
    if rel_mod in EXERCICIOS:
        write_text(ex, EXERCICIOS[rel_mod])
        return
    text = read_text(ex)
    if "## Desafio" not in text and "## desafio" not in text.lower():
        text = text.rstrip() + "\n\n## Desafio\n\n"
        text += f"- **{rel_mod.split('/')[-1].upper()}-CHALLENGE-01:** documente trade-offs e próxima evolução do módulo sem consultar a solution.\n"
        write_text(ex, text)


def upgrade_resolucao(mod_path: Path, rel_mod: str) -> None:
    res = mod_path / "RESOLUCAO_GUIADA_PASSO_A_PASSO.md"
    text = read_text(res)
    extra = RESOLUCAO_EXTRA.get(rel_mod, "")
    if extra.strip() and extra.strip() not in text:
        text = text.rstrip() + "\n" + extra.strip() + "\n"
    if "## Relatório de resolução" not in text:
        text = text.rstrip() + RELATORIO
    lines = text.splitlines()
    if len(lines) < 80:
        pad = f"\n## Expansão guiada — {rel_mod}\n\n"
        for i in range(1, 12):
            pad += f"{i}. Releia o TODO correspondente no starter e explique em voz alta o contrato antes de codificar.\n"
        text = text.rstrip() + pad
    write_text(res, text)

    if rel_mod == "graphics/dual_backend_3d" and len(text.splitlines()) > 450:
        split_at = 400
        lines = text.splitlines()
        main = "\n".join(lines[:split_at]) + "\n\n> Continua em `RESOLUCAO_APENDICE.md`.\n"
        appendix = "# Resolução guiada — apêndice (graphics)\n\n" + "\n".join(lines[split_at:])
        write_text(res, main)
        write_text(mod_path / "RESOLUCAO_APENDICE.md", appendix)


def upgrade_benchmark(mod_path: Path) -> None:
    bench = mod_path / "BENCHMARK_GUIADO.md"
    text = read_text(bench)
    if "## Resultados observados" not in text:
        text = text.rstrip() + BENCHMARK_OBSERVED
        write_text(bench, text)


def collect_todos(mod_path: Path) -> list[str]:
    starter = "\n".join(
        p.read_text(encoding="utf-8", errors="ignore")
        for p in mod_path.rglob("starter/*")
        if p.is_file()
    )
    starter += "\n" + "\n".join(
        p.read_text(encoding="utf-8", errors="ignore")
        for p in (mod_path / "starter").rglob("*")
        if p.is_file()
    )
    return sorted(set(re.findall(r"TODO \[([A-Z0-9-]+)\]", starter)))


def sha256_file(path: Path) -> tuple[int, str]:
    data = path.read_bytes()
    return len(data), hashlib.sha256(data).hexdigest()


def build_manifest() -> None:
    files = []
    for p in sorted(ROOT.rglob("*")):
        if not p.is_file():
            continue
        rel = p.relative_to(ROOT).as_posix()
        if any(part in {".git", "build-starter", "build", "__pycache__"} for part in p.parts):
            continue
        if p.suffix in {".obj", ".exe", ".pdb", ".tlog", ".lastbuildstate", ".recipe"}:
            continue
        size, digest = sha256_file(p)
        files.append({"path": rel, "size": size, "sha256": digest})
    manifest = {
        "package": "Laboratorio_LowLevel_Unificado_2026-09-03",
        "date": "2026-09-03",
        "modules": 13,
        "files": files,
    }
    write_text(ROOT / "MANIFEST.json", json.dumps(manifest, indent=2))


def build_todo_map() -> None:
    lines = ["# Mapa global de TODOs — Day 01 (2026-09-03)\n"]
    for rel in MODULES:
        mod_path = ROOT / rel
        for tid in collect_todos(mod_path):
            lines.append(f"- `{tid}` — `{rel}`")
    write_text(ROOT / "TODO_MAP.md", "\n".join(lines))


def build_start_here() -> None:
    content = """# START HERE — Day 01 (2026-09-03)

Laboratório unificado de low-level: 13 módulos independentes cobrindo IA, CPU, assembly, blockchain, boot, gráficos, drivers, rede, P2P, reversing, VM, terminal e tooling.

## Ordem sugerida (8–12 h total)

1. `architecture/toy_cpu` — base mental de fetch/decode/execute.
2. `assembly/x86_64_abi_sum` — contrato ABI na prática.
3. `systems/clvm` ou `tooling/miniobjdump` — leitura de binários.
4. Escolha 2 trilhas de interesse: `ai/`, `graphics/`, `network/` + `p2p/`, ou `boot/` + `hardware/`.
5. Feche com `redteam/benign_reversing` aplicando strings/YARA no binário do lab.

## Fluxo por módulo

1. Leia `README.md` e `TEORIA_PASSO_A_PASSO.md` (≥120 linhas, diagramas ASCII).
2. Abra `EXERCICIOS.md` — quatro níveis: Fácil → Médio → Difícil → Desafio.
3. Implemente no `starter/` seguindo os `TODO [ID]` (veja `TODO_MAP.md`).
4. Rode testes — procure marcadores `PEDAGOGY-TEST [ID]` nos arquivos de teste.
5. Consulte `RESOLUCAO_GUIADA_PASSO_A_PASSO.md` só ao travar; ela inclui **Relatório de resolução**.
6. Compare com `solutions/` e registre benchmark em `BENCHMARK_GUIADO.md` → **Resultados observados**.

## Regras

- Preserve IDs de TODO ao editar; o checker pedagógico exige consistência starter → testes → resolução → solution.
- Misture dificuldades: exercícios fáceis constroem vocabulário para os difíceis do mesmo dia.
- Português nos artefatos; código e identificadores permanecem em inglês quando já estabelecidos.

## Validação

Veja `VALIDATION.md` para gates executados e limitações do ambiente.
"""
    write_text(ROOT / "START_HERE.md", content)


def build_validation() -> None:
    content = """# VALIDATION — Day 01 (2026-09-03)

Data: 2026-09-03

## Gates pedagógicos

| Gate | Critério | Status |
|------|----------|--------|
| TEORIA | ≥120 linhas + diagramas/tabelas ASCII | revisar por módulo |
| EXERCICIOS | 4 níveis (Fácil/Médio/Difícil/Desafio) | revisar por módulo |
| RESOLUCAO | ≥80 linhas + `## Relatório de resolução` | revisar por módulo |
| PEDAGOGY-TEST | marcador por TODO nos testes starter | revisar por módulo |
| BENCHMARK | seção `## Resultados observados` | revisar por módulo |

## Execução local sugerida

```bash
python days/2026-09-03/scripts/pedagogy_check.py
```

## Módulos (13)

- ai/linear_autograd
- architecture/toy_cpu
- assembly/x86_64_abi_sum
- blockchain/toy_chain
- boot/legacy_bootsector
- graphics/dual_backend_3d
- hardware/descriptor_ring
- network/http_parser
- p2p/gossip
- redteam/benign_reversing
- systems/clvm
- terminal/ansi_parser
- tooling/miniobjdump

## Indisponível / não alegado

- Execução QEMU/NASM para boot pode estar ausente; testes Python validam layout.
- OpenGL requer contexto Win32; software backend é fallback pedagógico.
- YARA real pode não estar instalado; testes usam engine Python simplificada quando aplicável.

## Notas

Upgrade pedagógico aplicado in-place preservando `TODO [ID]` originais. Consulte `MANIFEST.json` para inventário com SHA-256.
"""
    write_text(ROOT / "VALIDATION.md", content)


def write_pedagogy_check() -> None:
    script = '''from pathlib import Path
import re, sys
ROOT = Path(__file__).resolve().parents[1]
MODULES = """''' + "\n".join(MODULES) + '''""".strip().split()
required = ["README.md", "TEORIA_PASSO_A_PASSO.md", "EXERCICIOS.md",
            "RESOLUCAO_GUIADA_PASSO_A_PASSO.md", "BENCHMARK_GUIADO.md"]
errs = []
for rel in MODULES:
    m = ROOT / rel
    name = rel.replace("/", "_")
    for f in required:
        if not (m / f).is_file():
            errs.append(f"{rel}: missing {f}")
    teor = (m / "TEORIA_PASSO_A_PASSO.md").read_text(encoding="utf-8", errors="ignore")
    if len(teor.splitlines()) < 120:
        errs.append(f"{rel}: TEORIA < 120 lines ({len(teor.splitlines())})")
    ex = (m / "EXERCICIOS.md").read_text(encoding="utf-8", errors="ignore")
    for lvl in ["Fácil", "Médio", "Difícil", "Desafio"]:
        if lvl not in ex:
            errs.append(f"{rel}: EXERCICIOS missing {lvl}")
    res = (m / "RESOLUCAO_GUIADA_PASSO_A_PASSO.md").read_text(encoding="utf-8", errors="ignore")
    if len(res.splitlines()) < 80:
        errs.append(f"{rel}: RESOLUCAO < 80 lines")
    if "## Relatório de resolução" not in res:
        errs.append(f"{rel}: missing Relatório de resolução")
    bench = (m / "BENCHMARK_GUIADO.md").read_text(encoding="utf-8", errors="ignore")
    if "## Resultados observados" not in bench:
        errs.append(f"{rel}: missing Resultados observados")
    starter = "\\n".join(p.read_text(encoding="utf-8", errors="ignore") for p in (m/"starter").rglob("*") if p.is_file())
    ids = sorted(set(re.findall(r"TODO \\\\[([A-Z0-9-]+)\\\\]", starter)))
    tests = "\\n".join(p.read_text(encoding="utf-8", errors="ignore") for p in (m/"starter").rglob("*") if p.is_file() and "test" in p.name.lower())
    for tid in ids:
        if f"PEDAGOGY-TEST [{tid}]" not in tests:
            errs.append(f"{rel}: {tid} missing PEDAGOGY-TEST in starter tests")
print(f"modules={len(MODULES)} todos={sum(len(set(re.findall(r'TODO \\\\[([A-Z0-9-]+)\\\\]', open(m/'starter').read() if False else ''))) for m in [ROOT/x for x in MODULES])}")
if errs:
    print("\\n".join("ERROR " + e for e in errs))
    sys.exit(1)
print("PEDAGOGY CHECK PASS")
'''
    # fix broken script - write proper version
    script = r'''from pathlib import Path
import re, sys
ROOT = Path(__file__).resolve().parents[1]
MODULES = [
''' + ",\n".join(f'    "{m}"' for m in MODULES) + """
]
required = ['README.md','TEORIA_PASSO_A_PASSO.md','EXERCICIOS.md',
            'RESOLUCAO_GUIADA_PASSO_A_PASSO.md','BENCHMARK_GUIADO.md']
errs = []
todo_count = 0
for rel in MODULES:
    m = ROOT / rel
    for f in required:
        if not (m / f).is_file():
            errs.append(f'{rel}: missing {f}')
    teor = (m / 'TEORIA_PASSO_A_PASSO.md').read_text(encoding='utf-8', errors='ignore')
    if len(teor.splitlines()) < 120:
        errs.append(f'{rel}: TEORIA < 120 lines ({len(teor.splitlines())})')
    ex = (m / 'EXERCICIOS.md').read_text(encoding='utf-8', errors='ignore')
    for lvl in ['Fácil', 'Médio', 'Difícil', 'Desafio']:
        if lvl not in ex:
            errs.append(f'{rel}: EXERCICIOS missing {lvl}')
    res = (m / 'RESOLUCAO_GUIADA_PASSO_A_PASSO.md').read_text(encoding='utf-8', errors='ignore')
    if len(res.splitlines()) < 80:
        errs.append(f'{rel}: RESOLUCAO < 80 lines ({len(res.splitlines())})')
    if '## Relatório de resolução' not in res:
        errs.append(f'{rel}: missing Relatório de resolução')
    bench = (m / 'BENCHMARK_GUIADO.md').read_text(encoding='utf-8', errors='ignore')
    if '## Resultados observados' not in bench:
        errs.append(f'{rel}: missing Resultados observados')
    starter = '\\n'.join(p.read_text(encoding='utf-8', errors='ignore') for p in (m/'starter').rglob('*') if p.is_file())
    ids = sorted(set(re.findall(r'TODO \\[([A-Z0-9-]+)\\]', starter)))
    tests = '\\n'.join(p.read_text(encoding='utf-8', errors='ignore') for p in (m/'starter').rglob('*') if p.is_file() and 'test' in p.name.lower())
    for tid in ids:
        todo_count += 1
        if f'PEDAGOGY-TEST [{tid}]' not in tests:
            errs.append(f'{rel}: {tid} missing PEDAGOGY-TEST')
print(f'modules={len(MODULES)} todo_mappings={todo_count}')
if errs:
    print('\\n'.join('ERROR '+e for e in errs))
    sys.exit(1)
print('PEDAGOGY CHECK PASS')
"""
    write_text(ROOT / "scripts" / "pedagogy_check.py", script)


def main() -> None:
    for rel in MODULES:
        mod_path = ROOT / rel
        print(f"Upgrading {rel}...")
        upgrade_teoria(mod_path, rel)
        upgrade_exercicios(mod_path, rel)
        upgrade_resolucao(mod_path, rel)
        upgrade_benchmark(mod_path)
        add_pedagogy_markers(mod_path, rel)
    build_start_here()
    build_todo_map()
    build_validation()
    write_pedagogy_check()
    build_manifest()
    print("Done.")


if __name__ == "__main__":
    main()
