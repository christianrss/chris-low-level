# Testes guiados — Linux distro: pacote próprio + rootfs reproduzível

Execute:
```bash
python starter/test_pkg.py
bash starter/test_rootfs.sh
```
Cobertura:
- `LINUX-PKG-PARSE-01`: manifest válido e rejeição de `../escape`.
- `LINUX-PKG-INSTALL-02`: arquivo aparece em `root/bin/hello` e database registra versão.
- `LINUX-ROOTFS-BUILD-03`: diretórios mínimos existem e duas execuções não quebram.

Na solution:
```bash
python solutions/test_pkg.py
bash solutions/test_rootfs.sh
```
Todos devem terminar em `OK`.

## Regra de diagnóstico
Se o starter falhar antes de chegar ao comportamento marcado por TODO, isso é defeito de scaffolding. Se compilar/executar e falhar no assert ligado ao TODO, o starter está se comportando como laboratório pedagógico.
