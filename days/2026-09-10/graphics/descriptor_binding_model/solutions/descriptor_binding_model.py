def layout_of(*bindings):
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
