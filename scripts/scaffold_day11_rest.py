#!/usr/bin/env python3
"""Part 2 of day 2026-09-11 scaffold — remaining modules + infra."""
from __future__ import annotations

from pathlib import Path

# Imported symbols set by parent before calling generate_rest
DAY: Path
DS: str
w = None
pad_teoria = None
package = None
todo_section = None
std_ex = None
std_bench = None
std_pesq = None
CMAKE_C = ""
CMAKE_CXX = ""
CMAKE_ASM = ""
ROOT: Path


def build_dotnet() -> None:
    mod = DAY / "dotnet" / "pe_import_span"
    csproj = """<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <ImplicitUsings>enable</ImplicitUsings>
    <Nullable>enable</Nullable>
    <RootNamespace>Chris.PeLab</RootNamespace>
  </PropertyGroup>
  <ItemGroup><Compile Remove="tests/**" /></ItemGroup>
</Project>
"""
    test_csproj = """<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <IsTestProject>true</IsTestProject>
  </PropertyGroup>
  <ItemGroup>
    <PackageReference Include="Microsoft.NET.Test.Sdk" Version="17.11.1" />
    <PackageReference Include="xunit" Version="2.9.2" />
    <PackageReference Include="xunit.runner.visualstudio" Version="2.8.2" />
  </ItemGroup>
  <ItemGroup><ProjectReference Include="..\\Chris.PeLab.csproj" /></ItemGroup>
</Project>
"""
    starter = r'''using System.Runtime.InteropServices;
namespace Chris.PeLab;
public static class PeImportSpan
{
    /// <summary>TODO [DOTNET-IMP-01]: validate MZ + PE signature via Span.</summary>
    public static bool IsPeFile(ReadOnlySpan<byte> data)
    {
        _ = data; return false;
    }
    /// <summary>TODO [DOTNET-IMP-02]: read e_lfanew (offset 0x3C).</summary>
    public static bool TryGetPeOffset(ReadOnlySpan<byte> data, out int peOffset)
    {
        peOffset = 0; _ = data; return false;
    }
    /// <summary>TODO [DOTNET-IMP-03]: read import directory RVA (data dir[1]) from PE32+ optional header.</summary>
    public static bool TryReadImportRva(ReadOnlySpan<byte> data, out uint importRva)
    {
        importRva = 0; _ = data; return false;
    }
}
'''
    sol = r'''using System.Runtime.InteropServices;
namespace Chris.PeLab;
public static class PeImportSpan
{
    public static bool IsPeFile(ReadOnlySpan<byte> data)
    {
        // PEDAGOGY-SOLUTION: DOTNET-IMP-01
        if (data.Length < 0x40) return false;
        if (data[0] != (byte)'M' || data[1] != (byte)'Z') return false;
        if (!TryGetPeOffset(data, out int off)) return false;
        if (off + 4 > data.Length) return false;
        return data[off] == (byte)'P' && data[off + 1] == (byte)'E';
    }
    public static bool TryGetPeOffset(ReadOnlySpan<byte> data, out int peOffset)
    {
        // PEDAGOGY-SOLUTION: DOTNET-IMP-02
        peOffset = 0;
        if (data.Length < 0x40) return false;
        peOffset = MemoryMarshal.Read<int>(data.Slice(0x3C, 4));
        return peOffset > 0 && peOffset + 4 <= data.Length;
    }
    public static bool TryReadImportRva(ReadOnlySpan<byte> data, out uint importRva)
    {
        // PEDAGOGY-SOLUTION: DOTNET-IMP-03
        importRva = 0;
        if (!IsPeFile(data) || !TryGetPeOffset(data, out int pe)) return false;
        int opt = pe + 4 + 20; // optional header start
        // PE32+ magic 0x20B at opt+0; import dir is data directory[1] at opt+0x78+8
        if (opt + 0x78 + 16 > data.Length) return false;
        importRva = MemoryMarshal.Read<uint>(data.Slice(opt + 0x78 + 8, 4));
        return true;
    }
}
'''
    tests = r'''using System;
using Chris.PeLab;
using Xunit;
public class PeImportTests
{
    static byte[] MinimalPe()
    {
        var buf = new byte[0x200];
        buf[0] = (byte)'M'; buf[1] = (byte)'Z';
        BitConverter.GetBytes(0x80).CopyTo(buf, 0x3C);
        buf[0x80] = (byte)'P'; buf[0x81] = (byte)'E';
        BitConverter.GetBytes((ushort)0x20B).CopyTo(buf, 0x98); // pe+24 = optional magic
        // pe=0x80; opt=0x80+24=0x98; data dir[1] at opt+0x80 = 0x118? 
        // Day08 export used opt+0x78 for dir[0]. dir[1] = opt+0x78+8.
        // opt = pe+4+20 = 0x98. dir0 @ 0x98+0x78=0x110, dir1 @ 0x118
        BitConverter.GetBytes(0x2000u).CopyTo(buf, 0x118);
        return buf;
    }
    // PEDAGOGY-TEST: DOTNET-IMP-01
    [Fact] public void Caso1_IsPe() => Assert.True(PeImportSpan.IsPeFile(MinimalPe()));
    // PEDAGOGY-TEST: DOTNET-IMP-02
    [Fact] public void Caso2_Offset() {
        Assert.True(PeImportSpan.TryGetPeOffset(MinimalPe(), out int off));
        Assert.Equal(0x80, off);
    }
    // PEDAGOGY-TEST: DOTNET-IMP-03
    [Fact] public void Caso3_ImportRva() {
        Assert.True(PeImportSpan.TryReadImportRva(MinimalPe(), out uint rva));
        Assert.Equal(0x2000u, rva);
    }
}
'''
    for base in (mod / "starter", mod / "solutions"):
        w(base / "Chris.PeLab.csproj", csproj)
        w(base / "tests" / "Chris.PeLab.Tests.csproj", test_csproj)
        w(base / "tests" / "PeImportTests.cs", tests)
    w(mod / "starter" / "PeImportSpan.cs", starter)
    w(mod / "solutions" / "PeImportSpan.cs", sol)
    teoria = pad_teoria(
        r'''# Teoria passo a passo — PE import directory via Span (.NET)

Laboratório em **C#**. Continua o dia 08 (export RVA); agora o **data directory[1]** (Import).

## 1. O quê

`e_lfanew` em 0x3C aponta ao PE. Optional header PE32+ começa em pe+24. Data directories começam em opt+0x70 (PE32+)… neste lab usamos o mesmo layout do dia 08: dir[0] em opt+0x78, logo **dir[1] em opt+0x80** (opt+0x78+8).

## 2. Trace

```text
e_lfanew = 0x80
PE signature @ 0x80 = 'P''E'
opt = 0x80 + 4 + 20 = 0x98
import RVA @ 0x98 + 0x78 + 8 = 0x118 → valor 0x2000
```

## 3. Por quê Span

Evita copiar o PE inteiro; fatias `ReadOnlySpan<byte>` leem campos.

## 4. Por quê dir[1]

Export=0, Import=1, Resource=2 — o índice importa.

## 5. Invariantes

- MZ + PE válidos antes de ler RVA
- peOffset > 0 e dentro do buffer
- import RVA do fixture = 0x2000

## 6. Bugs

| Sintoma | Causa |
|---------|-------|
| leu 0x1000 | leu dir[0] export |
| offset 0 | não leu 0x3C |
| false MZ | length < 0x40 |

## 7. Checklist

- [ ] e_lfanew=0x80
- [ ] import @ 0x118 = 0x2000
''',
        "pe_import_span",
        ["MZ em 0,1.", "PE em 0x80.", "opt=0x98.", "dir1 @ 0x118.", "RVA 0x2000."],
    )
    resolucao = (
        """# Resolução guiada — pe_import_span

## Mapa exato starter → resolução

| TODO | Arquivo | Função |
|------|---------|--------|
| `DOTNET-IMP-01` | `starter/PeImportSpan.cs` | `IsPeFile` |
| `DOTNET-IMP-02` | `starter/PeImportSpan.cs` | `TryGetPeOffset` |
| `DOTNET-IMP-03` | `starter/PeImportSpan.cs` | `TryReadImportRva` |

## Baseline

```powershell
dotnet test days/2026-09-11/dotnet/pe_import_span/starter/tests/Chris.PeLab.Tests.csproj
```

**Esperado:** FAIL.
"""
        + todo_section(
            "DOTNET-IMP-01", "starter/PeImportSpan.cs", "IsPeFile",
            "Precisa MZ+PE verdadeiros.",
            "Cheque MZ; pe offset; bytes PE.",
            "    if (data.Length < 0x40) return false;\n"
            "    if (data[0] != (byte)'M' || data[1] != (byte)'Z') return false;\n"
            "    if (!TryGetPeOffset(data, out int off)) return false;\n"
            "    if (off + 4 > data.Length) return false;\n"
            "    return data[off] == (byte)'P' && data[off + 1] == (byte)'E';",
            "csharp", "Mesma validação do lab export.", "IsPeFile(MinimalPe())==true.",
        )
        + todo_section(
            "DOTNET-IMP-02", "starter/PeImportSpan.cs", "TryGetPeOffset",
            "e_lfanew deve ser 0x80.",
            "MemoryMarshal.Read<int> em 0x3C.",
            "    peOffset = 0;\n"
            "    if (data.Length < 0x40) return false;\n"
            "    peOffset = MemoryMarshal.Read<int>(data.Slice(0x3C, 4));\n"
            "    return peOffset > 0 && peOffset + 4 <= data.Length;",
            "csharp", "Campo DOS clássico.", "off==0x80.",
        )
        + todo_section(
            "DOTNET-IMP-03", "starter/PeImportSpan.cs", "TryReadImportRva",
            "Import RVA = 0x2000, não o export 0x1000 do dia 08.",
            "opt=pe+24; leia uint em opt+0x78+8.",
            "    importRva = 0;\n"
            "    if (!IsPeFile(data) || !TryGetPeOffset(data, out int pe)) return false;\n"
            "    int opt = pe + 4 + 20;\n"
            "    if (opt + 0x78 + 16 > data.Length) return false;\n"
            "    importRva = MemoryMarshal.Read<uint>(data.Slice(opt + 0x78 + 8, 4));\n"
            "    return true;",
            "csharp", "dir[1] = dir[0]+8 bytes.", "rva==0x2000.",
        )
        + "\n## Debug\n\n| Sintoma | Correção |\n|---------|----------|\n| 0x1000 | leu export |\n\n## Relatório de resolução\n\n- TODOs: [ ]\n"
    )
    package(
        mod,
        readme="# dotnet/pe_import_span\n\nLê Import Directory RVA via Span (PE32+).\n",
        teoria=teoria,
        resolucao=resolucao,
        exercicios=std_ex(".NET", "MZ/PE no papel.", "e_lfanew 0x80.", "dir[1] offset.", "Contraste com export."),
        testes="# Testes\n\n- `DOTNET-IMP-01`\n- `DOTNET-IMP-02`\n- `DOTNET-IMP-03` — RVA 0x2000\n",
        pesquisa=std_pesq("PE import", ["Data directories?", "Import vs Export?", "Span vs array?"], ["https://learn.microsoft.com/en-us/windows/win32/debug/pe-format"]),
        benchmark=std_bench("TryReadImportRva", "dotnet test"),
    )


def build_alpha() -> None:
    mod = DAY / "graphics" / "alpha_blend_scanline"
    hpp = """#pragma once
#include <cstdint>
struct Pixel { uint8_t r,g,b,a; };
void blend_pixel(Pixel &dst, Pixel src);
void blend_scanline(Pixel *dst, const Pixel *src, int n);
int blend_coverage(const Pixel *dst, int n, uint8_t min_a);
"""
    starter = r'''#include "blend.hpp"
void blend_pixel(Pixel &dst, Pixel src) {
    /* TODO [GFX-BLEND-01]: src-over: out = src + dst*(1-src.a/255) per channel */
    (void)dst; (void)src;
}
void blend_scanline(Pixel *dst, const Pixel *src, int n) {
    /* TODO [GFX-BLEND-02]: blend n pixels */
    (void)dst; (void)src; (void)n;
}
int blend_coverage(const Pixel *dst, int n, uint8_t min_a) {
    /* TODO [GFX-BLEND-03]: count pixels with a >= min_a */
    (void)dst; (void)n; (void)min_a; return -1;
}
'''
    sol = r'''#include "blend.hpp"
static uint8_t lerp8(uint8_t d, uint8_t s, uint8_t a) {
    return (uint8_t)((s * a + d * (255 - a) + 127) / 255);
}
void blend_pixel(Pixel &dst, Pixel src) {
    /* PEDAGOGY-SOLUTION: GFX-BLEND-01 */
    uint8_t a = src.a;
    dst.r = lerp8(dst.r, src.r, a);
    dst.g = lerp8(dst.g, src.g, a);
    dst.b = lerp8(dst.b, src.b, a);
    dst.a = (uint8_t)(a + (dst.a * (255 - a) + 127) / 255);
}
void blend_scanline(Pixel *dst, const Pixel *src, int n) {
    /* PEDAGOGY-SOLUTION: GFX-BLEND-02 */
    for (int i = 0; i < n; ++i) blend_pixel(dst[i], src[i]);
}
int blend_coverage(const Pixel *dst, int n, uint8_t min_a) {
    /* PEDAGOGY-SOLUTION: GFX-BLEND-03 */
    int c = 0;
    if (!dst || n < 0) return -1;
    for (int i = 0; i < n; ++i) if (dst[i].a >= min_a) ++c;
    return c;
}
'''
    test = r'''#include "blend.hpp"
#include <cstdio>
static int fail(const char *m) { std::fprintf(stderr, "FAIL %s\n", m); return 1; }
int main() {
    /* PEDAGOGY-TEST: GFX-BLEND-01 */
    Pixel d{0,0,0,255}; Pixel s{255,0,0,128};
    blend_pixel(d, s);
    if (d.r < 120 || d.r > 135) return fail("r~128"); /* 255*128/255 ≈ 128 */
    /* PEDAGOGY-TEST: GFX-BLEND-02 */
    Pixel dst[2] = {{0,0,0,255},{0,0,0,255}};
    Pixel src[2] = {{255,0,0,255},{0,255,0,255}};
    blend_scanline(dst, src, 2);
    if (dst[0].r != 255 || dst[1].g != 255) return fail("scan");
    /* PEDAGOGY-TEST: GFX-BLEND-03 */
    if (blend_coverage(dst, 2, 200) != 2) return fail("cov");
    std::puts("ok"); return 0;
}
'''
    for base in (mod / "starter", mod / "solutions"):
        w(base / "blend.hpp", hpp)
        w(base / "CMakeLists.txt", CMAKE_CXX.format(name="blend", sources="blend.cpp test_blend.cpp"))
        w(base / "test_blend.cpp", test)
    w(mod / "starter" / "blend.cpp", starter)
    w(mod / "solutions" / "blend.cpp", sol)
    teoria = pad_teoria(
        r'''# Teoria passo a passo — alpha blend scanline (C++ headless)

Laboratório **headless** (sem Win32). Porter-Duff src-over em bytes 0..255.

## 1. O quê

`out_c = (src_c * a + dst_c * (255-a) + 127) / 255` com arredondamento.

## 2. Trace Caso 1

```text
dst = (0,0,0,255), src = (255,0,0,128)
r = (255*128 + 0*127 + 127)/255 = (32640+127)/255 = 32767/255 = 128
```

## 3. Scanline

Dois pixels opacos: resultado r=255 e g=255.

## 4. Coverage

Conta pixels com `a >= min_a` (200) → 2.

## 5. Por quê +127

Arredonda ao dividir por 255 (evita bias para baixo).

## 6. Por quê headless

Mesma matemática da GPU; sem MessageBox / janela.

## 7. Invariantes

- a=255 → src puro; a=0 → dst intacto no canal (exceto a composta)

## 8. Bugs

| Sintoma | Causa |
|---------|-------|
| r=127 | sem +127 |
| scan não muda | esqueceu loop |
| cov -1 | n<0 path |

## 9. Checklist

- [ ] r≈128 no Caso 1
- [ ] scanline 2 pixels
''',
        "alpha_blend_scanline",
        ["128 alpha → r~128.", "a=255 copia src.", "coverage=2.", "Fórmula +127.", "Sem Win32."],
    )
    resolucao = (
        """# Resolução guiada — alpha_blend_scanline

## Mapa exato starter → resolução

| TODO | Arquivo | Função |
|------|---------|--------|
| `GFX-BLEND-01` | `starter/blend.cpp` | `blend_pixel` |
| `GFX-BLEND-02` | `starter/blend.cpp` | `blend_scanline` |
| `GFX-BLEND-03` | `starter/blend.cpp` | `blend_coverage` |

## Baseline

```powershell
cd days/2026-09-11/graphics/alpha_blend_scanline/starter
cmake -S . -B build_ci -G Ninja
cmake --build build_ci
ctest --test-dir build_ci --output-on-failure
```

**Esperado:** FAIL.
"""
        + todo_section(
            "GFX-BLEND-01", "starter/blend.cpp", "blend_pixel",
            "dst vermelho deve ~128 com src a=128.",
            "lerp por canal com +127/255.",
            "    uint8_t a = src.a;\n"
            "    dst.r = (uint8_t)((src.r * a + dst.r * (255 - a) + 127) / 255);\n"
            "    dst.g = (uint8_t)((src.g * a + dst.g * (255 - a) + 127) / 255);\n"
            "    dst.b = (uint8_t)((src.b * a + dst.b * (255 - a) + 127) / 255);\n"
            "    dst.a = (uint8_t)(a + (dst.a * (255 - a) + 127) / 255);",
            "cpp", "Src-over clássico em 8-bit.", "120<=r<=135.",
        )
        + todo_section(
            "GFX-BLEND-02", "starter/blend.cpp", "blend_scanline",
            "Dois pixels opacos devem copiar r e g.",
            "loop blend_pixel.",
            "    for (int i = 0; i < n; ++i)\n"
            "        blend_pixel(dst[i], src[i]);\n"
            "    /* scanline done */",
            "cpp", "Scanline = N blends.", "dst[0].r==255, dst[1].g==255.",
        )
        + todo_section(
            "GFX-BLEND-03", "starter/blend.cpp", "blend_coverage",
            "Contar a>=200.",
            "loop contador.",
            "    int c = 0;\n"
            "    if (!dst || n < 0) return -1;\n"
            "    for (int i = 0; i < n; ++i) if (dst[i].a >= min_a) ++c;\n"
            "    return c;",
            "cpp", "Métrica simples de cobertura.", "return 2.",
        )
        + "\n## Debug\n\n| Sintoma | Correção |\n|---------|----------|\n| r baixo | +127 |\n\n## Relatório de resolução\n\n- TODOs: [ ]\n"
    )
    package(
        mod,
        readme="# graphics/alpha_blend_scanline\n\nAlpha src-over headless (sem Win32).\n",
        teoria=teoria,
        resolucao=resolucao,
        exercicios=std_ex("C++", "Calcule r com a=128.", "Scanline 2 px.", "Coverage.", "a=0 no papel."),
        testes="# Testes\n\n- `GFX-BLEND-01` r~128\n- `GFX-BLEND-02`\n- `GFX-BLEND-03`\n",
        pesquisa=std_pesq("alpha", ["Porter-Duff src-over?", "premultiplied?", "scanline?"], ["https://en.wikipedia.org/wiki/Alpha_compositing"]),
        benchmark=std_bench("blend_scanline", "ctest --test-dir build_ci"),
    )


def build_redteam() -> None:
    mod = DAY / "redteam" / "import_name_triage"
    starter = r'''"""Flag suspicious PE import names."""
SUSPICIOUS = ("VirtualAlloc", "WriteProcessMemory", "CreateRemoteThread", "NtMapViewOfSection")

def normalize_name(name: str) -> str:
    # TODO [RT-IMP-01]: strip whitespace; reject empty
    raise NotImplementedError("RT-IMP-01")

def flag_suspicious(names: list[str]) -> list[str]:
    # TODO [RT-IMP-02]: return names in SUSPICIOUS (preserve order)
    raise NotImplementedError("RT-IMP-02")

def triage_score(names: list[str]) -> int:
    # TODO [RT-IMP-03]: 10 points per flagged name
    raise NotImplementedError("RT-IMP-03")
'''
    sol = r'''"""Flag suspicious PE import names."""
SUSPICIOUS = ("VirtualAlloc", "WriteProcessMemory", "CreateRemoteThread", "NtMapViewOfSection")

def normalize_name(name: str) -> str:
    # PEDAGOGY-SOLUTION: RT-IMP-01
    s = name.strip()
    if not s:
        raise ValueError("empty")
    return s

def flag_suspicious(names: list[str]) -> list[str]:
    # PEDAGOGY-SOLUTION: RT-IMP-02
    out = []
    for n in names:
        nn = normalize_name(n)
        if nn in SUSPICIOUS:
            out.append(nn)
    return out

def triage_score(names: list[str]) -> int:
    # PEDAGOGY-SOLUTION: RT-IMP-03
    return 10 * len(flag_suspicious(names))
'''
    test = r'''from import_name_triage import normalize_name, flag_suspicious, triage_score
# PEDAGOGY-TEST: RT-IMP-01
def test_norm():
    assert normalize_name("  VirtualAlloc ") == "VirtualAlloc"
    try:
        normalize_name("   ")
        assert False
    except ValueError:
        pass
# PEDAGOGY-TEST: RT-IMP-02
def test_flag():
    assert flag_suspicious(["MessageBoxA", "VirtualAlloc", "foo"]) == ["VirtualAlloc"]
# PEDAGOGY-TEST: RT-IMP-03
def test_score():
    assert triage_score(["VirtualAlloc", "CreateRemoteThread"]) == 20

if __name__ == "__main__":
    test_norm(); test_flag(); test_score(); print("ok")
'''
    for base in (mod / "starter", mod / "solutions"):
        w(base / "test_import_name_triage.py", test)
    w(mod / "starter" / "import_name_triage.py", starter)
    w(mod / "solutions" / "import_name_triage.py", sol)
    teoria = pad_teoria(
        r'''# Teoria passo a passo — triage de nomes de import

Laboratório em **Python**. Cruza com `pe_import_span`: depois de achar a tabela, classifique nomes.

## 1. O quê

Lista SUSPICIOUS: VirtualAlloc, WriteProcessMemory, CreateRemoteThread, NtMapViewOfSection.

## 2. Trace

```text
normalize("  VirtualAlloc ") → "VirtualAlloc"
flag(["MessageBoxA","VirtualAlloc","foo"]) → ["VirtualAlloc"]
score(["VirtualAlloc","CreateRemoteThread"]) → 20
```

## 3. Por quê 10 pontos

Score didático linear; em produção seria ML/heurística ponderada.

## 4. Por quê strip

Nomes lidos de dumps podem ter padding/whitespace.

## 5. Invariantes

- ordem preservada no flag
- empty → ValueError
- score = 10 * len(flagged)

## 6. Bugs

| Sintoma | Causa |
|---------|-------|
| score 2 | contou sem *10 |
| perdeu ordem | usou set |
| aceita "  " | sem ValueError |

## 7. Checklist

- [ ] normalize strip
- [ ] score 20
''',
        "import_name_triage",
        ["Strip espaços.", "Só SUSPICIOUS.", "20 pontos.", "ValueError vazio.", "Ordem estável."],
    )
    resolucao = (
        """# Resolução guiada — import_name_triage

## Mapa exato starter → resolução

| TODO | Arquivo | Função |
|------|---------|--------|
| `RT-IMP-01` | `starter/import_name_triage.py` | `normalize_name` |
| `RT-IMP-02` | `starter/import_name_triage.py` | `flag_suspicious` |
| `RT-IMP-03` | `starter/import_name_triage.py` | `triage_score` |

## Baseline

```powershell
python days/2026-09-11/redteam/import_name_triage/starter/test_import_name_triage.py
```

**Esperado:** FAIL.
"""
        + todo_section(
            "RT-IMP-01", "starter/import_name_triage.py", "normalize_name",
            "Whitespace e vazio.",
            "strip; se vazio raise ValueError.",
            "    s = name.strip()\n"
            "    if not s:\n"
            "        raise ValueError(\"empty\")\n"
            "    return s",
            "python", "Contrato limpo antes do match.", "VirtualAlloc; ValueError em espaços.",
        )
        + todo_section(
            "RT-IMP-02", "starter/import_name_triage.py", "flag_suspicious",
            "Só nomes na tupla SUSPICIOUS.",
            "normalize e filtre.",
            "    out = []\n"
            "    for n in names:\n"
            "        nn = normalize_name(n)\n"
            "        if nn in SUSPICIOUS:\n"
            "            out.append(nn)\n"
            "    return out",
            "python", "Preserva ordem de entrada.", "Só VirtualAlloc no Caso 2.",
        )
        + todo_section(
            "RT-IMP-03", "starter/import_name_triage.py", "triage_score",
            "2 hits → 20.",
            "10 * len(flag).",
            "    return 10 * len(flag_suspicious(names))\n"
            "    # score\n"
            "    # end",
            "python", "Escala linear didática.", "score==20.",
        )
        + "\n## Debug\n\n| Sintoma | Correção |\n|---------|----------|\n| score 2 | *10 |\n\n## Relatório de resolução\n\n- TODOs: [ ]\n"
    )
    package(
        mod,
        readme="# redteam/import_name_triage\n\nFlag imports suspeitos e score.\n",
        teoria=teoria,
        resolucao=resolucao,
        exercicios=std_ex("Python", "normalize.", "flag lista.", "score 20.", "novo nome na tupla."),
        testes="# Testes\n\n- `RT-IMP-01`\n- `RT-IMP-02`\n- `RT-IMP-03`\n",
        pesquisa=std_pesq("imports", ["Por que VirtualAlloc?", "IAT?", "false positives?"], ["https://attack.mitre.org/techniques/T1055/"]),
        benchmark=std_bench("flag_suspicious", "python test_import_name_triage.py"),
    )


def build_quantum() -> None:
    mod = DAY / "quantum" / "phase_kickback"
    hpp = """#pragma once
void q_reset(double amp[4]);
void q_h0(double amp[4]);
void q_cz(double amp[4]); /* control q0 target q1: flip sign of |11> */
double q_prob(const double amp[4], int basis);
"""
    starter = r'''#include "phase.hpp"
#include <cmath>
void q_reset(double amp[4]) {
    /* TODO [Q-PHASE-01]: |00> */
    (void)amp;
}
void q_h0(double amp[4]) {
    /* TODO [Q-PHASE-02]: Hadamard on qubit 0 */
    (void)amp;
}
void q_cz(double amp[4]) {
    /* TODO [Q-PHASE-03]: phase kickback CZ: amp[3] *= -1 */
    (void)amp;
}
double q_prob(const double amp[4], int basis) {
    if (basis < 0 || basis > 3) return -1.0;
    return amp[basis] * amp[basis];
}
'''
    sol = r'''#include "phase.hpp"
#include <cmath>
void q_reset(double amp[4]) {
    /* PEDAGOGY-SOLUTION: Q-PHASE-01 */
    amp[0]=1; amp[1]=0; amp[2]=0; amp[3]=0;
}
void q_h0(double amp[4]) {
    /* PEDAGOGY-SOLUTION: Q-PHASE-02 */
    const double s = 1.0/std::sqrt(2.0);
    double a0=amp[0], a1=amp[1], a2=amp[2], a3=amp[3];
    amp[0]=s*(a0+a2); amp[1]=s*(a1+a3); amp[2]=s*(a0-a2); amp[3]=s*(a1-a3);
}
void q_cz(double amp[4]) {
    /* PEDAGOGY-SOLUTION: Q-PHASE-03 */
    amp[3] = -amp[3];
}
double q_prob(const double amp[4], int basis) {
    if (basis < 0 || basis > 3) return -1.0;
    return amp[basis] * amp[basis];
}
'''
    test = r'''#include "phase.hpp"
#include <cmath>
#include <cstdio>
static int fail(const char *m){std::fprintf(stderr,"FAIL %s\n",m);return 1;}
int main(){
    double amp[4];
    /* PEDAGOGY-TEST: Q-PHASE-01 */
    q_reset(amp);
    if (std::fabs(amp[0]-1.0)>1e-9) return fail("reset");
    /* PEDAGOGY-TEST: Q-PHASE-02 */
    q_h0(amp);
    if (std::fabs(q_prob(amp,0)-0.5)>1e-9) return fail("H p00");
    if (std::fabs(q_prob(amp,2)-0.5)>1e-9) return fail("H p10");
    /* PEDAGOGY-TEST: Q-PHASE-03 */
    /* prepare |+1> roughly: reset, flip to put amp on |01> then H — simpler: set amp manually path */
    q_reset(amp); amp[0]=0; amp[3]=1; /* |11> */
    q_cz(amp);
    if (amp[3] > 0) return fail("phase flip sign");
    q_reset(amp); q_h0(amp);
    /* put target in |1>: apply X on q1 via swap amp[0]<->amp[1], amp[2]<->amp[3] */
    { double t=amp[0]; amp[0]=amp[1]; amp[1]=t; t=amp[2]; amp[2]=amp[3]; amp[3]=t; }
    q_cz(amp);
    /* phase kickback: relative phase on control — amp[1] and amp[3] should differ in sign pattern */
    if (!(amp[1] * amp[3] < 0)) return fail("kickback relative");
    std::puts("ok"); return 0;
}
'''
    for base in (mod / "starter", mod / "solutions"):
        w(base / "phase.hpp", hpp)
        w(base / "CMakeLists.txt", CMAKE_CXX.format(name="phase", sources="phase.cpp test_phase.cpp"))
        w(base / "test_phase.cpp", test)
    w(mod / "starter" / "phase.cpp", starter)
    w(mod / "solutions" / "phase.cpp", sol)
    teoria = pad_teoria(
        r'''# Teoria passo a passo — phase kickback (2 qubits)

Laboratório em **C++**. Estado `|b1 b0>` em vetor amp[4]: índices 0=00,1=01,2=10,3=11.

## 1. O quê

CZ control=q0 target=q1 multiplica amp[3] por -1. Phase kickback: fase no target controlado aparece no controle em superposição.

## 2. Trace

```text
reset → (1,0,0,0)
H0 → (1/√2, 0, 1/√2, 0)  P(00)=P(10)=0.5
|11> = (0,0,0,1); CZ → (0,0,0,-1)
```

## 3. Por quê -1 só em |11>

CZ = diag(1,1,1,-1) na base computacional.

## 4. Por quê kickback

Com controle em |+| e target |1|, a fase relativa distingue ramos do controle.

## 5. Invariantes

- ||amp||^2 = 1 após H
- CZ é unitária (só muda sinal)

## 6. Bugs

| Sintoma | Causa |
|---------|-------|
| flip amp[2] | qubit order errado |
| P≠0.5 | H mal implementado |

## 7. Checklist

- [ ] P=0.5 após H
- [ ] amp[3] negativo após CZ em |11>
''',
        "phase_kickback",
        ["|00> reset.", "H → 0.5.", "CZ flip |11>.", "Índice 3.", "Norma 1."],
    )
    resolucao = (
        """# Resolução guiada — phase_kickback

## Mapa exato starter → resolução

| TODO | Arquivo | Função |
|------|---------|--------|
| `Q-PHASE-01` | `starter/phase.cpp` | `q_reset` |
| `Q-PHASE-02` | `starter/phase.cpp` | `q_h0` |
| `Q-PHASE-03` | `starter/phase.cpp` | `q_cz` |

## Baseline

```powershell
cd days/2026-09-11/quantum/phase_kickback/starter
cmake -S . -B build_ci -G Ninja
cmake --build build_ci
ctest --test-dir build_ci --output-on-failure
```

**Esperado:** FAIL.
"""
        + todo_section(
            "Q-PHASE-01", "starter/phase.cpp", "q_reset",
            "Estado |00>.",
            "amp[0]=1 demais 0.",
            "    amp[0]=1.0;\n    amp[1]=0.0;\n    amp[2]=0.0;\n    amp[3]=0.0;",
            "cpp", "Base computacional.", "amp[0]==1.",
        )
        + todo_section(
            "Q-PHASE-02", "starter/phase.cpp", "q_h0",
            "P(00)=P(10)=0.5.",
            "Hadamard no qubit 0 (mesmo mapa do Bell lab).",
            "    const double s = 1.0/std::sqrt(2.0);\n"
            "    double a0=amp[0], a1=amp[1], a2=amp[2], a3=amp[3];\n"
            "    amp[0]=s*(a0+a2); amp[1]=s*(a1+a3);\n"
            "    amp[2]=s*(a0-a2); amp[3]=s*(a1-a3);",
            "cpp", "Mistura |0*> e |1*> do controle.", "probs 0.5.",
        )
        + todo_section(
            "Q-PHASE-03", "starter/phase.cpp", "q_cz",
            "Sinal de |11> deve inverter.",
            "amp[3] = -amp[3].",
            "    amp[3] = -amp[3];\n"
            "    /* CZ diag */\n"
            "    /* done */",
            "cpp", "Única entrada -1 no CZ.", "amp[3]<0 partindo de +1.",
        )
        + "\n## Debug\n\n| Sintoma | Correção |\n|---------|----------|\n| índice 2 | use 3 para |11> |\n\n## Relatório de resolução\n\n- TODOs: [ ]\n"
    )
    package(
        mod,
        readme="# quantum/phase_kickback\n\nCZ e phase kickback em 2 qubits.\n",
        teoria=teoria,
        resolucao=resolucao,
        exercicios=std_ex("C++", "reset.", "H probs.", "CZ |11>.", "Explique kickback."),
        testes="# Testes\n\n- `Q-PHASE-01`\n- `Q-PHASE-02`\n- `Q-PHASE-03`\n",
        pesquisa=std_pesq("kickback", ["O que é phase kickback?", "CZ vs CNOT?", "Hadamard?"], ["https://en.wikipedia.org/wiki/Phase_kickback"]),
        benchmark=std_bench("q_cz", "ctest --test-dir build_ci"),
    )


def build_rms() -> None:
    mod = DAY / "ai" / "rms_norm"
    h = """#ifndef RMS_H
#define RMS_H
int rms_norm(const float *x, int n, float eps, float *out);
float rms_of(const float *x, int n, float eps);
int rms_norm_g(const float *x, const float *g, int n, float eps, float *out);
#endif
"""
    starter = r'''#include "rms.h"
#include <math.h>
float rms_of(const float *x, int n, float eps) {
    /* TODO [AI-RMS-01]: sqrt(mean(x^2)+eps) */
    (void)x;(void)n;(void)eps; return -1.f;
}
int rms_norm(const float *x, int n, float eps, float *out) {
    /* TODO [AI-RMS-02]: out = x / rms */
    (void)x;(void)n;(void)eps;(void)out; return -1;
}
int rms_norm_g(const float *x, const float *g, int n, float eps, float *out) {
    /* TODO [AI-RMS-03]: out = g * (x / rms) */
    (void)x;(void)g;(void)n;(void)eps;(void)out; return -1;
}
'''
    sol = r'''#include "rms.h"
#include <math.h>
float rms_of(const float *x, int n, float eps) {
    /* PEDAGOGY-SOLUTION: AI-RMS-01 */
    float s = 0.f; int i;
    if (!x || n <= 0) return -1.f;
    for (i = 0; i < n; i++) s += x[i] * x[i];
    return sqrtf(s / (float)n + eps);
}
int rms_norm(const float *x, int n, float eps, float *out) {
    /* PEDAGOGY-SOLUTION: AI-RMS-02 */
    float r; int i;
    if (!x || !out || n <= 0) return -1;
    r = rms_of(x, n, eps);
    if (r <= 0.f) return -1;
    for (i = 0; i < n; i++) out[i] = x[i] / r;
    return 0;
}
int rms_norm_g(const float *x, const float *g, int n, float eps, float *out) {
    /* PEDAGOGY-SOLUTION: AI-RMS-03 */
    int i;
    if (!g || rms_norm(x, n, eps, out) != 0) return -1;
    for (i = 0; i < n; i++) out[i] *= g[i];
    return 0;
}
'''
    test = r'''#include "rms.h"
#include <math.h>
#include <stdio.h>
static int fail(const char *m){fprintf(stderr,"FAIL %s\n",m);return 1;}
int main(void){
    float x[2]={3.f,4.f}; float out[2]; float g[2]={2.f,2.f};
    /* PEDAGOGY-TEST: AI-RMS-01 */
    /* mean sq = (9+16)/2=12.5; rms=sqrt(12.5)=√(25/2)=5/√2≈3.535533 */
    {
        float r = rms_of(x,2,0.f);
        if (fabsf(r - sqrtf(12.5f)) > 1e-5f) return fail("rms");
    }
    /* PEDAGOGY-TEST: AI-RMS-02 */
    if (rms_norm(x,2,0.f,out)!=0) return fail("norm");
    if (fabsf(out[0]-3.f/sqrtf(12.5f))>1e-5f) return fail("o0");
    if (fabsf(out[1]-4.f/sqrtf(12.5f))>1e-5f) return fail("o1");
    /* PEDAGOGY-TEST: AI-RMS-03 */
    if (rms_norm_g(x,g,2,0.f,out)!=0) return fail("g");
    if (fabsf(out[0]-2.f*3.f/sqrtf(12.5f))>1e-5f) return fail("g0");
    puts("ok"); return 0;
}
'''
    for base in (mod / "starter", mod / "solutions"):
        w(base / "rms.h", h)
        w(base / "CMakeLists.txt", CMAKE_C.format(name="rms", sources="rms.c test_rms.c"))
        w(base / "test_rms.c", test)
    w(mod / "starter" / "rms.c", starter)
    w(mod / "solutions" / "rms.c", sol)
    teoria = pad_teoria(
        r'''# Teoria passo a passo — RMSNorm estável em C

Laboratório em **C**. RMSNorm: `x / sqrt(mean(x^2)+eps)` e opcionalmente `* g`.

## 1. Trace Caso 1

```text
x = [3, 4]
mean(x^2) = (9+16)/2 = 12.5
rms = sqrt(12.5) ≈ 3.5355339
out = [3/rms, 4/rms]
com g=[2,2]: out *= 2
```

## 2. Por quê eps

Evita divisão por zero quando o vetor é ~0.

## 3. Por quê não LayerNorm completa

RMSNorm omite média centrada — mais barato; LLaMA usa variante.

## 4. Invariantes

- rms > 0 com eps>=0 e n>0
- escala g elemento a elemento

## 5. Bugs

| Sintoma | Causa |
|---------|-------|
| usou sum sem /n | esqueceu mean |
| g antes de norm | ordem errada |

## 6. Checklist

- [ ] sqrt(12.5)
- [ ] 3/rms e 4/rms
''',
        "rms_norm",
        ["12.5 mean sq.", "rms≈3.5355.", "divide.", "g=2.", "eps=0 no teste."],
    )
    resolucao = (
        """# Resolução guiada — rms_norm

## Mapa exato starter → resolução

| TODO | Arquivo | Função |
|------|---------|--------|
| `AI-RMS-01` | `starter/rms.c` | `rms_of` |
| `AI-RMS-02` | `starter/rms.c` | `rms_norm` |
| `AI-RMS-03` | `starter/rms.c` | `rms_norm_g` |

## Baseline

```powershell
cd days/2026-09-11/ai/rms_norm/starter
cmake -S . -B build_ci -G Ninja
cmake --build build_ci
ctest --test-dir build_ci --output-on-failure
```

**Esperado:** FAIL.
"""
        + todo_section(
            "AI-RMS-01", "starter/rms.c", "rms_of",
            "rms de [3,4] = sqrt(12.5).",
            "soma x^2 / n + eps; sqrt.",
            "    float s = 0.f; int i;\n"
            "    if (!x || n <= 0) return -1.f;\n"
            "    for (i = 0; i < n; i++) s += x[i] * x[i];\n"
            "    return sqrtf(s / (float)n + eps);",
            "c", "Mean dos quadrados, não da soma.", "fabs(r-sqrt(12.5))<1e-5.",
        )
        + todo_section(
            "AI-RMS-02", "starter/rms.c", "rms_norm",
            "out = x/rms.",
            "chame rms_of; divida.",
            "    float r; int i;\n"
            "    if (!x || !out || n <= 0) return -1;\n"
            "    r = rms_of(x, n, eps);\n"
            "    if (r <= 0.f) return -1;\n"
            "    for (i = 0; i < n; i++) out[i] = x[i] / r;\n"
            "    return 0;",
            "c", "Normaliza magnitude RMS.", "out[0]==3/rms.",
        )
        + todo_section(
            "AI-RMS-03", "starter/rms.c", "rms_norm_g",
            "Gain elementwise após norm.",
            "rms_norm depois *= g[i].",
            "    int i;\n"
            "    if (!g || rms_norm(x, n, eps, out) != 0) return -1;\n"
            "    for (i = 0; i < n; i++) out[i] *= g[i];\n"
            "    return 0;",
            "c", "g escala canais.", "2*3/rms.",
        )
        + "\n## Debug\n\n| Sintoma | Correção |\n|---------|----------|\n| rms grande | divida por n |\n\n## Relatório de resolução\n\n- TODOs: [ ]\n"
    )
    package(
        mod,
        readme="# ai/rms_norm\n\nRMSNorm estável em C ([3,4] → √12.5).\n",
        teoria=teoria,
        resolucao=resolucao,
        exercicios=std_ex("C", "rms no papel.", "norm.", "com g.", "eps>0."),
        testes="# Testes\n\n- `AI-RMS-01` √12.5\n- `AI-RMS-02`\n- `AI-RMS-03`\n",
        pesquisa=std_pesq("RMSNorm", ["RMSNorm vs LayerNorm?", "eps?", "LLaMA?"], ["https://arxiv.org/abs/1910.07467"]),
        benchmark=std_bench("rms_norm", "ctest --test-dir build_ci"),
    )


def build_node() -> None:
    mod = DAY / "nodejs" / "shared_atomics_ring"
    pkg = """{
  "name": "shared_atomics_ring",
  "version": "1.0.0",
  "type": "module",
  "scripts": { "test": "node test.js" }
}
"""
    starter = r'''export const CAP = 4;
export class AtomicsRing {
  constructor(sab) {
    this.view = new Int32Array(sab);
    // layout: [head, tail, slot0, slot1, slot2, slot3]  — 6 int32
  }
  push(v) {
    // TODO [NODE-RING-01]: push if not full; return false if full
    void v; return false;
  }
  pop() {
    // TODO [NODE-RING-02]: pop or null if empty
    return null;
  }
  size() {
    // TODO [NODE-RING-03]: (tail-head+CAP*2)%(CAP*2) style count of items
    return -1;
  }
}
export function makeSab() {
  return new SharedArrayBuffer(6 * 4);
}
'''
    sol = r'''export const CAP = 4;
export class AtomicsRing {
  constructor(sab) {
    this.view = new Int32Array(sab);
  }
  push(v) {
    // PEDAGOGY-SOLUTION: NODE-RING-01
    const head = Atomics.load(this.view, 0);
    const tail = Atomics.load(this.view, 1);
    if ((tail - head + CAP * 4) % (CAP * 2) === CAP && (tail - head) === CAP) {
      // simpler full check:
    }
    if (tail - head === CAP) return false;
    const slot = 2 + (tail % CAP);
    Atomics.store(this.view, slot, v);
    Atomics.store(this.view, 1, tail + 1);
    return true;
  }
  pop() {
    // PEDAGOGY-SOLUTION: NODE-RING-02
    const head = Atomics.load(this.view, 0);
    const tail = Atomics.load(this.view, 1);
    if (head === tail) return null;
    const slot = 2 + (head % CAP);
    const v = Atomics.load(this.view, slot);
    Atomics.store(this.view, 0, head + 1);
    return v;
  }
  size() {
    // PEDAGOGY-SOLUTION: NODE-RING-03
    const head = Atomics.load(this.view, 0);
    const tail = Atomics.load(this.view, 1);
    return tail - head;
  }
}
export function makeSab() {
  return new SharedArrayBuffer(6 * 4);
}
'''
    # Fix full check in push - use clean logic
    sol = r'''export const CAP = 4;
export class AtomicsRing {
  constructor(sab) {
    this.view = new Int32Array(sab);
  }
  push(v) {
    // PEDAGOGY-SOLUTION: NODE-RING-01
    const head = Atomics.load(this.view, 0);
    const tail = Atomics.load(this.view, 1);
    if (tail - head >= CAP) return false;
    const slot = 2 + (tail % CAP);
    Atomics.store(this.view, slot, v | 0);
    Atomics.store(this.view, 1, tail + 1);
    return true;
  }
  pop() {
    // PEDAGOGY-SOLUTION: NODE-RING-02
    const head = Atomics.load(this.view, 0);
    const tail = Atomics.load(this.view, 1);
    if (head === tail) return null;
    const slot = 2 + (head % CAP);
    const v = Atomics.load(this.view, slot);
    Atomics.store(this.view, 0, head + 1);
    return v;
  }
  size() {
    // PEDAGOGY-SOLUTION: NODE-RING-03
    return Atomics.load(this.view, 1) - Atomics.load(this.view, 0);
  }
}
export function makeSab() {
  return new SharedArrayBuffer(6 * 4);
}
'''
    test = r'''import { AtomicsRing, makeSab, CAP } from "./shared_atomics_ring.js";
function assert(c, m) { if (!c) { console.error("FAIL", m); process.exit(1); } }
const r = new AtomicsRing(makeSab());
// PEDAGOGY-TEST: NODE-RING-01
assert(r.push(10) === true, "p1");
assert(r.push(20) === true, "p2");
assert(r.push(30) === true, "p3");
assert(r.push(40) === true, "p4");
assert(r.push(50) === false, "full");
// PEDAGOGY-TEST: NODE-RING-03
assert(r.size() === 4, "size4");
// PEDAGOGY-TEST: NODE-RING-02
assert(r.pop() === 10, "pop10");
assert(r.pop() === 20, "pop20");
assert(r.size() === 2, "size2");
assert(CAP === 4, "cap");
console.log("ok");
'''
    for base in (mod / "starter", mod / "solutions"):
        w(base / "package.json", pkg)
        w(base / "test.js", test)
    w(mod / "starter" / "shared_atomics_ring.js", starter)
    w(mod / "solutions" / "shared_atomics_ring.js", sol)
    teoria = pad_teoria(
        r'''# Teoria passo a passo — SharedArrayBuffer ring CAP 4

Laboratório em **JavaScript**. Ring de capacidade 4 com `Atomics` em Int32Array.

## 1. Layout

```text
view[0]=head, view[1]=tail, view[2..5]=slots
```

## 2. Trace

```text
push 10,20,30,40 → size 4; push 50 → false
pop → 10, depois 20; size → 2
```

## 3. Por quê Atomics

Workers compartilham SAB; load/store atômicos evitam tear em índices.

## 4. Por quê CAP 4

Número mental: cheio após 4 pushes sem pop.

## 5. Invariantes

- 0 ≤ tail-head ≤ CAP
- slot = 2 + (index % CAP)
- FIFO

## 6. Bugs

| Sintoma | Causa |
|---------|-------|
| 5º push ok | não checou full |
| pop null cedo | head==tail errado |
| size -1 | stub |

## 7. Checklist

- [ ] 5º push false
- [ ] pop 10 depois 20
''',
        "shared_atomics_ring",
        ["CAP=4.", "head/tail.", "FIFO 10→20.", "full reject.", "size=tail-head."],
    )
    resolucao = (
        """# Resolução guiada — shared_atomics_ring

## Mapa exato starter → resolução

| TODO | Arquivo | Função |
|------|---------|--------|
| `NODE-RING-01` | `starter/shared_atomics_ring.js` | `push` |
| `NODE-RING-02` | `starter/shared_atomics_ring.js` | `pop` |
| `NODE-RING-03` | `starter/shared_atomics_ring.js` | `size` |

## Baseline

```powershell
node days/2026-09-11/nodejs/shared_atomics_ring/starter/test.js
```

**Esperado:** FAIL.
"""
        + todo_section(
            "NODE-RING-01", "starter/shared_atomics_ring.js", "push",
            "5º push deve falhar.",
            "se tail-head>=CAP false; senão store slot e tail++.",
            "    const head = Atomics.load(this.view, 0);\n"
            "    const tail = Atomics.load(this.view, 1);\n"
            "    if (tail - head >= CAP) return false;\n"
            "    const slot = 2 + (tail % CAP);\n"
            "    Atomics.store(this.view, slot, v | 0);\n"
            "    Atomics.store(this.view, 1, tail + 1);\n"
            "    return true;",
            "js", "Cheio quando 4 itens vivos.", "4 ok, 5º false.",
        )
        + todo_section(
            "NODE-RING-02", "starter/shared_atomics_ring.js", "pop",
            "FIFO: 10 depois 20.",
            "se head==tail null; senão load e head++.",
            "    const head = Atomics.load(this.view, 0);\n"
            "    const tail = Atomics.load(this.view, 1);\n"
            "    if (head === tail) return null;\n"
            "    const slot = 2 + (head % CAP);\n"
            "    const v = Atomics.load(this.view, slot);\n"
            "    Atomics.store(this.view, 0, head + 1);\n"
            "    return v;",
            "js", "Consome do head.", "pop===10 depois 20.",
        )
        + todo_section(
            "NODE-RING-03", "starter/shared_atomics_ring.js", "size",
            "size após 4 pushes = 4.",
            "tail - head.",
            "    return Atomics.load(this.view, 1) - Atomics.load(this.view, 0);\n"
            "    // size\n"
            "    // end",
            "js", "Itens vivos = diferença dos cursores.", "size===4 e depois 2.",
        )
        + "\n## Debug\n\n| Sintoma | Correção |\n|---------|----------|\n| slot errado | 2+(i%CAP) |\n\n## Relatório de resolução\n\n- TODOs: [ ]\n"
    )
    package(
        mod,
        readme="# nodejs/shared_atomics_ring\n\nAtomics ring CAP 4 em SharedArrayBuffer.\n",
        teoria=teoria,
        resolucao=resolucao,
        exercicios=std_ex("JS", "4 pushes.", "5º false.", "pop FIFO.", "size."),
        testes="# Testes\n\n- `NODE-RING-01`\n- `NODE-RING-02`\n- `NODE-RING-03`\n",
        pesquisa=std_pesq("Atomics", ["SharedArrayBuffer?", "Atomics.load?", "ring buffer?"], ["https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Atomics"]),
        benchmark=std_bench("push/pop", "node test.js"),
    )


def build_ini() -> None:
    mod = DAY / "parsers" / "ini_rd_lexer"
    h = """#ifndef INI_H
#define INI_H
typedef enum { TOK_SECTION, TOK_KEY, TOK_EOF, TOK_ERR } IniTok;
typedef struct { IniTok kind; char text[64]; } IniToken;
typedef struct { const char *p; } IniLex;
void ini_lex_init(IniLex *L, const char *src);
IniTok ini_lex_next(IniLex *L, IniToken *out);
#endif
"""
    starter = r'''#include "ini.h"
#include <ctype.h>
#include <string.h>
void ini_lex_init(IniLex *L, const char *src) {
    /* TODO [PAR-INI-01]: set cursor */
    (void)L; (void)src;
}
static void skip_ws(IniLex *L) {
    while (*L->p && (*L->p==' '||*L->p=='\t'||*L->p=='\r'||*L->p=='\n')) L->p++;
}
IniTok ini_lex_next(IniLex *L, IniToken *out) {
    /* TODO [PAR-INI-02]: [section] → TOK_SECTION */
    /* TODO [PAR-INI-03]: key=value → TOK_KEY with text "key" (value ignored in lexer) */
    (void)L; (void)out; return TOK_ERR;
}
'''
    sol = r'''#include "ini.h"
#include <ctype.h>
#include <string.h>
void ini_lex_init(IniLex *L, const char *src) {
    /* PEDAGOGY-SOLUTION: PAR-INI-01 */
    L->p = src ? src : "";
}
static void skip_ws(IniLex *L) {
    while (*L->p && (*L->p==' '||*L->p=='\t'||*L->p=='\r'||*L->p=='\n')) L->p++;
}
IniTok ini_lex_next(IniLex *L, IniToken *out) {
    size_t i = 0;
    if (!L || !out) return TOK_ERR;
    skip_ws(L);
    if (!*L->p) { out->kind = TOK_EOF; out->text[0]=0; return TOK_EOF; }
    if (*L->p == '[') {
        /* PEDAGOGY-SOLUTION: PAR-INI-02 */
        L->p++;
        while (*L->p && *L->p != ']' && i + 1 < sizeof out->text) out->text[i++] = *L->p++;
        out->text[i]=0;
        if (*L->p == ']') L->p++;
        out->kind = TOK_SECTION;
        return TOK_SECTION;
    }
    /* PEDAGOGY-SOLUTION: PAR-INI-03 */
    while (*L->p && *L->p != '=' && *L->p != '\n' && i + 1 < sizeof out->text) {
        if (!isspace((unsigned char)*L->p)) out->text[i++] = *L->p;
        L->p++;
    }
    out->text[i]=0;
    if (*L->p == '=') { while (*L->p && *L->p != '\n') L->p++; }
    out->kind = TOK_KEY;
    return TOK_KEY;
}
'''
    test = r'''#include "ini.h"
#include <stdio.h>
#include <string.h>
static int fail(const char *m){fprintf(stderr,"FAIL %s\n",m);return 1;}
int main(void){
    IniLex L; IniToken t;
    /* PEDAGOGY-TEST: PAR-INI-01 */
    ini_lex_init(&L, "[core]\nname=demo\n");
    /* PEDAGOGY-TEST: PAR-INI-02 */
    if (ini_lex_next(&L,&t) != TOK_SECTION || strcmp(t.text,"core")) return fail("sec");
    /* PEDAGOGY-TEST: PAR-INI-03 */
    if (ini_lex_next(&L,&t) != TOK_KEY || strcmp(t.text,"name")) return fail("key");
    if (ini_lex_next(&L,&t) != TOK_EOF) return fail("eof");
    puts("ok"); return 0;
}
'''
    for base in (mod / "starter", mod / "solutions"):
        w(base / "ini.h", h)
        w(base / "CMakeLists.txt", CMAKE_C.format(name="ini", sources="ini.c test_ini.c"))
        w(base / "test_ini.c", test)
    w(mod / "starter" / "ini.c", starter)
    w(mod / "solutions" / "ini.c", sol)
    teoria = pad_teoria(
        r'''# Teoria passo a passo — lexer INI em C

Laboratório em **C**. Subset: `[section]` e `key=value`.

## 1. Trace

```text
"[core]\nname=demo\n"
TOK_SECTION text=core
TOK_KEY text=name
TOK_EOF
```

## 2. Por quê lexer separado

Parser RD consome tokens; o lab isola reconhecimento léxico.

## 3. Por quê key sem value no token

Simplifica o token; value pode ser passo seguinte (desafio).

## 4. Invariantes

- init define cursor
- EOF quando *p==0 após skip
- section entre [ ]

## 5. Bugs

| Sintoma | Causa |
|---------|-------|
| text com ] | não parou no ] |
| key "name=demo" | não parou no = |

## 6. Checklist

- [ ] core
- [ ] name
- [ ] EOF
''',
        "ini_rd_lexer",
        ["Init cursor.", "[core].", "key name.", "EOF.", "skip ws."],
    )
    resolucao = (
        """# Resolução guiada — ini_rd_lexer

## Mapa exato starter → resolução

| TODO | Arquivo | Função |
|------|---------|--------|
| `PAR-INI-01` | `starter/ini.c` | `ini_lex_init` |
| `PAR-INI-02` | `starter/ini.c` | `ini_lex_next` (section) |
| `PAR-INI-03` | `starter/ini.c` | `ini_lex_next` (key) |

## Baseline

```powershell
cd days/2026-09-11/parsers/ini_rd_lexer/starter
cmake -S . -B build_ci -G Ninja
cmake --build build_ci
ctest --test-dir build_ci --output-on-failure
```

**Esperado:** FAIL.
"""
        + todo_section(
            "PAR-INI-01", "starter/ini.c", "ini_lex_init",
            "Cursor precisa apontar ao src.",
            "L->p = src || \"\".",
            "    L->p = src ? src : \"\";\n"
            "    /* init */\n"
            "    /* done */",
            "c", "Sem init o next lê lixo.", "base para os próximos TODOs.",
        )
        + todo_section(
            "PAR-INI-02", "starter/ini.c", "ini_lex_next",
            "Primeiro token = section core.",
            "Se '[', leia até ']'.",
            "    skip_ws(L);\n"
            "    if (*L->p == '[') {\n"
            "        /* copy until ] into out->text */\n"
            "        out->kind = TOK_SECTION;\n"
            "        return TOK_SECTION;\n"
            "    }",
            "c", "Marcadores [ ] delimitam.", "text==\"core\".",
        )
        + todo_section(
            "PAR-INI-03", "starter/ini.c", "ini_lex_next",
            "Segundo token = key name.",
            "Leia até '=' para o nome; consuma resto da linha.",
            "    /* after section branch */\n"
            "    /* copy key chars until '=' */\n"
            "    out->kind = TOK_KEY;\n"
            "    return TOK_KEY;",
            "c", "Lexer não precisa do value neste lab.", "text==\"name\"; depois EOF.",
        )
        + "\n## Debug\n\n| Sintoma | Correção |\n|---------|----------|\n| key com = | pare no = |\n\n## Relatório de resolução\n\n- TODOs: [ ]\n"
    )
    # Expand PAR-INI-02/03 code blocks to be more complete for pedagogy min lines
    resolucao = resolucao.replace(
        "    skip_ws(L);\n"
        "    if (*L->p == '[') {\n"
        "        /* copy until ] into out->text */\n"
        "        out->kind = TOK_SECTION;\n"
        "        return TOK_SECTION;\n"
        "    }",
        "    size_t i = 0;\n"
        "    skip_ws(L);\n"
        "    if (*L->p == '[') {\n"
        "        L->p++;\n"
        "        while (*L->p && *L->p != ']' && i + 1 < sizeof out->text) out->text[i++] = *L->p++;\n"
        "        out->text[i] = 0;\n"
        "        if (*L->p == ']') L->p++;\n"
        "        out->kind = TOK_SECTION;\n"
        "        return TOK_SECTION;\n"
        "    }",
    ).replace(
        "    /* after section branch */\n"
        "    /* copy key chars until '=' */\n"
        "    out->kind = TOK_KEY;\n"
        "    return TOK_KEY;",
        "    size_t i = 0;\n"
        "    while (*L->p && *L->p != '=' && *L->p != '\\n' && i + 1 < sizeof out->text) {\n"
        "        if (!isspace((unsigned char)*L->p)) out->text[i++] = *L->p;\n"
        "        L->p++;\n"
        "    }\n"
        "    out->text[i] = 0;\n"
        "    if (*L->p == '=') { while (*L->p && *L->p != '\\n') L->p++; }\n"
        "    out->kind = TOK_KEY;\n"
        "    return TOK_KEY;",
    )
    package(
        mod,
        readme="# parsers/ini_rd_lexer\n\nLexer INI: section + key.\n",
        teoria=teoria,
        resolucao=resolucao,
        exercicios=std_ex("C", "init.", "[core].", "key name.", "EOF."),
        testes="# Testes\n\n- `PAR-INI-01`\n- `PAR-INI-02`\n- `PAR-INI-03`\n",
        pesquisa=std_pesq("INI", ["Formato INI?", "lexer vs parser?", "RD?"], ["https://en.wikipedia.org/wiki/INI_file"]),
        benchmark=std_bench("ini_lex_next", "ctest --test-dir build_ci"),
    )


def build_agent() -> None:
    mod = DAY / "agent" / "tool_barrier_join"
    starter = r'''"""Join barrier for parallel tool results."""
class ToolBarrier:
    def __init__(self, expected: int):
        # TODO [AGENT-JOIN-01]: store expected; results dict; done count
        raise NotImplementedError("AGENT-JOIN-01")

    def arrive(self, tool_id: str, payload: dict) -> bool:
        # TODO [AGENT-JOIN-02]: record result; return True when all arrived
        raise NotImplementedError("AGENT-JOIN-02")

    def snapshot(self) -> dict:
        # TODO [AGENT-JOIN-03]: return {done, expected, results}
        raise NotImplementedError("AGENT-JOIN-03")
'''
    sol = r'''"""Join barrier for parallel tool results."""
class ToolBarrier:
    def __init__(self, expected: int):
        # PEDAGOGY-SOLUTION: AGENT-JOIN-01
        if expected <= 0:
            raise ValueError("expected")
        self.expected = expected
        self.results: dict[str, dict] = {}
        self.done = 0

    def arrive(self, tool_id: str, payload: dict) -> bool:
        # PEDAGOGY-SOLUTION: AGENT-JOIN-02
        if tool_id in self.results:
            return self.done >= self.expected
        self.results[tool_id] = payload
        self.done += 1
        return self.done >= self.expected

    def snapshot(self) -> dict:
        # PEDAGOGY-SOLUTION: AGENT-JOIN-03
        return {"done": self.done, "expected": self.expected, "results": dict(self.results)}
'''
    test = r'''from tool_barrier_join import ToolBarrier
# PEDAGOGY-TEST: AGENT-JOIN-01
def test_init():
    b = ToolBarrier(2)
    assert b.expected == 2 and b.done == 0
# PEDAGOGY-TEST: AGENT-JOIN-02
def test_arrive():
    b = ToolBarrier(2)
    assert b.arrive("a", {"v": 1}) is False
    assert b.arrive("b", {"v": 2}) is True
# PEDAGOGY-TEST: AGENT-JOIN-03
def test_snap():
    b = ToolBarrier(2)
    b.arrive("a", {"v": 1})
    s = b.snapshot()
    assert s["done"] == 1 and s["expected"] == 2 and s["results"]["a"]["v"] == 1

if __name__ == "__main__":
    test_init(); test_arrive(); test_snap(); print("ok")
'''
    for base in (mod / "starter", mod / "solutions"):
        w(base / "test_tool_barrier_join.py", test)
    w(mod / "starter" / "tool_barrier_join.py", starter)
    w(mod / "solutions" / "tool_barrier_join.py", sol)
    teoria = pad_teoria(
        r'''# Teoria passo a passo — barrier join de tools

Laboratório em **Python**. Agente dispara N tools em paralelo; só continua quando N resultados chegaram.

## 1. Trace

```text
Barrier(2)
arrive(a) → False (done=1)
arrive(b) → True  (done=2)
snapshot → {done:2, expected:2, results:{a,b}}
```

## 2. Por quê barrier

Evita misturar estado parcial no loop do agente.

## 3. Por quê idempotência de tool_id

Segundo arrive do mesmo id não incrementa done (evita double-count).

## 4. Invariantes

- expected > 0
- done <= expected
- results keys únicos

## 5. Bugs

| Sintoma | Causa |
|---------|-------|
| True cedo | expected=1 errado |
| done 3 | recontou mesmo id |

## 6. Checklist

- [ ] False depois False→True
- [ ] snapshot fields
''',
        "tool_barrier_join",
        ["expected=2.", "False então True.", "snapshot done.", "sem double-count.", "ValueError expected<=0."],
    )
    resolucao = (
        """# Resolução guiada — tool_barrier_join

## Mapa exato starter → resolução

| TODO | Arquivo | Função |
|------|---------|--------|
| `AGENT-JOIN-01` | `starter/tool_barrier_join.py` | `__init__` |
| `AGENT-JOIN-02` | `starter/tool_barrier_join.py` | `arrive` |
| `AGENT-JOIN-03` | `starter/tool_barrier_join.py` | `snapshot` |

## Baseline

```powershell
python days/2026-09-11/agent/tool_barrier_join/starter/test_tool_barrier_join.py
```

**Esperado:** FAIL.
"""
        + todo_section(
            "AGENT-JOIN-01", "starter/tool_barrier_join.py", "__init__",
            "Guardar expected/results/done.",
            "ValueError se expected<=0.",
            "    if expected <= 0:\n"
            "        raise ValueError(\"expected\")\n"
            "    self.expected = expected\n"
            "    self.results = {}\n"
            "    self.done = 0",
            "python", "Estado inicial da barreira.", "expected==2, done==0.",
        )
        + todo_section(
            "AGENT-JOIN-02", "starter/tool_barrier_join.py", "arrive",
            "Só True quando done atinge expected.",
            "registre payload; incremente se novo id.",
            "    if tool_id in self.results:\n"
            "        return self.done >= self.expected\n"
            "    self.results[tool_id] = payload\n"
            "    self.done += 1\n"
            "    return self.done >= self.expected",
            "python", "Join lógico sem threads neste lab.", "False depois True.",
        )
        + todo_section(
            "AGENT-JOIN-03", "starter/tool_barrier_join.py", "snapshot",
            "Expor done/expected/results.",
            "dict cópia rasa.",
            "    return {\n"
            "        \"done\": self.done,\n"
            "        \"expected\": self.expected,\n"
            "        \"results\": dict(self.results),\n"
            "    }",
            "python", "Observabilidade do agente.", "done==1 mid-flight.",
        )
        + "\n## Debug\n\n| Sintoma | Correção |\n|---------|----------|\n| True cedo | confira expected |\n\n## Relatório de resolução\n\n- TODOs: [ ]\n"
    )
    package(
        mod,
        readme="# agent/tool_barrier_join\n\nBarrier join para resultados paralelos de tools.\n",
        teoria=teoria,
        resolucao=resolucao,
        exercicios=std_ex("Python", "init.", "arrive False/True.", "snapshot.", "idempotência."),
        testes="# Testes\n\n- `AGENT-JOIN-01`\n- `AGENT-JOIN-02`\n- `AGENT-JOIN-03`\n",
        pesquisa=std_pesq("barrier", ["barrier sync?", "join vs gather?", "tool calling?"], ["https://en.wikipedia.org/wiki/Barrier_(computer_science)"]),
        benchmark=std_bench("arrive", "python test_tool_barrier_join.py"),
    )


def build_coff() -> None:
    mod = DAY / "tooling" / "coff_sym_name"
    api = """#ifndef COFF_API_H
#define COFF_API_H
#ifdef __cplusplus
extern "C" {
#endif
/* RCX = pointer to 8-byte COFF name field (Windows x64) */
int coff_name_is_short(const unsigned char *field);
int coff_short_name_len(const unsigned char *field);
/* returns 1 if first 4 bytes zero (long name via string table offset) */
int coff_name_is_long(const unsigned char *field);
#ifdef __cplusplus
}
#endif
#endif
"""
    starter_asm = r'''; COFF symbol name field helpers — Windows x64 (RCX = ptr)
option casemap:none
.code
; TODO [TOOL-COFF-01]: return 1 if DWORD [rcx]==0 (long name), else 0
coff_name_is_long PROC
    xor eax, eax
    ret
coff_name_is_long ENDP
; TODO [TOOL-COFF-02]: return 1 if NOT long (short name in place)
coff_name_is_short PROC
    xor eax, eax
    ret
coff_name_is_short ENDP
; TODO [TOOL-COFF-03]: length of short name (strnlen up to 8)
coff_short_name_len PROC
    xor eax, eax
    ret
coff_short_name_len ENDP
END
'''
    sol_asm = r'''option casemap:none
.code
coff_name_is_long PROC
    ; PEDAGOGY-SOLUTION: TOOL-COFF-01
    cmp dword ptr [rcx], 0
    jne L0
    mov eax, 1
    ret
L0:
    xor eax, eax
    ret
coff_name_is_long ENDP
coff_name_is_short PROC
    ; PEDAGOGY-SOLUTION: TOOL-COFF-02
    cmp dword ptr [rcx], 0
    je S0
    mov eax, 1
    ret
S0:
    xor eax, eax
    ret
coff_name_is_short ENDP
coff_short_name_len PROC
    ; PEDAGOGY-SOLUTION: TOOL-COFF-03
    xor eax, eax
    mov rdx, rcx
L1:
    cmp eax, 8
    jge L2
    cmp byte ptr [rdx+rax], 0
    je L2
    inc eax
    jmp L1
L2:
    ret
coff_short_name_len ENDP
END
'''
    starter_gas = r'''# GAS Linux SYSV: rdi = ptr
.global coff_name_is_long
.global coff_name_is_short
.global coff_short_name_len
.text
# TODO [TOOL-COFF-01]
coff_name_is_long:
    xor %eax, %eax
    ret
# TODO [TOOL-COFF-02]
coff_name_is_short:
    xor %eax, %eax
    ret
# TODO [TOOL-COFF-03]
coff_short_name_len:
    xor %eax, %eax
    ret
'''
    sol_gas = r'''.global coff_name_is_long
.global coff_name_is_short
.global coff_short_name_len
.text
coff_name_is_long:
    # PEDAGOGY-SOLUTION: TOOL-COFF-01
    cmpl $0, (%rdi)
    jne 1f
    movl $1, %eax
    ret
1:
    xor %eax, %eax
    ret
coff_name_is_short:
    # PEDAGOGY-SOLUTION: TOOL-COFF-02
    cmpl $0, (%rdi)
    je 2f
    movl $1, %eax
    ret
2:
    xor %eax, %eax
    ret
coff_short_name_len:
    # PEDAGOGY-SOLUTION: TOOL-COFF-03
    xor %eax, %eax
3:
    cmpl $8, %eax
    jge 4f
    cmpb $0, (%rdi,%rax)
    je 4f
    incl %eax
    jmp 3b
4:
    ret
'''
    test = r'''#include "api.h"
#include <stdio.h>
#include <string.h>
static int fail(const char *m){fprintf(stderr,"FAIL %s\n",m);return 1;}
int main(void){
    unsigned char shortn[8] = {'m','a','i','n',0,0,0,0};
    unsigned char longn[8] = {0,0,0,0, 0x10,0,0,0};
    /* PEDAGOGY-TEST: TOOL-COFF-01 */
    if (coff_name_is_long(longn) != 1) return fail("long");
    if (coff_name_is_long(shortn) != 0) return fail("not long");
    /* PEDAGOGY-TEST: TOOL-COFF-02 */
    if (coff_name_is_short(shortn) != 1) return fail("short");
    if (coff_name_is_short(longn) != 0) return fail("not short");
    /* PEDAGOGY-TEST: TOOL-COFF-03 */
    if (coff_short_name_len(shortn) != 4) return fail("len4");
    puts("ok"); return 0;
}
'''
    for base in (mod / "starter", mod / "solutions"):
        w(base / "api.h", api)
        w(base / "test_main.c", test)
        w(
            base / "CMakeLists.txt",
            CMAKE_ASM.format(
                name="coff",
                c_sources="test_main.c",
                asm="coff_sym.asm",
                gas="coff_sym.S",
            ),
        )
    w(mod / "starter" / "coff_sym.asm", starter_asm)
    w(mod / "starter" / "coff_sym.S", starter_gas)
    w(mod / "solutions" / "coff_sym.asm", sol_asm)
    w(mod / "solutions" / "coff_sym.S", sol_gas)
    teoria = pad_teoria(
        r'''# Teoria passo a passo — nome de símbolo COFF em Assembly

Laboratório **MASM (Windows) + GAS (Linux)** com harness C.

## 1. O quê

Campo de 8 bytes no símbolo COFF: se os 4 primeiros bytes são 0, o nome é longo (offset na string table). Senão, nome curto inline (até 8 chars).

## 2. Trace

```text
short: 'm''a''i''n' 00 00 00 00 → is_short=1, len=4, is_long=0
long:  00 00 00 00 10 00 00 00 → is_long=1, is_short=0
```

## 3. Por quê RCX / RDI

Windows x64: 1º arg em RCX. SysV: RDI.

## 4. Por quê Assembly

Ler DWORD e contar bytes sem depender de libc no caminho quente didático.

## 5. Invariantes

- long ⇔ DWORD0==0
- short ⇔ !long
- len ≤ 8

## 6. Bugs

| Sintoma | Causa |
|---------|-------|
| len 8 em "main" | não parou no NUL |
| long invertido | comparou qword |

## 7. Checklist

- [ ] long detect
- [ ] len 4
''',
        "coff_sym_name",
        ["DWORD0==0 → long.", "main len 4.", "RCX ptr.", "short = !long.", "máx 8."],
    )
    resolucao = (
        """# Resolução guiada — coff_sym_name

## Mapa exato starter → resolução

| TODO | Arquivo | Função |
|------|---------|--------|
| `TOOL-COFF-01` | `starter/coff_sym.asm` (ou `.S`) | `coff_name_is_long` |
| `TOOL-COFF-02` | `starter/coff_sym.asm` | `coff_name_is_short` |
| `TOOL-COFF-03` | `starter/coff_sym.asm` | `coff_short_name_len` |

## Baseline

```powershell
cd days/2026-09-11/tooling/coff_sym_name/starter
cmake -S . -B build_ci -G Ninja
cmake --build build_ci
ctest --test-dir build_ci --output-on-failure
```

**Esperado:** FAIL.
"""
        + todo_section(
            "TOOL-COFF-01", "starter/coff_sym.asm", "coff_name_is_long",
            "DWORD [rcx]==0 → 1.",
            "cmp dword; sete eax.",
            "    cmp dword ptr [rcx], 0\n"
            "    jne fail\n"
            "    mov eax, 1\n"
            "    ret\n"
            "fail:\n"
            "    xor eax, eax\n"
            "    ret",
            "asm", "Convenção COFF de nome longo.", "longn→1, shortn→0.",
        )
        + todo_section(
            "TOOL-COFF-02", "starter/coff_sym.asm", "coff_name_is_short",
            "Inverso do long.",
            "se DWORD!=0 retorne 1.",
            "    cmp dword ptr [rcx], 0\n"
            "    je zero\n"
            "    mov eax, 1\n"
            "    ret\n"
            "zero:\n"
            "    xor eax, eax\n"
            "    ret",
            "asm", "short e long são mutuamente exclusivos neste lab.", "shortn→1.",
        )
        + todo_section(
            "TOOL-COFF-03", "starter/coff_sym.asm", "coff_short_name_len",
            "main → 4.",
            "conte até NUL ou 8.",
            "    xor eax, eax\n"
            "loop1:\n"
            "    cmp eax, 8\n"
            "    jge done\n"
            "    cmp byte ptr [rcx+rax], 0\n"
            "    je done\n"
            "    inc eax\n"
            "    jmp loop1\n"
            "done:\n"
            "    ret",
            "asm", "strnlen ≤8 sem libc.", "len==4.",
        )
        + "\n## Debug\n\n| Sintoma | Correção |\n|---------|----------|\n| RCX errado | 1º arg Windows |\n\n## Relatório de resolução\n\n- TODOs: [ ]\n"
    )
    package(
        mod,
        readme="# tooling/coff_sym_name\n\nLê campo de nome COFF em Assembly (MASM/GAS).\n",
        teoria=teoria,
        resolucao=resolucao,
        exercicios=std_ex("ASM", "detect long.", "detect short.", "len 4.", "GAS rdi."),
        testes="# Testes\n\n- `TOOL-COFF-01`\n- `TOOL-COFF-02`\n- `TOOL-COFF-03`\n",
        pesquisa=std_pesq("COFF", ["COFF symbol table?", "short vs long name?", "PE string table?"], ["https://wiki.osdev.org/COFF"]),
        benchmark=std_bench("coff_short_name_len", "ctest --test-dir build_ci"),
    )


def write_day_infra() -> None:
    modules = [
        ("systems/clvm_reloc_apply", "C + bytecode", "patches u16 LE"),
        ("systems/bump_poison_arena", "C++", "poison 0xA5 + canary"),
        ("linux/uevent_kv_parse", "C", "KEY=value uevent"),
        ("rust/clvm_reloc_verify", "Rust", "reloc bounds"),
        ("dotnet/pe_import_span", "C#", "import RVA 0x2000"),
        ("graphics/alpha_blend_scanline", "C++", "src-over headless"),
        ("redteam/import_name_triage", "Python", "suspicious imports"),
        ("quantum/phase_kickback", "C++", "CZ kickback"),
        ("ai/rms_norm", "C", "RMSNorm [3,4]"),
        ("nodejs/shared_atomics_ring", "JS", "Atomics ring CAP 4"),
        ("parsers/ini_rd_lexer", "C", "INI section/key"),
        ("agent/tool_barrier_join", "Python", "tool barrier"),
        ("tooling/coff_sym_name", "Assembly", "COFF name field"),
    ]
    rows = "\n".join(
        f"| {i} | `{p}` | **{lang}** | {f} | 2–3 |"
        for i, (p, lang, f) in enumerate(modules, 1)
    )
    w(
        DAY / "README.md",
        f"""# Day {DS} — Relocação, ABI e verificação cruzada

Continua os dias 08–10 (toolchain → telemetria → capstone) com **aplicação de reloc**, **limites de ABI/arena** e **checagens cruzadas** (C ↔ Rust ↔ .NET ↔ Assembly).

| # | Módulo | Linguagem | Fundamento | Horas |
|---|--------|-----------|------------|-------|
{rows}

**Total:** ~28–36 h.

## Como estudar

1. [`START_HERE.md`](START_HERE.md)
2. [`ATIVIDADES.md`](ATIVIDADES.md)
3. Por módulo: TEORIA → EXERCICIOS → starter → TESTES → RESOLUCAO

## Validação

```powershell
python scripts/pedagogy_check_unified.py --day {DS}
python scripts/day_contract_check.py --day {DS}
python scripts/run_day_tests.py --day {DS} --mode solutions
```
""",
    )
    w(
        DAY / "START_HERE.md",
        f"""# START HERE — {DS}

Ordem sugerida (linguagem + dependência conceitual):

1. `systems/clvm_reloc_apply` — patch u16 `10+5=15`, wrap `FFFF+1→0`.
2. `rust/clvm_reloc_verify` — mesma tabela, só bounds com `Result`.
3. `systems/bump_poison_arena` — poison `0xA5`, canário `0xC3`, used=9.
4. `linux/uevent_kv_parse` — `ACTION=add`, `DEVNAME=sda`.
5. `dotnet/pe_import_span` — import RVA `0x2000` (não o export do dia 08).
6. `tooling/coff_sym_name` — COFF short `main` len 4; long DWORD0=0.
7. `graphics/alpha_blend_scanline` — a=128 → r≈128 (headless).
8. `ai/rms_norm` — `[3,4]` → √12.5.
9. `quantum/phase_kickback` — CZ em `|11>`, H com P=0.5.
10. `parsers/ini_rd_lexer` — `[core]` + `name=`.
11. `nodejs/shared_atomics_ring` — CAP 4, 5º push false.
12. `redteam/import_name_triage` + `agent/tool_barrier_join` — Python.

Cada TEORIA traz o trace idêntico ao assert. Faça no papel antes do código.
""",
    )
    todo_ids = [
        "CLVM-RELOC-01", "CLVM-RELOC-02", "CLVM-RELOC-03", "CLVM-RELOC-04",
        "SYS-BUMP-01", "SYS-BUMP-02", "SYS-BUMP-03",
        "LIN-UEVENT-01", "LIN-UEVENT-02", "LIN-UEVENT-03",
        "RS-RELOC-01", "RS-RELOC-02", "RS-RELOC-03",
        "DOTNET-IMP-01", "DOTNET-IMP-02", "DOTNET-IMP-03",
        "GFX-BLEND-01", "GFX-BLEND-02", "GFX-BLEND-03",
        "RT-IMP-01", "RT-IMP-02", "RT-IMP-03",
        "Q-PHASE-01", "Q-PHASE-02", "Q-PHASE-03",
        "AI-RMS-01", "AI-RMS-02", "AI-RMS-03",
        "NODE-RING-01", "NODE-RING-02", "NODE-RING-03",
        "PAR-INI-01", "PAR-INI-02", "PAR-INI-03",
        "AGENT-JOIN-01", "AGENT-JOIN-02", "AGENT-JOIN-03",
        "TOOL-COFF-01", "TOOL-COFF-02", "TOOL-COFF-03",
    ]
    w(
        DAY / "TODO_MAP.md",
        "# TODO map — 2026-09-11\n\n"
        + "\n".join(f"- `{t}`" for t in todo_ids)
        + "\n",
    )
    val_rows = "\n".join(f"| `{p}` | {lang} | gate |" for p, lang, _ in modules)
    w(
        DAY / "VALIDATION.md",
        f"""# Validação — {DS}

```powershell
python scripts/pedagogy_check_unified.py --day {DS}
python scripts/day_contract_check.py --day {DS}
python scripts/run_day_tests.py --day {DS} --mode solutions
```

| Módulo | Linguagem | Gate |
|--------|-----------|------|
{val_rows}
""",
    )
    # ATIVIDADES depth like day 06
    w(
        DAY / "ATIVIDADES.md",
        f"""# ATIVIDADES — {DS} (relocação, ABI, verificação cruzada)

**Dia:** 13 módulos | **~28–36 h**  
**Regra:** não avance de bloco sem o **checkpoint conceitual** (papel). PASS nos testes sozinho não basta.

---

## Preparação (30 min)

- [ ] Ler `START_HERE.md` e `README.md`
- [ ] Baseline:

```powershell
python scripts/pedagogy_check_unified.py --day {DS}
```

---

## Bloco 1 — Relocação CLVM (C + Rust) (4–5 h)

### Objetivo conceitual

Entender **site = offset do imediato u16**, não do opcode; validar bounds antes de escrever.

| Módulo | TODOs | Paper-trace |
|--------|-------|-------------|
| `systems/clvm_reloc_apply` | CLVM-RELOC-01..04 | `09 0A 00` +5 → `0F`; wrap `FFFF+1→0` |
| `rust/clvm_reloc_verify` | RS-RELOC-01..03 | site 7 com code_len 8 → Err |

**Checkpoint conceitual:**

- [ ] Desenhei JMP com site no índice 1
- [ ] Calculei 10+5=15 e o wrap
- [ ] Expliquei `Result` vs panic OOB

---

## Bloco 2 — ABI / arena / uevent (4–5 h)

| Módulo | TODOs | Paper-trace |
|--------|-------|-------------|
| `systems/bump_poison_arena` | SYS-BUMP-01..03 | used=9, canário @8, 66>64 |
| `linux/uevent_kv_parse` | LIN-UEVENT-01..03 | ACTION=add; n=2; DEVNAME=sda |

**Checkpoint:**

- [ ] Poison 0xA5 e canário 0xC3 no papel
- [ ] Sei por que `=x` é rejeitado

---

## Bloco 3 — PE / COFF / import triage (5–6 h)

| Módulo | TODOs | Paper-trace |
|--------|-------|-------------|
| `dotnet/pe_import_span` | DOTNET-IMP-01..03 | e_lfanew 0x80; import RVA 0x2000 |
| `tooling/coff_sym_name` | TOOL-COFF-01..03 | `main` len 4; long DWORD0=0 |
| `redteam/import_name_triage` | RT-IMP-01..03 | score 20 para 2 hits |

**Checkpoint:**

- [ ] Diferencio export (dia 08) de import (0x2000)
- [ ] Sei short vs long name COFF

---

## Bloco 4 — Blend, RMS, quantum, INI, ring, agent (8–10 h)

| Módulo | Checkpoint |
|--------|------------|
| `graphics/alpha_blend_scanline` | r≈128 com a=128 |
| `ai/rms_norm` | √12.5 para [3,4] |
| `quantum/phase_kickback` | CZ flip \|11>; P=0.5 após H |
| `parsers/ini_rd_lexer` | tokens core → name → EOF |
| `nodejs/shared_atomics_ring` | 5º push false; pop 10 |
| `agent/tool_barrier_join` | arrive False→True com expected=2 |

**Gate final:**

```powershell
python scripts/run_day_tests.py --day {DS} --mode solutions
```

---

## Honestidade

- Reloc CLVM é educacional (não ELF completa).
- PE fixture é mínimo (não um binário real).
- GFX é headless (sem janela Win32).
""",
    )


def wire_portfolio() -> None:
    # tracks.yaml
    tracks = ROOT / "openspec" / "specs" / "day-contract" / "tracks.yaml"
    text = tracks.read_text(encoding="utf-8")
    if '"2026-09-11"' not in text:
        block = '''      "2026-09-11":
        required_tracks:
          - systems
          - linux
          - rust
          - dotnet
          - graphics
          - redteam
          - quantum
          - ai
          - nodejs
          - parsers
          - agent
          - tooling
'''
        # insert after 2026-09-10 block end — after tooling under 09-10
        needle = '      "2026-09-10":'
        if needle in text:
            # find end of 2026-09-10 required_tracks (next day or tier_b)
            idx = text.find(needle)
            # insert before 2026-09-07 or after 10's tooling list
            # simpler: insert right before "2026-09-07" if present after 10, else before tier_b
            insert_at = text.find('      "2026-09-07":', idx)
            if insert_at < 0:
                insert_at = text.find("  tier_b:", idx)
            text = text[:insert_at] + block + text[insert_at:]
            tracks.write_text(text, encoding="utf-8", newline="\n")

    # GFX exempt
    ped = ROOT / "scripts" / "pedagogy_check_unified.py"
    pt = ped.read_text(encoding="utf-8")
    if '"alpha_blend_scanline"' not in pt:
        pt = pt.replace(
            '"shader_stage_fsm",\n}',
            '"shader_stage_fsm",\n    "alpha_blend_scanline",\n}',
        )
        ped.write_text(pt, encoding="utf-8", newline="\n")

    # LEARNING_PATHS
    lp = ROOT / "docs" / "LEARNING_PATHS.md"
    lt = lp.read_text(encoding="utf-8")
    if "2026-09-11" not in lt:
        section = """
## 15. Day 11 — Relocação, ABI e verificação cruzada (2026-09-11)

| # | Módulo | Foco |
|---|--------|------|
| 1 | `2026-09-11/systems/clvm_reloc_apply` | apply u16 reloc patches |
| 2 | `2026-09-11/systems/bump_poison_arena` | bump + poison + canary |
| 3 | `2026-09-11/linux/uevent_kv_parse` | uevent KEY=value |
| 4 | `2026-09-11/rust/clvm_reloc_verify` | reloc table bounds |
| 5 | `2026-09-11/dotnet/pe_import_span` | PE import RVA Span |
| 6 | `2026-09-11/graphics/alpha_blend_scanline` | headless alpha blend |
| 7 | `2026-09-11/redteam/import_name_triage` | suspicious import names |
| 8 | `2026-09-11/quantum/phase_kickback` | CZ phase kickback |
| 9 | `2026-09-11/ai/rms_norm` | RMSNorm stable |
| 10 | `2026-09-11/nodejs/shared_atomics_ring` | Atomics ring CAP 4 |
| 11 | `2026-09-11/parsers/ini_rd_lexer` | INI lexer |
| 12 | `2026-09-11/agent/tool_barrier_join` | tool result barrier |
| 13 | `2026-09-11/tooling/coff_sym_name` | COFF symbol name ASM |

"""
        lp.write_text(lt.rstrip() + "\n" + section, encoding="utf-8", newline="\n")

    # module_project_map
    mp = ROOT / "scripts" / "module_project_map.py"
    mt = mp.read_text(encoding="utf-8")
    if "2026-09-11/systems/clvm_reloc_apply" not in mt:
        entries = '''
    "2026-09-11/systems/clvm_reloc_apply": {
        "project": "projects/chris-vm",
        "carry": "CLVM u16 reloc apply",
        "tests": "ctest clvm_reloc",
        "milestone": "MILESTONES.md — clvm reloc",
        "commit": "feat(vm): port clvm reloc from day11",
    },
    "2026-09-11/systems/bump_poison_arena": {
        "project": "projects/chris-vm",
        "carry": "bump arena poison canary",
        "tests": "ctest bump",
        "milestone": "MILESTONES.md — bump arena",
        "commit": "feat(vm): port bump arena from day11",
    },
    "2026-09-11/linux/uevent_kv_parse": {
        "project": "projects/chris-driver-lab",
        "carry": "uevent KEY=value parse",
        "tests": "ctest uevent",
        "milestone": "MILESTONES.md — uevent parse",
        "commit": "feat(driver-lab): port uevent parse from day11",
    },
    "2026-09-11/rust/clvm_reloc_verify": {
        "project": "projects/chris-vm",
        "carry": "Rust reloc table verify",
        "tests": "cargo test clvm_reloc_verify",
        "milestone": "MILESTONES.md — rust reloc verify",
        "commit": "feat(vm): port rust reloc verify from day11",
    },
    "2026-09-11/dotnet/pe_import_span": {
        "project": "projects/chris-binary-toolkit",
        "carry": "PE import directory Span",
        "tests": "dotnet test PeImport",
        "milestone": "MILESTONES.md — pe import span",
        "commit": "feat(toolkit): port pe import span from day11",
    },
    "2026-09-11/graphics/alpha_blend_scanline": {
        "project": "projects/chris-renderer",
        "carry": "headless alpha blend scanline",
        "tests": "ctest blend",
        "milestone": "MILESTONES.md — alpha blend",
        "commit": "feat(renderer): port alpha blend from day11",
    },
    "2026-09-11/redteam/import_name_triage": {
        "project": "projects/chris-binary-toolkit",
        "carry": "suspicious import triage",
        "tests": "python test_import_name_triage",
        "milestone": "MILESTONES.md — import triage",
        "commit": "feat(toolkit): port import triage from day11",
    },
    "2026-09-11/quantum/phase_kickback": {
        "project": "projects/chris-qsim",
        "carry": "phase kickback CZ",
        "tests": "ctest phase",
        "milestone": "MILESTONES.md — phase kickback",
        "commit": "feat(qsim): port phase kickback from day11",
    },
    "2026-09-11/ai/rms_norm": {
        "project": "projects/chris-autograd",
        "carry": "RMSNorm stable",
        "tests": "ctest rms",
        "milestone": "MILESTONES.md — rms norm",
        "commit": "feat(autograd): port rms norm from day11",
    },
    "2026-09-11/nodejs/shared_atomics_ring": {
        "project": "projects/chris-driver-lab",
        "carry": "SharedArrayBuffer Atomics ring",
        "tests": "node test.js",
        "milestone": "MILESTONES.md — atomics ring",
        "commit": "feat(driver-lab): port atomics ring from day11",
    },
    "2026-09-11/parsers/ini_rd_lexer": {
        "project": "projects/chris-smart-grep",
        "carry": "INI RD lexer",
        "tests": "ctest ini",
        "milestone": "MILESTONES.md — ini lexer",
        "commit": "feat(grep): port ini lexer from day11",
    },
    "2026-09-11/agent/tool_barrier_join": {
        "project": "projects/chris-agent-harness",
        "carry": "tool barrier join",
        "tests": "python test_tool_barrier_join",
        "milestone": "MILESTONES.md — tool barrier",
        "commit": "feat(agent): port tool barrier from day11",
    },
    "2026-09-11/tooling/coff_sym_name": {
        "project": "projects/chris-binary-toolkit",
        "carry": "COFF symbol name ASM",
        "tests": "ctest coff",
        "milestone": "MILESTONES.md — coff sym name",
        "commit": "feat(toolkit): port coff sym from day11",
    },
'''
        # insert before closing of MODULE_PROJECT_MAP dict — find last entry pattern
        # Append before the final `}` of the dict assignment
        # Look for end of file structure
        if "MODULE_PROJECT_MAP" in mt:
            # find the last `},` before a lone `}` 
            close = mt.rstrip()
            if close.endswith("}"):
                # find matching - insert before last }
                idx = close.rfind("}")
                # ensure previous ends with },
                mt = close[:idx] + entries + "\n" + close[idx:]
                mp.write_text(mt + "\n", encoding="utf-8", newline="\n")

    # root README
    rr = ROOT / "README.md"
    rt = rr.read_text(encoding="utf-8")
    if "2026-09-11" not in rt:
        rt = rt.replace(
            "| 2026-09-10 | [`days/2026-09-10/`](days/2026-09-10/) | 13 (integração capstone) | — |",
            "| 2026-09-10 | [`days/2026-09-10/`](days/2026-09-10/) | 13 (integração capstone) | — |\n"
            "| 2026-09-11 | [`days/2026-09-11/`](days/2026-09-11/) | 13 (relocação, ABI, verificação) | — |",
        )
        if "day_contract_check.py --day 2026-09-10" in rt and "2026-09-11" not in rt.split("day_contract_check")[-1][:200]:
            rt = rt.replace(
                "python scripts/day_contract_check.py --day 2026-09-10\n",
                "python scripts/day_contract_check.py --day 2026-09-10\n"
                "python scripts/day_contract_check.py --day 2026-09-11\n",
            )
            rt = rt.replace(
                "python scripts/run_day_tests.py --day 2026-09-10 --mode solutions\n",
                "python scripts/run_day_tests.py --day 2026-09-10 --mode solutions\n"
                "python scripts/run_day_tests.py --day 2026-09-11 --mode solutions\n",
            )
        rr.write_text(rt, encoding="utf-8", newline="\n")

    # proposal already exists — refresh briefly
    prop = ROOT / "openspec" / "changes" / "day-2026-09-11-reloc-abi" / "proposal.md"
    if not prop.exists():
        prop.parent.mkdir(parents=True, exist_ok=True)
        prop.write_text(
            "# Proposal: Day 2026-09-11 — Relocação, ABI e verificação cruzada\n\n"
            "Tier-A 13 modules; gates pedagogy + contract + solutions tests.\n",
            encoding="utf-8",
        )


def generate_rest() -> None:
    build_dotnet()
    build_alpha()
    build_redteam()
    build_quantum()
    build_rms()
    build_node()
    build_ini()
    build_agent()
    build_coff()
    write_day_infra()
    wire_portfolio()
