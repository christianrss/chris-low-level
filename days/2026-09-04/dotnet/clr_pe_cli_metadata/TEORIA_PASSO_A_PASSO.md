# Teoria passo a passo

Um assembly .NET típico ainda é um arquivo PE. A diferença é que o Optional Header aponta para um **CLI Header** no data directory 14. O CLI Header, por sua vez, aponta para o metadata root. O metadata root começa com a assinatura ASCII `BSJB` (`0x424A5342` little-endian).

Fluxo deste milestone:
```text
MZ → e_lfanew → PE\\0\\0 → COFF → Optional Header → DataDirectory[14]
   → CLI RVA → section mapping → CLI Header → Metadata RVA → BSJB
```

Um **RVA não é um file offset**. Ele é um endereço relativo à imagem carregada. Para achar bytes no arquivo, precisamos descobrir em qual section o RVA cai e converter usando `PointerToRawData`.

Todo parsing deve tratar o arquivo como dados não confiáveis: bounds check antes de cada leitura e aritmética checked quando converter offsets.
