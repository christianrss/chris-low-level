def match(code, text):
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
