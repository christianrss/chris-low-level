# .NET/C# + CLR e Node.js/TypeScript + JavaScript Runtime — diretivas permanentes

As quatro faixas são paralelas e não substitutas:

1. **.NET/C# sênior de produção** — C# moderno, ASP.NET Core/Kestrel, data, concorrência, performance, diagnóstico, observabilidade, testes, arquitetura e operação.
2. **CLR/.NET internals from scratch** — PE/CLI, metadata, CIL, VM, compiler C#, CLR-lite, GC, JIT/tiered JIT/AOT, reflection, async runtime, profiler/debugger/heap viewer.
3. **Node.js/TypeScript sênior de produção** — Node core, streams/backpressure, buffers, HTTP/networking, worker threads, data, performance, diagnóstico, observabilidade, segurança e operação.
4. **JavaScript runtime from scratch** — lexer/parser/AST/bytecode/VM, GC, shapes, inline caches, type feedback, JIT/SSA, guards/deoptimization, event loop/libuv-lite, native addons e inspector/profiler.

## Projetos black-magic transversais
`chris-time-travel-debugger`, `chris-replay`, `chris-mixed-debugger`, `chris-runtime-visualizer`, `chris-jit-explorer`, `chris-runtime-patcher`, `chris-object-layout`.

## Integração de longo prazo
```text
C# -> chris-csharp-compiler -> CIL -> chris-clr-lite -> chris-dotnet-jit -> x86-64 -> chris-os
JS -> chris-js -> bytecode -> chris-js-vm -> chris-js-jit -> x86-64 -> chris-os
Node-like -> chris-js-vm -> chris-event-loop/libuv-lite -> chris-os sockets/TCP-IP -> drivers
```

## Regra de senioridade
Internals não substituem experiência de produção. Toda semana deve conter arquitetura, dados, testes, observabilidade, performance, debugging, segurança, deployment e incident analysis em .NET e Node, além da construção dos runtimes próprios.
