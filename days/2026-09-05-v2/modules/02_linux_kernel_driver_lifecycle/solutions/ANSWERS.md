# Resposta - KMOD-SOURCE-REVIEW-03

- `chris_init()` chama `misc_register(&chris_dev)` e registra o miscdevice.
- `chris_exit()` chama `misc_deregister(&chris_dev)` e desfaz o registro.
- A simetria evita deixar recurso/registro vivo após descarregar o módulo e facilita raciocinar sobre ownership e cleanup.
