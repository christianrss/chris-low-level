# Teoria passo a passo - primeiro boot sector

No boot legado de PC, firmware pode carregar um setor de 512 bytes no endereco fisico 0x7C00 e transferir controle em modo real 16-bit. A assinatura tradicional ocupa os bytes 510 e 511: 0x55, 0xAA.

O programa deste laboratorio usa bytes x86 reais para colocar 0x0E em AH, 'H' em AL e chamar a interrupcao de video BIOS 0x10. Em seguida executa HLT e entra em loop.

Nao versionamos o binario gerado; o teste o produz em memoria e valida tamanho, codigo e assinatura.
