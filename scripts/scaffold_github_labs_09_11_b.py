#!/usr/bin/env python3
"""Scaffold GitHub labs for days 10–11 + refresh day infra for 09–11."""
from __future__ import annotations

import re
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# reuse helpers by importing from first script
import importlib.util
spec = importlib.util.spec_from_file_location("s9", ROOT / "scripts" / "scaffold_github_labs_09_11.py")
s9 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(s9)
W, pedagogy, py_mod = s9.W, s9.pedagogy, s9.py_mod


def day10():
    day = "2026-09-10"

    py_mod(day, "systems", "aba_tagged_freelist",
           ["D8-ABA-PUSH", "D8-ABA-POP", "D8-ABA-TAG"],
           "Freelist com tag anti-ABA (indice|tag).",
           '''class TaggedFreelist:
    def __init__(self, n):
        self.nodes = [{"next": i+1, "tag": 0} for i in range(n)]
        self.nodes[-1]["next"] = None
        self.head = 0  # index
        self.head_tag = 0
    def push(self, idx):
        # TODO [D8-ABA-PUSH]
        raise NotImplementedError("D8-ABA-PUSH")
    def pop(self):
        # TODO [D8-ABA-POP]
        raise NotImplementedError("D8-ABA-POP")
    def pack(self, idx, tag):
        # TODO [D8-ABA-TAG]
        raise NotImplementedError("D8-ABA-TAG")
''',
           '''class TaggedFreelist:
    def __init__(self, n):
        self.nodes = [{"next": i+1, "tag": 0} for i in range(n)]
        self.nodes[-1]["next"] = None
        self.head = 0
        self.head_tag = 0
    def pack(self, idx, tag):
        # PEDAGOGY-SOLUTION: D8-ABA-TAG
        return (idx & 0xFFFF) | ((tag & 0xFFFF) << 16)
    def push(self, idx):
        # PEDAGOGY-SOLUTION: D8-ABA-PUSH
        self.nodes[idx]["next"] = self.head
        self.nodes[idx]["tag"] = self.head_tag
        self.head = idx
        self.head_tag = (self.head_tag + 1) & 0xFFFF
    def pop(self):
        # PEDAGOGY-SOLUTION: D8-ABA-POP
        if self.head is None:
            return None
        idx = self.head
        nxt = self.nodes[idx]["next"]
        self.head = nxt
        self.head_tag = (self.head_tag + 1) & 0xFFFF
        return idx
''',
           '''from aba_tagged_freelist import TaggedFreelist

def test_tag():
    # PEDAGOGY-TEST: D8-ABA-TAG
    f = TaggedFreelist(4)
    assert f.pack(3, 1) == (3 | (1 << 16))

def test_push_pop():
    # PEDAGOGY-TEST: D8-ABA-PUSH
    # PEDAGOGY-TEST: D8-ABA-POP
    f = TaggedFreelist(3)
    a = f.pop(); b = f.pop()
    f.push(a)
    assert f.pop() == a
''',
           {"D8-ABA-PUSH": ("starter/aba_tagged_freelist.py", "push"),
            "D8-ABA-POP": ("starter/aba_tagged_freelist.py", "pop"),
            "D8-ABA-TAG": ("starter/aba_tagged_freelist.py", "pack")},
           {"D8-ABA-TAG": "return (idx&0xFFFF)|((tag&0xFFFF)<<16)",
            "D8-ABA-PUSH": "link idx to head; bump head_tag",
            "D8-ABA-POP": "return head; advance"})

    py_mod(day, "ai", "tiled_attention_online_softmax",
           ["D8-ATT-TILE", "D8-ATT-ONLINE", "D8-ATT-OUT"],
           "Online softmax por tile: m,l atualizados; saida normalizada.",
           '''import math

def online_softmax_update(m, l, tile):
    # TODO [D8-ATT-TILE]
    # TODO [D8-ATT-ONLINE]
    raise NotImplementedError("D8-ATT-TILE")

def finalize(m, l, weighted_sum):
    # TODO [D8-ATT-OUT]
    raise NotImplementedError("D8-ATT-OUT")
''',
           '''import math

def online_softmax_update(m, l, tile):
    # PEDAGOGY-SOLUTION: D8-ATT-TILE
    # PEDAGOGY-SOLUTION: D8-ATT-ONLINE
    if not tile:
        return m, l
    tm = max(tile)
    nm = tm if m is None else max(m, tm)
    nl = 0.0
    if m is not None:
        nl = l * math.exp(m - nm)
    for x in tile:
        nl += math.exp(x - nm)
    return nm, nl

def finalize(m, l, weighted_sum):
    # PEDAGOGY-SOLUTION: D8-ATT-OUT
    if l == 0:
        return 0.0
    return weighted_sum / l
''',
           '''from tiled_attention_online_softmax import online_softmax_update, finalize
import math

def test_online():
    # PEDAGOGY-TEST: D8-ATT-TILE
    # PEDAGOGY-TEST: D8-ATT-ONLINE
    m, l = online_softmax_update(None, 0.0, [1.0, 2.0, 3.0])
    assert abs(m - 3.0) < 1e-9
    assert abs(l - (math.exp(-2)+math.exp(-1)+1.0)) < 1e-9

def test_out():
    # PEDAGOGY-TEST: D8-ATT-OUT
    assert abs(finalize(0.0, 2.0, 4.0) - 2.0) < 1e-9
''',
           {"D8-ATT-TILE": ("starter/tiled_attention_online_softmax.py", "online_softmax_update"),
            "D8-ATT-ONLINE": ("starter/tiled_attention_online_softmax.py", "online_softmax_update"),
            "D8-ATT-OUT": ("starter/tiled_attention_online_softmax.py", "finalize")},
           {"D8-ATT-TILE": "tm=max(tile); nm=max(m,tm)",
            "D8-ATT-ONLINE": "l *= exp(m-nm); sum exp(x-nm)",
            "D8-ATT-OUT": "return weighted_sum/l"})

    py_mod(day, "architecture", "tlb_page_walk",
           ["D8-TLB-LOOKUP", "D8-TLB-WALK", "D8-TLB-FILL"],
           "TLB hit ou page-walk + fill.",
           '''PAGE = 4096

class TLB:
    def __init__(self):
        self.entries = {}
    def lookup(self, vaddr):
        # TODO [D8-TLB-LOOKUP]
        raise NotImplementedError("D8-TLB-LOOKUP")
    def walk(self, vaddr, page_table):
        # TODO [D8-TLB-WALK]
        raise NotImplementedError("D8-TLB-WALK")
    def fill(self, vpn, pfn):
        # TODO [D8-TLB-FILL]
        raise NotImplementedError("D8-TLB-FILL")
''',
           '''PAGE = 4096

class TLB:
    def __init__(self):
        self.entries = {}
    def lookup(self, vaddr):
        # PEDAGOGY-SOLUTION: D8-TLB-LOOKUP
        vpn = vaddr // PAGE
        return self.entries.get(vpn)
    def walk(self, vaddr, page_table):
        # PEDAGOGY-SOLUTION: D8-TLB-WALK
        vpn = vaddr // PAGE
        if vpn not in page_table:
            raise KeyError("fault")
        return page_table[vpn]
    def fill(self, vpn, pfn):
        # PEDAGOGY-SOLUTION: D8-TLB-FILL
        self.entries[vpn] = pfn
''',
           '''from tlb_page_walk import TLB, PAGE

def test_lookup_fill():
    # PEDAGOGY-TEST: D8-TLB-LOOKUP
    # PEDAGOGY-TEST: D8-TLB-FILL
    t = TLB()
    assert t.lookup(0) is None
    t.fill(0, 7)
    assert t.lookup(100) == 7

def test_walk():
    # PEDAGOGY-TEST: D8-TLB-WALK
    t = TLB()
    assert t.walk(PAGE + 3, {1: 9}) == 9
''',
           {"D8-TLB-LOOKUP": ("starter/tlb_page_walk.py", "lookup"),
            "D8-TLB-WALK": ("starter/tlb_page_walk.py", "walk"),
            "D8-TLB-FILL": ("starter/tlb_page_walk.py", "fill")},
           {"D8-TLB-LOOKUP": "return entries.get(vaddr//PAGE)",
            "D8-TLB-WALK": "return page_table[vpn]",
            "D8-TLB-FILL": "entries[vpn]=pfn"})

    py_mod(day, "parsers", "backtracking_regex_vm",
           ["D8-RE-CHAR", "D8-RE-STAR", "D8-RE-MATCH"],
           "VM regex backtracking: CHAR, STAR, MATCH.",
           '''def match(code, text):
    # TODO [D8-RE-CHAR]
    # TODO [D8-RE-STAR]
    # TODO [D8-RE-MATCH]
    raise NotImplementedError("D8-RE-MATCH")
''',
           '''def match(code, text):
    # PEDAGOGY-SOLUTION: D8-RE-MATCH
    def run(pc, i):
        if pc >= len(code):
            return i == len(text)
        op = code[pc]
        # PEDAGOGY-SOLUTION: D8-RE-CHAR
        if op[0] == "CHAR":
            if i < len(text) and text[i] == op[1]:
                return run(pc + 1, i + 1)
            return False
        # PEDAGOGY-SOLUTION: D8-RE-STAR
        if op[0] == "STAR":
            # greedy then backtrack
            j = i
            ch = op[1]
            while j < len(text) and text[j] == ch:
                j += 1
            while j >= i:
                if run(pc + 1, j):
                    return True
                j -= 1
            return False
        if op[0] == "MATCH":
            return i == len(text)
        return False
    return run(0, 0)
''',
           '''from backtracking_regex_vm import match

def test_char_match():
    # PEDAGOGY-TEST: D8-RE-CHAR
    # PEDAGOGY-TEST: D8-RE-MATCH
    assert match([("CHAR", "a"), ("MATCH",)], "a")
    assert not match([("CHAR", "a"), ("MATCH",)], "b")

def test_star():
    # PEDAGOGY-TEST: D8-RE-STAR
    assert match([("STAR", "a"), ("CHAR", "b"), ("MATCH",)], "aaab")
''',
           {"D8-RE-CHAR": ("starter/backtracking_regex_vm.py", "match"),
            "D8-RE-STAR": ("starter/backtracking_regex_vm.py", "match"),
            "D8-RE-MATCH": ("starter/backtracking_regex_vm.py", "match")},
           {"D8-RE-CHAR": "if text[i]==op[1]: recurse",
            "D8-RE-STAR": "greedy then backtrack",
            "D8-RE-MATCH": "i==len(text)"})

    # port remaining day10 from projects when possible
    py_mod(day, "agent", "transactional_patcher",
           ["D8-PATCH-BEGIN", "D8-PATCH-APPLY", "D8-PATCH-COMMIT"],
           "Patch transacional: begin snapshot, apply, commit/rollback.",
           '''class Patcher:
    def __init__(self, text):
        self.text = text
        self.snap = None
    def begin(self):
        # TODO [D8-PATCH-BEGIN]
        raise NotImplementedError("D8-PATCH-BEGIN")
    def apply(self, start, end, repl):
        # TODO [D8-PATCH-APPLY]
        raise NotImplementedError("D8-PATCH-APPLY")
    def commit(self):
        # TODO [D8-PATCH-COMMIT]
        raise NotImplementedError("D8-PATCH-COMMIT")
    def rollback(self):
        if self.snap is None:
            raise RuntimeError("no tx")
        self.text = self.snap
        self.snap = None
''',
           '''class Patcher:
    def __init__(self, text):
        self.text = text
        self.snap = None
    def begin(self):
        # PEDAGOGY-SOLUTION: D8-PATCH-BEGIN
        self.snap = self.text
    def apply(self, start, end, repl):
        # PEDAGOGY-SOLUTION: D8-PATCH-APPLY
        if self.snap is None:
            raise RuntimeError("no tx")
        self.text = self.text[:start] + repl + self.text[end:]
    def commit(self):
        # PEDAGOGY-SOLUTION: D8-PATCH-COMMIT
        if self.snap is None:
            raise RuntimeError("no tx")
        self.snap = None
    def rollback(self):
        if self.snap is None:
            raise RuntimeError("no tx")
        self.text = self.snap
        self.snap = None
''',
           '''from transactional_patcher import Patcher

def test_tx():
    # PEDAGOGY-TEST: D8-PATCH-BEGIN
    # PEDAGOGY-TEST: D8-PATCH-APPLY
    # PEDAGOGY-TEST: D8-PATCH-COMMIT
    p = Patcher("abcdef")
    p.begin()
    p.apply(2, 4, "ZZ")
    assert p.text == "abZZef"
    p.commit()
    assert p.snap is None
''',
           {"D8-PATCH-BEGIN": ("starter/transactional_patcher.py", "begin"),
            "D8-PATCH-APPLY": ("starter/transactional_patcher.py", "apply"),
            "D8-PATCH-COMMIT": ("starter/transactional_patcher.py", "commit")},
           {"D8-PATCH-BEGIN": "self.snap=self.text",
            "D8-PATCH-APPLY": "splice repl",
            "D8-PATCH-COMMIT": "self.snap=None"})

    # if project transactional exists, prefer it if compatible - skip

    py_mod(day, "redteam", "elf64_relocation_triage",
           ["D8-ELF-MAGIC", "D8-ELF-CLASS", "D8-ELF-RELOC"],
           "Triagem ELF64: magic, class 2, contagem de relocs sintetica.",
           '''def triage(data: bytes):
    # TODO [D8-ELF-MAGIC]
    # TODO [D8-ELF-CLASS]
    # TODO [D8-ELF-RELOC]
    raise NotImplementedError("D8-ELF-MAGIC")
''',
           '''def triage(data: bytes):
    # PEDAGOGY-SOLUTION: D8-ELF-MAGIC
    if data[:4] != b"\\x7fELF":
        return {"ok": False, "reason": "magic"}
    # PEDAGOGY-SOLUTION: D8-ELF-CLASS
    if len(data) < 5 or data[4] != 2:
        return {"ok": False, "reason": "class"}
    # PEDAGOGY-SOLUTION: D8-ELF-RELOC
    # synthetic: byte 5 = reloc count
    n = data[5] if len(data) > 5 else 0
    return {"ok": True, "class": 64, "relocs": n}
''',
           '''from elf64_relocation_triage import triage

def test_elf():
    # PEDAGOGY-TEST: D8-ELF-MAGIC
    # PEDAGOGY-TEST: D8-ELF-CLASS
    # PEDAGOGY-TEST: D8-ELF-RELOC
    blob = b"\\x7fELF" + bytes([2, 3])
    r = triage(blob)
    assert r["ok"] and r["relocs"] == 3
    assert triage(b"MZ")["ok"] is False
''',
           {"D8-ELF-MAGIC": ("starter/elf64_relocation_triage.py", "triage"),
            "D8-ELF-CLASS": ("starter/elf64_relocation_triage.py", "triage"),
            "D8-ELF-RELOC": ("starter/elf64_relocation_triage.py", "triage")},
           {"D8-ELF-MAGIC": "data[:4]==\\\\x7fELF",
            "D8-ELF-CLASS": "data[4]==2",
            "D8-ELF-RELOC": "relocs=data[5]"})

    # descriptor binding - from project
    src = (ROOT / "projects/chris-renderer-vulkan/descriptor_binding_model.py").read_text(encoding="utf-8") if (ROOT / "projects/chris-renderer-vulkan/descriptor_binding_model.py").exists() else None
    if src and "PEDAGOGY-SOLUTION" in src:
        # extract and wrap
        py_mod(day, "graphics", "descriptor_binding_model",
               ["D8-GFX-BIND", "D8-GFX-SET", "D8-GFX-LAYOUT"],
               "Modelo de descriptor set/binding (headless).",
               '''def bind(layout, set_id, binding, resource):
    # TODO [D8-GFX-BIND]
    raise NotImplementedError("D8-GFX-BIND")

def validate_set(layout, set_id, table):
    # TODO [D8-GFX-SET]
    raise NotImplementedError("D8-GFX-SET")

def layout_of(*bindings):
    # TODO [D8-GFX-LAYOUT]
    raise NotImplementedError("D8-GFX-LAYOUT")
''',
               '''def layout_of(*bindings):
    # PEDAGOGY-SOLUTION: D8-GFX-LAYOUT
    return {"bindings": list(bindings)}

def bind(layout, set_id, binding, resource):
    # PEDAGOGY-SOLUTION: D8-GFX-BIND
    if binding not in layout["bindings"]:
        raise KeyError(binding)
    return {"set": set_id, "binding": binding, "resource": resource}

def validate_set(layout, set_id, table):
    # PEDAGOGY-SOLUTION: D8-GFX-SET
    for b in layout["bindings"]:
        if b not in table:
            raise KeyError(f"missing {b}")
    return True
''',
               '''from descriptor_binding_model import layout_of, bind, validate_set

def test_desc():
    # PEDAGOGY-TEST: D8-GFX-LAYOUT
    # PEDAGOGY-TEST: D8-GFX-BIND
    # PEDAGOGY-TEST: D8-GFX-SET
    lay = layout_of(0, 1)
    e = bind(lay, 0, 0, "tex")
    assert e["resource"] == "tex"
    assert validate_set(lay, 0, {0: "a", 1: "b"}) is True
''',
               {"D8-GFX-LAYOUT": ("starter/descriptor_binding_model.py", "layout_of"),
                "D8-GFX-BIND": ("starter/descriptor_binding_model.py", "bind"),
                "D8-GFX-SET": ("starter/descriptor_binding_model.py", "validate_set")},
               {"D8-GFX-LAYOUT": "return {bindings:list}",
                "D8-GFX-BIND": "check binding in layout",
                "D8-GFX-SET": "all bindings present"})
        W(ROOT / f"days/{day}/graphics/descriptor_binding_model/docs/COMPARISON.md",
          """# COMPARISON — descriptor_binding_model

| Aspecto | CPU/software | OpenGL | Vulkan/D3D12 |
|---------|--------------|--------|--------------|
| Binding | dict | uniform locations | descriptor sets |

Headless exempt.
""")
    else:
        # still create minimal - already in if branch with invented code; fix else
        pass

    # reinvent if project didn't have markers - the if created it; if not exists create:
    if not (ROOT / f"days/{day}/graphics/descriptor_binding_model/solutions").exists():
        pass  # created above in if - actually if src without PEDAGOGY we skip. Force create:
    
    # Always ensure descriptor module exists with invented code
    if not (ROOT / f"days/{day}/graphics/descriptor_binding_model/starter").exists():
        py_mod(day, "graphics", "descriptor_binding_model",
               ["D8-GFX-BIND", "D8-GFX-SET", "D8-GFX-LAYOUT"],
               "Modelo de descriptor set/binding (headless).",
               '''def layout_of(*bindings):
    # TODO [D8-GFX-LAYOUT]
    raise NotImplementedError
def bind(layout, set_id, binding, resource):
    # TODO [D8-GFX-BIND]
    raise NotImplementedError
def validate_set(layout, set_id, table):
    # TODO [D8-GFX-SET]
    raise NotImplementedError
''',
               '''def layout_of(*bindings):
    # PEDAGOGY-SOLUTION: D8-GFX-LAYOUT
    return {"bindings": list(bindings)}
def bind(layout, set_id, binding, resource):
    # PEDAGOGY-SOLUTION: D8-GFX-BIND
    if binding not in layout["bindings"]:
        raise KeyError(binding)
    return {"set": set_id, "binding": binding, "resource": resource}
def validate_set(layout, set_id, table):
    # PEDAGOGY-SOLUTION: D8-GFX-SET
    for b in layout["bindings"]:
        if b not in table:
            raise KeyError(b)
    return True
''',
               '''from descriptor_binding_model import layout_of, bind, validate_set
def test_desc():
    # PEDAGOGY-TEST: D8-GFX-LAYOUT
    # PEDAGOGY-TEST: D8-GFX-BIND
    # PEDAGOGY-TEST: D8-GFX-SET
    lay = layout_of(0, 1)
    assert bind(lay, 0, 0, "tex")["resource"] == "tex"
    assert validate_set(lay, 0, {0: "a", 1: "b"}) is True
''',
               {"D8-GFX-LAYOUT": ("starter/descriptor_binding_model.py", "layout_of"),
                "D8-GFX-BIND": ("starter/descriptor_binding_model.py", "bind"),
                "D8-GFX-SET": ("starter/descriptor_binding_model.py", "validate_set")},
               {"D8-GFX-LAYOUT": "return bindings", "D8-GFX-BIND": "check", "D8-GFX-SET": "all present"})
        W(ROOT / f"days/{day}/graphics/descriptor_binding_model/docs/COMPARISON.md",
          "# COMPARISON\\n\\n| Aspecto | CPU/software | OpenGL | Vulkan |\\n|---|---|---|---|\\n| Binding | dict | locations | sets |\\n")

    # linux procfs module lab - python sim
    py_mod(day, "linux", "procfs_module_lab",
           ["D8-PROC-LIST", "D8-PROC-READ", "D8-PROC-WRITE"],
           "Simulacao procfs: list/read/write de entradas.",
           '''class ProcFS:
    def __init__(self):
        self.entries = {}
    def write(self, name, data):
        # TODO [D8-PROC-WRITE]
        raise NotImplementedError
    def read(self, name):
        # TODO [D8-PROC-READ]
        raise NotImplementedError
    def list(self):
        # TODO [D8-PROC-LIST]
        raise NotImplementedError
''',
           '''class ProcFS:
    def __init__(self):
        self.entries = {}
    def write(self, name, data):
        # PEDAGOGY-SOLUTION: D8-PROC-WRITE
        self.entries[name] = str(data)
    def read(self, name):
        # PEDAGOGY-SOLUTION: D8-PROC-READ
        if name not in self.entries:
            raise KeyError(name)
        return self.entries[name]
    def list(self):
        # PEDAGOGY-SOLUTION: D8-PROC-LIST
        return sorted(self.entries)
''',
           '''from procfs_module_lab import ProcFS
def test_proc():
    # PEDAGOGY-TEST: D8-PROC-WRITE
    # PEDAGOGY-TEST: D8-PROC-READ
    # PEDAGOGY-TEST: D8-PROC-LIST
    p = ProcFS(); p.write("stats", "1"); assert p.read("stats")=="1"; assert p.list()==["stats"]
''',
           {"D8-PROC-WRITE": ("starter/procfs_module_lab.py", "write"),
            "D8-PROC-READ": ("starter/procfs_module_lab.py", "read"),
            "D8-PROC-LIST": ("starter/procfs_module_lab.py", "list")},
           {"D8-PROC-WRITE": "entries[name]=str(data)", "D8-PROC-READ": "return entries[name]", "D8-PROC-LIST": "return sorted(entries)"})

    # node message channel
    mod = ROOT / "days" / day / "nodejs" / "message_channel_rpc"
    W(mod / "starter" / "rpc.js", ''''use strict';
function createPair() {
  // TODO [D8-NODE-PAIR]
  throw new Error('D8-NODE-PAIR');
}
function request(port, method, args) {
  // TODO [D8-NODE-REQ]
  throw new Error('D8-NODE-REQ');
}
function serve(port, handlers) {
  // TODO [D8-NODE-SERVE]
  throw new Error('D8-NODE-SERVE');
}
module.exports = { createPair, request, serve };
''')
    W(mod / "solutions" / "rpc.js", ''''use strict';
const { MessageChannel } = require('worker_threads');
function createPair() {
  // PEDAGOGY-SOLUTION: D8-NODE-PAIR
  const { port1, port2 } = new MessageChannel();
  return { client: port1, server: port2 };
}
function request(port, method, args) {
  // PEDAGOGY-SOLUTION: D8-NODE-REQ
  return new Promise((resolve, reject) => {
    const onMsg = (msg) => {
      port.off('message', onMsg);
      if (msg.error) reject(new Error(msg.error));
      else resolve(msg.result);
    };
    port.on('message', onMsg);
    port.postMessage({ method, args });
  });
}
function serve(port, handlers) {
  // PEDAGOGY-SOLUTION: D8-NODE-SERVE
  port.on('message', (msg) => {
    try {
      const fn = handlers[msg.method];
      if (!fn) throw new Error('unknown');
      const result = fn(...(msg.args || []));
      port.postMessage({ result });
    } catch (e) {
      port.postMessage({ error: String(e.message || e) });
    }
  });
}
module.exports = { createPair, request, serve };
''')
    W(mod / "starter" / "test.js", ''''use strict';
const assert = require('assert');
const { createPair, request, serve } = require('./rpc');
(async () => {
  // PEDAGOGY-TEST: D8-NODE-PAIR
  // PEDAGOGY-TEST: D8-NODE-SERVE
  // PEDAGOGY-TEST: D8-NODE-REQ
  const { client, server } = createPair();
  serve(server, { add: (a, b) => a + b });
  const r = await request(client, 'add', [2, 3]);
  assert.strictEqual(r, 5);
  console.log('ok');
  client.close(); server.close();
})();
''')
    W(mod / "solutions" / "test.js", (mod / "starter" / "test.js").read_text(encoding="utf-8"))
    W(mod / "starter" / "package.json", '{"name":"message-channel-rpc","private":true}\\n')
    W(mod / "solutions" / "package.json", '{"name":"message-channel-rpc","private":true}\\n')
    pedagogy(mod, "message_channel_rpc", "javascript",
             ["D8-NODE-PAIR", "D8-NODE-REQ", "D8-NODE-SERVE"],
             "RPC via MessageChannel ports.",
             f"cd days/{day}/nodejs/message_channel_rpc/starter\\nnode test.js",
             {"D8-NODE-PAIR": ("starter/rpc.js", "createPair"),
              "D8-NODE-REQ": ("starter/rpc.js", "request"),
              "D8-NODE-SERVE": ("starter/rpc.js", "serve")},
             {"D8-NODE-PAIR": "new MessageChannel()", "D8-NODE-REQ": "Promise postMessage", "D8-NODE-SERVE": "handlers[method]"})

    # dotnet pinned memory
    mod = ROOT / "days" / day / "dotnet" / "pinned_memory_probe"
    W(mod / "starter" / "Pinned.cs", '''namespace Chris.PinnedLab;
public static class Pinned {
    public static int SumPinned(byte[] data) {
        // TODO [D8-DN-PIN]
        // TODO [D8-DN-LEN]
        // TODO [D8-DN-SUM]
        throw new NotImplementedException();
    }
}
''')
    W(mod / "solutions" / "Pinned.cs", '''using System.Runtime.InteropServices;
namespace Chris.PinnedLab;
public static class Pinned {
    public static int SumPinned(byte[] data) {
        // PEDAGOGY-SOLUTION: D8-DN-PIN
        var handle = GCHandle.Alloc(data, GCHandleType.Pinned);
        try {
            // PEDAGOGY-SOLUTION: D8-DN-LEN
            int n = data.Length;
            // PEDAGOGY-SOLUTION: D8-DN-SUM
            int s = 0;
            for (int i = 0; i < n; i++) s += data[i];
            return s;
        } finally {
            handle.Free();
        }
    }
}
''')
    for base in (mod / "starter", mod / "solutions"):
        W(base / "Chris.PinnedLab.csproj", '''<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup><TargetFramework>net8.0</TargetFramework><ImplicitUsings>enable</ImplicitUsings><Nullable>enable</Nullable></PropertyGroup>
  <ItemGroup><Compile Remove="tests/**" /></ItemGroup>
</Project>
''')
        W(base / "tests" / "Chris.PinnedLab.Tests.csproj", '''<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup><TargetFramework>net8.0</TargetFramework><IsTestProject>true</IsTestProject></PropertyGroup>
  <ItemGroup>
    <PackageReference Include="Microsoft.NET.Test.Sdk" Version="17.11.1" />
    <PackageReference Include="xunit" Version="2.9.2" />
    <PackageReference Include="xunit.runner.visualstudio" Version="2.8.2" />
  </ItemGroup>
  <ItemGroup><ProjectReference Include="..\\Chris.PinnedLab.csproj" /></ItemGroup>
</Project>
''')
        W(base / "tests" / "PinnedTests.cs", '''using Chris.PinnedLab;
using Xunit;
public class PinnedTests {
    [Fact]
    public void Sum() {
        // PEDAGOGY-TEST: D8-DN-PIN
        // PEDAGOGY-TEST: D8-DN-LEN
        // PEDAGOGY-TEST: D8-DN-SUM
        Assert.Equal(6, Pinned.SumPinned(new byte[]{1,2,3}));
    }
}
''')
    pedagogy(mod, "pinned_memory_probe", "csharp",
             ["D8-DN-PIN", "D8-DN-LEN", "D8-DN-SUM"],
             "GCHandle.Pinned + soma de bytes.",
             f"cd days/{day}/dotnet/pinned_memory_probe/starter\\ndotnet test tests/Chris.PinnedLab.Tests.csproj",
             {"D8-DN-PIN": ("starter/Pinned.cs", "SumPinned"),
              "D8-DN-LEN": ("starter/Pinned.cs", "SumPinned"),
              "D8-DN-SUM": ("starter/Pinned.cs", "SumPinned")},
             {"D8-DN-PIN": "GCHandle.Alloc Pinned", "D8-DN-LEN": "n=data.Length", "D8-DN-SUM": "sum bytes"})

    print("day10 done")


def day11():
    day = "2026-09-11"

    py_mod(day, "systems", "hazard_pointer_stack",
           ["D9-HP-PUSH", "D9-HP-POP", "D9-HP-PROTECT"],
           "Stack com hazard pointer educacional (protect antes de deref).",
           '''class HPStack:
    def __init__(self):
        self.head = None
        self.hazard = None
    def protect(self, node):
        # TODO [D9-HP-PROTECT]
        raise NotImplementedError
    def push(self, value):
        # TODO [D9-HP-PUSH]
        raise NotImplementedError
    def pop(self):
        # TODO [D9-HP-POP]
        raise NotImplementedError
''',
           '''class HPStack:
    def __init__(self):
        self.head = None
        self.hazard = None
    def protect(self, node):
        # PEDAGOGY-SOLUTION: D9-HP-PROTECT
        self.hazard = node
        return node
    def push(self, value):
        # PEDAGOGY-SOLUTION: D9-HP-PUSH
        node = {"value": value, "next": self.head}
        self.head = node
    def pop(self):
        # PEDAGOGY-SOLUTION: D9-HP-POP
        node = self.protect(self.head)
        if node is None:
            return None
        self.head = node["next"]
        if self.hazard is node:
            self.hazard = None
        return node["value"]
''',
           '''from hazard_pointer_stack import HPStack
def test_hp():
    # PEDAGOGY-TEST: D9-HP-PROTECT
    # PEDAGOGY-TEST: D9-HP-PUSH
    # PEDAGOGY-TEST: D9-HP-POP
    s = HPStack(); s.push(1); s.push(2)
    assert s.pop() == 2 and s.pop() == 1 and s.pop() is None
''',
           {"D9-HP-PROTECT": ("starter/hazard_pointer_stack.py", "protect"),
            "D9-HP-PUSH": ("starter/hazard_pointer_stack.py", "push"),
            "D9-HP-POP": ("starter/hazard_pointer_stack.py", "pop")},
           {"D9-HP-PROTECT": "self.hazard=node", "D9-HP-PUSH": "link node", "D9-HP-POP": "protect then advance"})

    py_mod(day, "ai", "kv_cache_ring",
           ["D9-KV-WRITE", "D9-KV-READ", "D9-KV-WINDOW"],
           "KV-cache circular com janela deslizante.",
           '''class KVRing:
    def __init__(self, cap):
        self.cap = cap
        self.buf = [None] * cap
        self.pos = 0
        self.count = 0
    def write(self, item):
        # TODO [D9-KV-WRITE]
        raise NotImplementedError
    def read(self, i):
        # TODO [D9-KV-READ]
        raise NotImplementedError
    def window(self):
        # TODO [D9-KV-WINDOW]
        raise NotImplementedError
''',
           '''class KVRing:
    def __init__(self, cap):
        self.cap = cap
        self.buf = [None] * cap
        self.pos = 0
        self.count = 0
    def write(self, item):
        # PEDAGOGY-SOLUTION: D9-KV-WRITE
        self.buf[self.pos] = item
        self.pos = (self.pos + 1) % self.cap
        self.count = min(self.cap, self.count + 1)
    def read(self, i):
        # PEDAGOGY-SOLUTION: D9-KV-READ
        if i < 0 or i >= self.count:
            raise IndexError(i)
        start = (self.pos - self.count) % self.cap
        return self.buf[(start + i) % self.cap]
    def window(self):
        # PEDAGOGY-SOLUTION: D9-KV-WINDOW
        return [self.read(i) for i in range(self.count)]
''',
           '''from kv_cache_ring import KVRing
def test_kv():
    # PEDAGOGY-TEST: D9-KV-WRITE
    # PEDAGOGY-TEST: D9-KV-READ
    # PEDAGOGY-TEST: D9-KV-WINDOW
    r = KVRing(3)
    r.write("a"); r.write("b"); r.write("c"); r.write("d")
    assert r.window() == ["b", "c", "d"]
    assert r.read(0) == "b"
''',
           {"D9-KV-WRITE": ("starter/kv_cache_ring.py", "write"),
            "D9-KV-READ": ("starter/kv_cache_ring.py", "read"),
            "D9-KV-WINDOW": ("starter/kv_cache_ring.py", "window")},
           {"D9-KV-WRITE": "circular overwrite", "D9-KV-READ": "index from start", "D9-KV-WINDOW": "list read"})

    # dwarf from project
    W(ROOT / f"days/{day}/redteam/dwarf_line_program/solutions/dwarf_line_program.py",
      (ROOT / "projects/chris-binary-toolkit/dwarf_line_subset.py").read_text(encoding="utf-8"))
    W(ROOT / f"days/{day}/redteam/dwarf_line_program/starter/dwarf_line_program.py", '''def read_uleb(data, off):
    # TODO [D9-DWARF-ULEB]
    raise NotImplementedError
def read_sleb(data, off):
    # TODO [D9-DWARF-SLEB]
    raise NotImplementedError
def run_line_program(data):
    # TODO [D9-DWARF-VM]
    raise NotImplementedError
''')
    W(ROOT / f"days/{day}/redteam/dwarf_line_program/starter/test_dwarf_line_program.py", '''from dwarf_line_program import read_uleb, read_sleb, run_line_program

def test_uleb_sleb():
    # PEDAGOGY-TEST: D9-DWARF-ULEB
    # PEDAGOGY-TEST: D9-DWARF-SLEB
    v, o = read_uleb(bytes([0x80, 0x01]), 0)
    assert v == 128 and o == 2
    v, o = read_sleb(bytes([0x7f]), 0)
    assert v == -1

def test_vm():
    # PEDAGOGY-TEST: D9-DWARF-VM
    # op1 uleb2, op2 sleb+1, op4 row, op0 end
    prog = bytes([1, 2, 2, 1, 4, 0])
    rows = run_line_program(prog)
    assert rows == [(2, 1, 2)]
''')
    W(ROOT / f"days/{day}/redteam/dwarf_line_program/solutions/test_dwarf_line_program.py",
      (ROOT / f"days/{day}/redteam/dwarf_line_program/starter/test_dwarf_line_program.py").read_text(encoding="utf-8"))
    pedagogy(ROOT / f"days/{day}/redteam/dwarf_line_program", "dwarf_line_program", "python",
             ["D9-DWARF-ULEB", "D9-DWARF-SLEB", "D9-DWARF-VM"],
             "DWARF line program subset: ULEB/SLEB + VM.",
             f"cd days/{day}/redteam/dwarf_line_program/starter\\npython test_dwarf_line_program.py",
             {"D9-DWARF-ULEB": ("starter/dwarf_line_program.py", "read_uleb"),
              "D9-DWARF-SLEB": ("starter/dwarf_line_program.py", "read_sleb"),
              "D9-DWARF-VM": ("starter/dwarf_line_program.py", "run_line_program")},
             {"D9-DWARF-ULEB": "value|=(b&0x7f)<<shift", "D9-DWARF-SLEB": "sign extend", "D9-DWARF-VM": "ops 0..4"})

    # pike from project
    W(ROOT / f"days/{day}/parsers/pike_regex_vm/solutions/pike_regex_vm.py",
      (ROOT / "projects/chris-regex/pike_vm.py").read_text(encoding="utf-8"))
    W(ROOT / f"days/{day}/parsers/pike_regex_vm/starter/pike_regex_vm.py", '''def add_thread(code, pc, out, seen):
    # TODO [D9-PIKE-EPSILON]
    raise NotImplementedError
def run(code, text, trace=False):
    # TODO [D9-PIKE-STEP]
    # TODO [D9-PIKE-TRACE]
    # TODO [D9-PIKE-MATCH]
    raise NotImplementedError
''')
    # pike has 4 todos - adjust starter/ids
    W(ROOT / f"days/{day}/parsers/pike_regex_vm/starter/test_pike_regex_vm.py", '''from pike_regex_vm import run

def test_match():
    # PEDAGOGY-TEST: D9-PIKE-EPSILON
    # PEDAGOGY-TEST: D9-PIKE-STEP
    # PEDAGOGY-TEST: D9-PIKE-MATCH
    code = [("CHAR", "a", 1), ("MATCH",)]
    assert run(code, "a") is True
    assert run(code, "b") is False

def test_trace():
    # PEDAGOGY-TEST: D9-PIKE-TRACE
    code = [("CHAR", "a", 1), ("MATCH",)]
    ok, snap = run(code, "a", trace=True)
    assert ok and len(snap) >= 1
''')
    W(ROOT / f"days/{day}/parsers/pike_regex_vm/solutions/test_pike_regex_vm.py",
      (ROOT / f"days/{day}/parsers/pike_regex_vm/starter/test_pike_regex_vm.py").read_text(encoding="utf-8"))
    pedagogy(ROOT / f"days/{day}/parsers/pike_regex_vm", "pike_regex_vm", "python",
             ["D9-PIKE-EPSILON", "D9-PIKE-STEP", "D9-PIKE-TRACE", "D9-PIKE-MATCH"],
             "Pike VM: epsilon closure + step + match.",
             f"cd days/{day}/parsers/pike_regex_vm/starter\\npython test_pike_regex_vm.py",
             {"D9-PIKE-EPSILON": ("starter/pike_regex_vm.py", "add_thread"),
              "D9-PIKE-STEP": ("starter/pike_regex_vm.py", "run"),
              "D9-PIKE-TRACE": ("starter/pike_regex_vm.py", "run"),
              "D9-PIKE-MATCH": ("starter/pike_regex_vm.py", "run")},
             {"D9-PIKE-EPSILON": "JMP/SPLIT recurse", "D9-PIKE-STEP": "CHAR/ANY advance",
              "D9-PIKE-TRACE": "snap.append", "D9-PIKE-MATCH": "any MATCH in cur"})

    # context budgeter
    W(ROOT / f"days/{day}/agent/context_budgeter/solutions/context_budgeter.py",
      (ROOT / "projects/chris-agent-core/context_budgeter.py").read_text(encoding="utf-8"))
    W(ROOT / f"days/{day}/agent/context_budgeter/starter/context_budgeter.py", '''def base_score(c):
    # TODO [D9-CTX-SCORE]
    raise NotImplementedError
def pack(candidates, budget):
    # TODO [D9-CTX-DEDUPE]
    # TODO [D9-CTX-DIVERSITY]
    # TODO [D9-CTX-BUDGET]
    raise NotImplementedError
''')
    W(ROOT / f"days/{day}/agent/context_budgeter/starter/test_context_budgeter.py", '''from context_budgeter import base_score, pack

def test_score_pack():
    # PEDAGOGY-TEST: D9-CTX-SCORE
    # PEDAGOGY-TEST: D9-CTX-DEDUPE
    # PEDAGOGY-TEST: D9-CTX-DIVERSITY
    # PEDAGOGY-TEST: D9-CTX-BUDGET
    c = {"path": "a.py", "content": "x", "bytes": 1, "lexical": 1, "semantic": 1, "graph": 1}
    assert abs(base_score(c) - 1.0) < 1e-9
    out = pack([c, dict(c)], 10)
    assert len(out["selected"]) == 1
''')
    W(ROOT / f"days/{day}/agent/context_budgeter/solutions/test_context_budgeter.py",
      (ROOT / f"days/{day}/agent/context_budgeter/starter/test_context_budgeter.py").read_text(encoding="utf-8"))
    pedagogy(ROOT / f"days/{day}/agent/context_budgeter", "context_budgeter", "python",
             ["D9-CTX-SCORE", "D9-CTX-DEDUPE", "D9-CTX-DIVERSITY", "D9-CTX-BUDGET"],
             "Context budgeter: score, dedupe, diversity, budget.",
             f"cd days/{day}/agent/context_budgeter/starter\\npython test_context_budgeter.py",
             {"D9-CTX-SCORE": ("starter/context_budgeter.py", "base_score"),
              "D9-CTX-DEDUPE": ("starter/context_budgeter.py", "pack"),
              "D9-CTX-DIVERSITY": ("starter/context_budgeter.py", "pack"),
              "D9-CTX-BUDGET": ("starter/context_budgeter.py", "pack")},
             {"D9-CTX-SCORE": "0.45*lex+...", "D9-CTX-DEDUPE": "sha256",
              "D9-CTX-DIVERSITY": "bonus new path", "D9-CTX-BUDGET": "used+bytes<=budget"})

    py_mod(day, "quantum", "statevector_bitmask",
           ["D9-Q-SET", "D9-Q-GET", "D9-Q-NORM"],
           "Statevector indexado por bitmask; get/set/normalize.",
           '''import math
class SV:
    def __init__(self, nqubits):
        self.n = nqubits
        self.amp = [0.0] * (1 << nqubits)
        self.amp[0] = 1.0
    def set(self, mask, value):
        # TODO [D9-Q-SET]
        raise NotImplementedError
    def get(self, mask):
        # TODO [D9-Q-GET]
        raise NotImplementedError
    def normalize(self):
        # TODO [D9-Q-NORM]
        raise NotImplementedError
''',
           '''import math
class SV:
    def __init__(self, nqubits):
        self.n = nqubits
        self.amp = [0.0] * (1 << nqubits)
        self.amp[0] = 1.0
    def set(self, mask, value):
        # PEDAGOGY-SOLUTION: D9-Q-SET
        self.amp[mask] = value
    def get(self, mask):
        # PEDAGOGY-SOLUTION: D9-Q-GET
        return self.amp[mask]
    def normalize(self):
        # PEDAGOGY-SOLUTION: D9-Q-NORM
        s = math.sqrt(sum(a*a for a in self.amp))
        if s == 0:
            return
        self.amp = [a / s for a in self.amp]
''',
           '''from statevector_bitmask import SV
def test_sv():
    # PEDAGOGY-TEST: D9-Q-SET
    # PEDAGOGY-TEST: D9-Q-GET
    # PEDAGOGY-TEST: D9-Q-NORM
    s = SV(1); s.set(0, 3); s.set(1, 4); s.normalize()
    assert abs(s.get(0) - 0.6) < 1e-9 and abs(s.get(1) - 0.8) < 1e-9
''',
           {"D9-Q-SET": ("starter/statevector_bitmask.py", "set"),
            "D9-Q-GET": ("starter/statevector_bitmask.py", "get"),
            "D9-Q-NORM": ("starter/statevector_bitmask.py", "normalize")},
           {"D9-Q-SET": "amp[mask]=value", "D9-Q-GET": "return amp[mask]", "D9-Q-NORM": "divide by L2"})

    py_mod(day, "network", "length_prefixed_framing",
           ["D9-NET-ENCODE", "D9-NET-DECODE", "D9-NET-FEED"],
           "Framing u32 LE length-prefixed incremental.",
           '''import struct
class Framer:
    def __init__(self):
        self.buf = bytearray()
    def encode(self, payload: bytes) -> bytes:
        # TODO [D9-NET-ENCODE]
        raise NotImplementedError
    def feed(self, data: bytes):
        # TODO [D9-NET-FEED]
        raise NotImplementedError
    def decode_one(self):
        # TODO [D9-NET-DECODE]
        raise NotImplementedError
''',
           '''import struct
class Framer:
    def __init__(self):
        self.buf = bytearray()
    def encode(self, payload: bytes) -> bytes:
        # PEDAGOGY-SOLUTION: D9-NET-ENCODE
        return struct.pack("<I", len(payload)) + payload
    def feed(self, data: bytes):
        # PEDAGOGY-SOLUTION: D9-NET-FEED
        self.buf.extend(data)
    def decode_one(self):
        # PEDAGOGY-SOLUTION: D9-NET-DECODE
        if len(self.buf) < 4:
            return None
        (n,) = struct.unpack_from("<I", self.buf, 0)
        if len(self.buf) < 4 + n:
            return None
        payload = bytes(self.buf[4:4+n])
        del self.buf[:4+n]
        return payload
''',
           '''from length_prefixed_framing import Framer
def test_frame():
    # PEDAGOGY-TEST: D9-NET-ENCODE
    # PEDAGOGY-TEST: D9-NET-FEED
    # PEDAGOGY-TEST: D9-NET-DECODE
    f = Framer()
    blob = f.encode(b"hi")
    assert blob[:4] == bytes([2,0,0,0])
    f.feed(blob[:3]); assert f.decode_one() is None
    f.feed(blob[3:]); assert f.decode_one() == b"hi"
''',
           {"D9-NET-ENCODE": ("starter/length_prefixed_framing.py", "encode"),
            "D9-NET-FEED": ("starter/length_prefixed_framing.py", "feed"),
            "D9-NET-DECODE": ("starter/length_prefixed_framing.py", "decode_one")},
           {"D9-NET-ENCODE": "u32le + payload", "D9-NET-FEED": "extend buf", "D9-NET-DECODE": "need 4+n"})

    py_mod(day, "algorithms", "robin_hood_hash",
           ["D9-RH-INSERT", "D9-RH-LOOKUP", "D9-RH-PROBE"],
           "Robin Hood hash: insert com displace por distância de sonda.",
           '''class RobinHood:
    def __init__(self, cap=8):
        self.cap = cap
        self.keys = [None] * cap
        self.dist = [-1] * cap
    def _probe(self, key):
        # TODO [D9-RH-PROBE]
        raise NotImplementedError
    def insert(self, key):
        # TODO [D9-RH-INSERT]
        raise NotImplementedError
    def lookup(self, key):
        # TODO [D9-RH-LOOKUP]
        raise NotImplementedError
''',
           '''class RobinHood:
    def __init__(self, cap=8):
        self.cap = cap
        self.keys = [None] * cap
        self.dist = [-1] * cap
    def _probe(self, key):
        # PEDAGOGY-SOLUTION: D9-RH-PROBE
        return hash(key) % self.cap
    def insert(self, key):
        # PEDAGOGY-SOLUTION: D9-RH-INSERT
        idx = self._probe(key)
        d = 0
        while True:
            if self.keys[idx] is None:
                self.keys[idx] = key
                self.dist[idx] = d
                return idx
            if self.keys[idx] == key:
                return idx
            if self.dist[idx] < d:
                self.keys[idx], key = key, self.keys[idx]
                self.dist[idx], d = d, self.dist[idx]
            idx = (idx + 1) % self.cap
            d += 1
            if d > self.cap:
                raise RuntimeError("full")
    def lookup(self, key):
        # PEDAGOGY-SOLUTION: D9-RH-LOOKUP
        idx = self._probe(key)
        d = 0
        while self.keys[idx] is not None and d <= self.cap:
            if self.keys[idx] == key:
                return idx
            if self.dist[idx] < d:
                return None
            idx = (idx + 1) % self.cap
            d += 1
        return None
''',
           '''from robin_hood_hash import RobinHood
def test_rh():
    # PEDAGOGY-TEST: D9-RH-PROBE
    # PEDAGOGY-TEST: D9-RH-INSERT
    # PEDAGOGY-TEST: D9-RH-LOOKUP
    h = RobinHood(8)
    i = h.insert("a")
    assert h.lookup("a") == i
    assert h.lookup("missing") is None
''',
           {"D9-RH-PROBE": ("starter/robin_hood_hash.py", "_probe"),
            "D9-RH-INSERT": ("starter/robin_hood_hash.py", "insert"),
            "D9-RH-LOOKUP": ("starter/robin_hood_hash.py", "lookup")},
           {"D9-RH-PROBE": "hash%cap", "D9-RH-INSERT": "displace poorer", "D9-RH-LOOKUP": "stop if dist < d"})

    # node worker pool
    mod = ROOT / "days" / day / "nodejs" / "worker_pool_scheduler"
    W(mod / "starter" / "pool.js", ''''use strict';
function createPool(size) {
  // TODO [D9-NODE-POOL]
  throw new Error('D9-NODE-POOL');
}
function submit(pool, fn) {
  // TODO [D9-NODE-SUBMIT]
  throw new Error('D9-NODE-SUBMIT');
}
function shutdown(pool) {
  // TODO [D9-NODE-SHUT]
  throw new Error('D9-NODE-SHUT');
}
module.exports = { createPool, submit, shutdown };
''')
    W(mod / "solutions" / "pool.js", ''''use strict';
function createPool(size) {
  // PEDAGOGY-SOLUTION: D9-NODE-POOL
  return { size, active: 0, q: [], closed: false, nextId: 1 };
}
function submit(pool, fn) {
  // PEDAGOGY-SOLUTION: D9-NODE-SUBMIT
  if (pool.closed) return Promise.reject(new Error('closed'));
  const id = pool.nextId++;
  return new Promise((resolve, reject) => {
    const job = { id, fn, resolve, reject };
    if (pool.active < pool.size) run(pool, job);
    else pool.q.push(job);
  });
}
function run(pool, job) {
  pool.active++;
  Promise.resolve()
    .then(() => job.fn(job.id))
    .then(job.resolve, job.reject)
    .finally(() => {
      pool.active--;
      if (pool.q.length) run(pool, pool.q.shift());
    });
}
function shutdown(pool) {
  // PEDAGOGY-SOLUTION: D9-NODE-SHUT
  pool.closed = true;
  return pool.active === 0 && pool.q.length === 0;
}
module.exports = { createPool, submit, shutdown };
''')
    W(mod / "starter" / "test.js", ''''use strict';
const assert = require('assert');
const { createPool, submit, shutdown } = require('./pool');
(async () => {
  // PEDAGOGY-TEST: D9-NODE-POOL
  // PEDAGOGY-TEST: D9-NODE-SUBMIT
  // PEDAGOGY-TEST: D9-NODE-SHUT
  const p = createPool(2);
  const a = await submit(p, async (id) => id);
  assert.strictEqual(a, 1);
  assert.strictEqual(shutdown(p), true);
  console.log('ok');
})();
''')
    W(mod / "solutions" / "test.js", (mod / "starter" / "test.js").read_text(encoding="utf-8"))
    W(mod / "starter" / "package.json", '{"name":"worker-pool","private":true}\\n')
    W(mod / "solutions" / "package.json", '{"name":"worker-pool","private":true}\\n')
    pedagogy(mod, "worker_pool_scheduler", "javascript",
             ["D9-NODE-POOL", "D9-NODE-SUBMIT", "D9-NODE-SHUT"],
             "Worker pool com fila, ids e shutdown.",
             f"cd days/{day}/nodejs/worker_pool_scheduler/starter\\nnode test.js",
             {"D9-NODE-POOL": ("starter/pool.js", "createPool"),
              "D9-NODE-SUBMIT": ("starter/pool.js", "submit"),
              "D9-NODE-SHUT": ("starter/pool.js", "shutdown")},
             {"D9-NODE-POOL": "{size,active,q}", "D9-NODE-SUBMIT": "queue or run", "D9-NODE-SHUT": "closed=true"})

    # dotnet jit callsite
    mod = ROOT / "days" / day / "dotnet" / "jit_callsite_model"
    W(mod / "starter" / "CallSite.cs", '''namespace Chris.JitLab;
public abstract class Animal { public abstract string Speak(); }
public class Dog : Animal { public override string Speak() => "woof"; }
public static class CallSite {
    public static string Dispatch(Animal a) {
        // TODO [D9-DN-VIRT]
        throw new NotImplementedException();
    }
    public static string DevirtDog(Dog d) {
        // TODO [D9-DN-DEVIRT]
        throw new NotImplementedException();
    }
    public static bool IsExactDog(Animal a) {
        // TODO [D9-DN-TYPE]
        throw new NotImplementedException();
    }
}
''')
    W(mod / "solutions" / "CallSite.cs", '''namespace Chris.JitLab;
public abstract class Animal { public abstract string Speak(); }
public class Dog : Animal { public override string Speak() => "woof"; }
public static class CallSite {
    public static string Dispatch(Animal a) {
        // PEDAGOGY-SOLUTION: D9-DN-VIRT
        return a.Speak();
    }
    public static string DevirtDog(Dog d) {
        // PEDAGOGY-SOLUTION: D9-DN-DEVIRT
        return d.Speak();
    }
    public static bool IsExactDog(Animal a) {
        // PEDAGOGY-SOLUTION: D9-DN-TYPE
        return a.GetType() == typeof(Dog);
    }
}
''')
    for base in (mod / "starter", mod / "solutions"):
        W(base / "Chris.JitLab.csproj", '''<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup><TargetFramework>net8.0</TargetFramework><ImplicitUsings>enable</ImplicitUsings><Nullable>enable</Nullable></PropertyGroup>
  <ItemGroup><Compile Remove="tests/**" /></ItemGroup>
</Project>
''')
        W(base / "tests" / "Chris.JitLab.Tests.csproj", '''<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup><TargetFramework>net8.0</TargetFramework><IsTestProject>true</IsTestProject></PropertyGroup>
  <ItemGroup>
    <PackageReference Include="Microsoft.NET.Test.Sdk" Version="17.11.1" />
    <PackageReference Include="xunit" Version="2.9.2" />
    <PackageReference Include="xunit.runner.visualstudio" Version="2.8.2" />
  </ItemGroup>
  <ItemGroup><ProjectReference Include="..\\Chris.JitLab.csproj" /></ItemGroup>
</Project>
''')
        W(base / "tests" / "JitTests.cs", '''using Chris.JitLab;
using Xunit;
public class JitTests {
    [Fact]
    public void Virt() {
        // PEDAGOGY-TEST: D9-DN-VIRT
        // PEDAGOGY-TEST: D9-DN-DEVIRT
        // PEDAGOGY-TEST: D9-DN-TYPE
        Animal a = new Dog();
        Assert.Equal("woof", CallSite.Dispatch(a));
        Assert.Equal("woof", CallSite.DevirtDog((Dog)a));
        Assert.True(CallSite.IsExactDog(a));
    }
}
''')
    pedagogy(mod, "jit_callsite_model", "csharp",
             ["D9-DN-VIRT", "D9-DN-DEVIRT", "D9-DN-TYPE"],
             "Call-site virtual vs devirtualized + exact type check.",
             f"cd days/{day}/dotnet/jit_callsite_model/starter\\ndotnet test tests/Chris.JitLab.Tests.csproj",
             {"D9-DN-VIRT": ("starter/CallSite.cs", "Dispatch"),
              "D9-DN-DEVIRT": ("starter/CallSite.cs", "DevirtDog"),
              "D9-DN-TYPE": ("starter/CallSite.cs", "IsExactDog")},
             {"D9-DN-VIRT": "a.Speak()", "D9-DN-DEVIRT": "d.Speak()", "D9-DN-TYPE": "GetType()==typeof(Dog)"})

    print("day11 done")


def refresh_infra(day: str, core_note: str) -> None:
    day_dir = ROOT / "days" / day
    mods = sorted(
        p.relative_to(day_dir).as_posix()
        for p in day_dir.glob("*/*")
        if p.is_dir() and (p / "RESOLUCAO_GUIADA_PASSO_A_PASSO.md").exists()
    )
    n = len(mods)
    # TODO_MAP
    ids = []
    seen = set()
    for m in mods:
        starter = day_dir / m / "starter"
        for p in starter.rglob("*"):
            if not p.is_file():
                continue
            try:
                t = p.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            for tid in re.findall(r"TODO\\s*\\[([A-Z0-9-]+)\\]", t):
                if tid not in seen:
                    seen.add(tid)
                    ids.append(tid)
    W(day_dir / "TODO_MAP.md", f"# TODO map — {day}\\n\\n" + "\\n".join(f"- `{i}`" for i in ids) + "\\n")
    W(day_dir / "VALIDATION.md", f"""# Validacao — {day}

```powershell
python scripts/pedagogy_check_unified.py --day {day}
python scripts/day_contract_check.py --day {day}
python scripts/run_day_tests.py --day {day} --mode solutions
```

## Modulos ({n})

""" + "\\n".join(f"- `{m}`" for m in mods) + "\\n")
    # README: keep title, rewrite table
    W(day_dir / "README.md", f"""# Day {day}

**{n} modulos** — core local + labs sugeridos do GitHub incorporados.

{core_note}

| # | Modulo |
|---|--------|
""" + "\\n".join(f"| {i} | `{m}` |" for i, m in enumerate(mods, 1)) + f"""

**Total:** ~{n * 2}–{n * 3} h (fatie se preciso).
""")
    # ATIVIDADES: rewrite with both tracks
    ativ = f"""# ATIVIDADES — {day}

**Dia:** {n} modulos | core + trilha GitHub incorporada
**Regra:** checkpoint no papel antes do codigo.

## Preparacao

- [ ] Ler START_HERE.md e README.md
- [ ] `python scripts/pedagogy_check_unified.py --day {day}`

## Bloco core (ja existente)

Complete os modulos core listados no README (observabilidade / capstone / reloc conforme o dia).

## Bloco labs GitHub (agora com pasta days/)

"""
    # classify github-ish by TODO prefix
    gh = [m for m in mods if any(
        (day_dir / m / "starter").exists() and "D7-" in (day_dir / m / "starter").read_text(encoding="utf-8", errors="ignore")
        or "D8-" in "".join(p.read_text(encoding="utf-8", errors="ignore") for p in (day_dir / m / "starter").rglob("*") if p.is_file())
        or "D9-" in "".join(p.read_text(encoding="utf-8", errors="ignore") for p in (day_dir / m / "starter").rglob("*") if p.is_file())
        for _ in [0]
    )]
    # simpler: all mods that are not in a fixed core set
    cores = {
        "2026-09-09": {
            "systems/clvm_trace_profiler", "systems/arena_telemetry", "ai/attention_mask",
            "rust/stack_sample_trace", "dotnet/activity_source_span", "nodejs/async_hooks_trace",
            "linux/perf_event_open_lab", "graphics/gpu_timer_query", "parsers/logfmt_lexer",
            "quantum/decoherence_noise", "redteam/yara_match_scan", "agent/verify_replay_log",
            "tooling/pdb_symbol_index",
        },
        "2026-09-10": {
            "systems/clvm_pipeline_integration", "systems/unified_input_pipeline", "linux/composite_input_driver",
            "rust/cross_verify_clvm", "dotnet/capstone_input_host", "graphics/pipeline_state_object",
            "redteam/capstone_triage", "quantum/capstone_measurement", "ai/capstone_tokenizer",
            "nodejs/capstone_stream_pipeline", "parsers/capstone_query_eval", "agent/capstone_agent_loop",
            "tooling/capstone_format_detect",
        },
        "2026-09-11": {
            "systems/clvm_reloc_apply", "systems/bump_poison_arena", "linux/uevent_kv_parse",
            "rust/clvm_reloc_verify", "dotnet/pe_import_span", "graphics/alpha_blend_scanline",
            "redteam/import_name_triage", "quantum/phase_kickback", "ai/rms_norm",
            "nodejs/shared_atomics_ring", "parsers/ini_rd_lexer", "agent/tool_barrier_join",
            "tooling/coff_sym_name",
        },
    }
    core = cores.get(day, set())
    gh_mods = [m for m in mods if m not in core]
    for m in gh_mods:
        ativ += f"- [ ] `{m}` — implementar TODOs; paper-trace do Caso 1\\n"
    ativ += f"""
**Checkpoint trilha GitHub:**

- [ ] Listei os {len(gh_mods)} labs novos no caderno
- [ ] Rodei solutions desses labs

```powershell
python scripts/run_day_tests.py --day {day} --mode solutions
```
"""
    W(day_dir / "ATIVIDADES.md", ativ)
    print(day, "infra", n, "modules", "gh", len(gh_mods))


def wire_maps():
    # append LEARNING_PATHS + module_project_map for new modules
    lp = ROOT / "docs" / "LEARNING_PATHS.md"
    lt = lp.read_text(encoding="utf-8")
    mp = ROOT / "scripts" / "module_project_map.py"
    mt = mp.read_text(encoding="utf-8")
    new_entries = []
    for day in ("2026-09-09", "2026-09-10", "2026-09-11"):
        day_dir = ROOT / "days" / day
        for p in sorted(day_dir.glob("*/*")):
            if not (p / "RESOLUCAO_GUIADA_PASSO_A_PASSO.md").exists():
                continue
            key = f"{day}/{p.parent.name}/{p.name}"
            if key not in lt:
                new_entries.append(key)
            if key not in mt:
                proj = "projects/chris-binary-toolkit"
                if "agent" in key: proj = "projects/chris-agent-core"
                elif "regex" in key or "parsers" in key: proj = "projects/chris-regex"
                elif "dotnet" in key: proj = "projects/chris-dotnet-bench"
                elif "graphics" in key: proj = "projects/chris-renderer"
                elif "linux" in key: proj = "projects/chris-linux-utils"
                elif "quantum" in key: proj = "projects/chris-qsim"
                elif "ai" in key: proj = "projects/chris-tensor"
                elif "nodejs" in key: proj = "projects/chris-node-streaming"
                block = f'''
    "{key}": {{
        "project": "{proj}",
        "carry": "{p.name} from github track",
        "tests": "day module tests",
        "milestone": "MILESTONES.md — {p.name}",
        "commit": "feat({day}): port {p.name}",
    }},'''
                # insert before def module_key
                if "def module_key" in mt and block.strip() not in mt:
                    pre, post = mt.split("\\ndef module_key", 1)
                    pre = pre.rstrip()
                    if pre.endswith("}"):
                        pre = pre[:-1].rstrip()
                        if not pre.endswith(","):
                            pre += ","
                        mt = pre + block + "\\n}\\n\\ndef module_key" + post
    if new_entries:
        lt = lt.rstrip() + "\\n\\n### Labs GitHub incorporados (09–11)\\n\\n"
        for i, k in enumerate(new_entries, 1):
            lt += f"| {i} | `{k}` | github track |\\n"
        lp.write_text(lt + "\\n", encoding="utf-8", newline="\\n")
    mp.write_text(mt, encoding="utf-8", newline="\\n")

    # GFX exempt
    ped = ROOT / "scripts" / "pedagogy_check_unified.py"
    pt = ped.read_text(encoding="utf-8")
    for name in ("explicit_barriers", "descriptor_binding_model"):
        if f'"{name}"' not in pt:
            pt = pt.replace('"alpha_blend_scanline",', f'"alpha_blend_scanline",\\n    "{name}",')
    ped.write_text(pt, encoding="utf-8", newline="\\n")


if __name__ == "__main__":
    # ensure day09 from part1
    if not (ROOT / "days/2026-09-09/systems/buddy_allocator").exists():
        s9.day09()
    day10()
    day11()
    for d, note in (
        ("2026-09-09", "Core: observabilidade. GitHub: buddy/Welford/prologue/pratt/…"),
        ("2026-09-10", "Core: capstone. GitHub: ABA/TLB/regex/patcher/…"),
        ("2026-09-11", "Core: reloc/ABI. GitHub: hazard/KV/DWARF/Pike/…"),
    ):
        refresh_infra(d, note)
    wire_maps()
    print("all done")
