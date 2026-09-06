#include "huffman.hpp"
#include "bit_io.hpp"
#include <algorithm>
#include <cstring>
#include <queue>
#include <vector>

namespace {

struct Node {
    std::uint8_t symbol = 0;
    std::uint32_t freq = 0;
    Node* left = nullptr;
    Node* right = nullptr;
    bool leaf = false;
};

struct NodeCompare {
    bool operator()(const Node* a, const Node* b) const { return a->freq > b->freq; }
};

void collect_codes(const Node* node, std::uint32_t prefix, int depth, std::vector<HuffmanCodeEntry>& out) {
    if (!node) {
        return;
    }
    if (node->leaf) {
        HuffmanCodeEntry e;
        e.symbol = node->symbol;
        e.bit_length = static_cast<std::uint8_t>(depth == 0 ? 1 : depth);
        e.code = static_cast<std::uint16_t>(prefix << (16 - e.bit_length));
        out.push_back(e);
        return;
    }
    collect_codes(node->left, (prefix << 1), depth + 1, out);
    collect_codes(node->right, (prefix << 1) | 1u, depth + 1, out);
}

void free_tree(Node* node) {
    if (!node) {
        return;
    }
    free_tree(node->left);
    free_tree(node->right);
    delete node;
}

}  // namespace

// PEDAGOGY-SOLUTION: COMP-HUF-02
// PEDAGOGY-SOLUTION: COMP-HUF-03
// PEDAGOGY-SOLUTION: COMP-HUF-04

bool build_huffman_codes(const std::uint32_t freq[256], std::vector<HuffmanCodeEntry>& table) {
    table.clear();
    std::priority_queue<Node*, std::vector<Node*>, NodeCompare> pq;
    for (int i = 0; i < 256; ++i) {
        if (freq[i] == 0) {
            continue;
        }
        auto* n = new Node();
        n->symbol = static_cast<std::uint8_t>(i);
        n->freq = freq[i];
        n->leaf = true;
        pq.push(n);
    }
    if (pq.empty()) {
        return false;
    }
    if (pq.size() == 1) {
        Node* only = pq.top();
        pq.pop();
        auto* root = new Node();
        root->freq = only->freq;
        root->left = only;
        root->leaf = false;
        pq.push(root);
    }
    while (pq.size() > 1) {
        Node* a = pq.top();
        pq.pop();
        Node* b = pq.top();
        pq.pop();
        auto* parent = new Node();
        parent->freq = a->freq + b->freq;
        parent->left = a;
        parent->right = b;
        pq.push(parent);
    }
    Node* root = pq.top();
    collect_codes(root, 0, 0, table);
    free_tree(root);
    std::sort(table.begin(), table.end(), [](const HuffmanCodeEntry& a, const HuffmanCodeEntry& b) {
        return a.symbol < b.symbol;
    });
    return !table.empty();
}

bool encode_huffman(std::span<const std::uint8_t> input, std::vector<std::uint8_t>& out) {
    std::uint32_t freq[256] = {};
    for (std::uint8_t b : input) {
        ++freq[b];
    }
    std::vector<HuffmanCodeEntry> table;
    if (!build_huffman_codes(freq, table)) {
        return false;
    }
    HuffmanCodeEntry lookup[256] = {};
    for (const auto& e : table) {
        lookup[e.symbol] = e;
    }
    BitWriter writer;
    for (std::uint8_t b : input) {
        const auto& e = lookup[b];
        writer.write_bits(e.code >> (16 - e.bit_length), e.bit_length);
    }
    writer.flush();
    const auto& payload = writer.bytes();
    out.clear();
    out.insert(out.end(), CHHUF_MAGIC, CHHUF_MAGIC + 5);
    const std::uint32_t len = static_cast<std::uint32_t>(input.size());
    out.push_back(static_cast<std::uint8_t>(len & 0xFF));
    out.push_back(static_cast<std::uint8_t>((len >> 8) & 0xFF));
    out.push_back(static_cast<std::uint8_t>((len >> 16) & 0xFF));
    out.push_back(static_cast<std::uint8_t>((len >> 24) & 0xFF));
    const std::uint16_t n = static_cast<std::uint16_t>(table.size());
    out.push_back(static_cast<std::uint8_t>(n & 0xFF));
    out.push_back(static_cast<std::uint8_t>((n >> 8) & 0xFF));
    for (const auto& e : table) {
        out.push_back(e.symbol);
        out.push_back(e.bit_length);
        out.push_back(static_cast<std::uint8_t>((e.code >> 8) & 0xFF));
        out.push_back(static_cast<std::uint8_t>(e.code & 0xFF));
    }
    out.insert(out.end(), payload.begin(), payload.end());
    return true;
}

bool decode_huffman(std::span<const std::uint8_t> input, std::vector<std::uint8_t>& out) {
    out.clear();
    if (input.size() < 11 || std::memcmp(input.data(), CHHUF_MAGIC, 5) != 0) {
        return false;
    }
    std::uint32_t len = 0;
    len |= input[5];
    len |= static_cast<std::uint32_t>(input[6]) << 8;
    len |= static_cast<std::uint32_t>(input[7]) << 16;
    len |= static_cast<std::uint32_t>(input[8]) << 24;
    const std::uint16_t n = static_cast<std::uint16_t>(input[9] | (static_cast<std::uint16_t>(input[10]) << 8));
    std::size_t p = 11;
    if (p + n * 4 > input.size()) {
        return false;
    }
    struct DecodeNode {
        int left = -1;
        int right = -1;
        int symbol = -1;
    };
    std::vector<DecodeNode> nodes(1);
    for (std::uint16_t i = 0; i < n; ++i) {
        const std::uint8_t sym = input[p++];
        const std::uint8_t bit_len = input[p++];
        const std::uint16_t code =
            static_cast<std::uint16_t>((static_cast<std::uint16_t>(input[p]) << 8) | input[p + 1]);
        p += 2;
        int node = 0;
        for (int b = 0; b < bit_len; ++b) {
            const bool bit = ((code >> (15 - b)) & 1u) != 0;
            if (bit) {
                if (nodes[node].right < 0) {
                    nodes[node].right = static_cast<int>(nodes.size());
                    nodes.push_back({});
                }
                node = nodes[node].right;
            } else {
                if (nodes[node].left < 0) {
                    nodes[node].left = static_cast<int>(nodes.size());
                    nodes.push_back({});
                }
                node = nodes[node].left;
            }
        }
        nodes[node].symbol = sym;
    }
    BitReader reader(std::span<const std::uint8_t>(input.data() + p, input.size() - p));
    out.reserve(len);
    while (out.size() < len) {
        int node = 0;
        while (nodes[node].symbol < 0) {
            bool bit = false;
            if (!reader.read_bit(bit)) {
                return false;
            }
            node = bit ? nodes[node].right : nodes[node].left;
            if (node < 0) {
                return false;
            }
        }
        out.push_back(static_cast<std::uint8_t>(nodes[node].symbol));
    }
    return out.size() == len;
}
