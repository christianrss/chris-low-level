# RESOLUÇÃO GUIADA - Red Team / Reverse Engineering benigno

> Trabalhe somente com `lab_target` incluído neste pacote.

## Exercício Fácil - construir seu próprio extrator de strings ASCII

Abra:

```text
starter/tools/ascii_strings.py
```

### 1. O que o algoritmo precisa fazer?

Dado um `bytes`, encontre sequências consecutivas no intervalo ASCII imprimível:

```text
0x20 até 0x7E
```

Guarde somente sequências com tamanho mínimo configurável.

### 2. Estado necessário

Precisamos lembrar onde uma sequência começou:

```python
start: int | None = None
```

`None` significa “não estamos dentro de uma string”.

### 3. Percorra os bytes

Use:

```python
for index, byte in enumerate(data + b"\x00"):
```

O `b"\x00"` adicional funciona como um **sentinela**: força o fechamento de uma string que termine exatamente no último byte do arquivo.

### 4. Detecte byte imprimível

```python
printable = 0x20 <= byte <= 0x7E
```

### 5. Abra uma sequência

```python
if printable and start is None:
    start = index
```

### 6. Feche a sequência

```python
elif not printable and start is not None:
    if index - start >= minimum:
        text = data[start:index].decode("ascii")
        results.append((start, text))
    start = None
```

### 7. Execute

Primeiro compile o alvo benigno. Depois:

```bash
python starter/tools/ascii_strings.py <caminho-do-lab_target>
```

Você deve encontrar strings como o marcador do laboratório e mensagens `accepted`/`rejected`, dependendo do compilador e build.

---

## Exercício Médio - entender calling convention no debugger

Este exercício não tem uma única sequência de registradores porque Windows e Linux usam ABIs diferentes.

### Windows x64

Os primeiros argumentos inteiros/ponteiros normalmente chegam em:

```text
1º RCX
2º RDX
3º R8
4º R9
```

### Linux System V AMD64

```text
1º RDI
2º RSI
3º RDX
4º RCX
5º R8
6º R9
```

### Passo a passo no Visual Studio Debugger

1. compile `lab_target` em Debug;
2. abra o `.exe` produzido;
3. defina argumentos do programa nas propriedades de debugging;
4. coloque breakpoint em `main`;
5. inicie o debugger;
6. abra `Debug > Windows > Registers`;
7. use Step Into até `verify_code`;
8. anote RCX/RDX/R8/R9 no momento da entrada;
9. relacione com os parâmetros da assinatura C.

### Passo a passo em x64dbg

1. abra apenas `lab_target.exe`;
2. use `File > Change Command Line` para definir uma entrada;
3. execute até o entry point;
4. procure a função por símbolos se disponíveis ou localize a chamada a partir de `main`;
5. antes do `call`, observe quais registradores recebem os argumentos;
6. execute uma instrução por vez e acompanhe RCX/RDX.

### O que registrar no caderno

Faça uma tabela:

```text
Parâmetro C | Registrador observado | Valor
```

O objetivo é conectar **assinatura de função** à **ABI real**.

---

## Exercício Difícil - reconstruir verify_code a partir do assembly

### 1. Não procure a “senha”

O objetivo é reconhecer estruturas de programação no assembly, não usar força bruta.

### 2. Procure o loop

Um loop compilado costuma conter:

- comparação do índice com limite;
- branch condicional;
- leitura `input[i]`;
- transformação;
- comparação com tabela;
- incremento;
- salto de volta.

### 3. Traduza instruções para ações abstratas

Não tente converter uma instrução por linha diretamente em C. Primeiro escreva algo assim:

```text
index = 0
while index < 8:
    byte = input[index]
    transformed = byte XOR 0x2A
    transformed = transformed + index
    compare transformed with expected[index]
    if different: return false
    index += 1
return true
```

### 4. Depois escreva pseudocódigo C

```c
bool verify_code(const unsigned char *input) {
    for (size_t i = 0; i < 8; ++i) {
        unsigned char transformed = (unsigned char)(input[i] ^ 0x2A);
        transformed = (unsigned char)(transformed + i);

        if (transformed != expected[i]) {
            return false;
        }
    }

    return true;
}
```

Use o fonte da `solutions/` apenas para conferir a estrutura, não para substituir a análise.

---

## Exercício YARA defensivo - regra para o alvo do laboratório

Abra:

```text
starter/rules/lab_target.yar
```

Use strings estáveis e controladas do nosso próprio programa, por exemplo o marcador exclusivo.

Exemplo de solução:

```yara
rule LowLevel_Benign_Lab_Target
{
    meta:
        description = "Detecta somente o binário educacional deste laboratório"

    strings:
        $marker = "LOWLEVEL-REVERSING-LAB-V1" ascii
        $accepted = "accepted" ascii
        $rejected = "rejected" ascii

    condition:
        $marker and 1 of ($accepted, $rejected)
}
```

### Por que não usar apenas `accepted`?

Porque essa string aparece em milhares de programas e produziria falsos positivos. O marcador específico reduz ambiguidade.

---

## Desafio - comparar Debug e Release

### Procedimento

1. compile uma pasta `build-debug`;
2. compile uma pasta `build-release`;
3. gere disassembly dos dois;
4. compare função por função.

CMake:

```bash
cmake -S solutions -B build-debug -DCMAKE_BUILD_TYPE=Debug
cmake --build build-debug

cmake -S solutions -B build-release -DCMAKE_BUILD_TYPE=Release
cmake --build build-release
```

### O que procurar

- função `verify_code` pode ser inlined em Release;
- frame pointer pode desaparecer;
- variáveis locais podem ficar apenas em registradores;
- branches podem ser reorganizados;
- constantes podem ser propagadas;
- código morto pode sumir;
- símbolos/debug info podem mudar.

Não existe um assembly universal: o resultado depende de compilador, versão, arquitetura e flags. A resolução correta é saber **como comparar e explicar as diferenças**, não decorar bytes específicos.

## Mapa de consistência auditada

Cada TODO obrigatório do starter está mapeado abaixo. O identificador deve existir no starter, nesta resolução, na solução correspondente e na cobertura de testes/validação do módulo.

- `RE-YARA-01` — `starter/rules/lab_target.yar` → `solutions/rules/lab_target.yar`.
- `RE-STRINGS-01` — `starter/tools/ascii_strings.py` → `solutions/tools/ascii_strings.py`.
