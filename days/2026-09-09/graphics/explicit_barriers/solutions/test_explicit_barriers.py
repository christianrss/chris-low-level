from explicit_barriers import validate_transition, d3d12_barrier, vulkan_barrier

def test_validate():
    # PEDAGOGY-TEST: D7-GFX-VALIDATE
    assert validate_transition("Undefined", "CopyDst") is True
    try:
        validate_transition("Undefined", "Present")
        assert False
    except ValueError:
        pass

def test_maps():
    # PEDAGOGY-TEST: D7-GFX-D3D12
    # PEDAGOGY-TEST: D7-GFX-VULKAN
    d = d3d12_barrier("CopyDst", "ShaderRead")
    assert d["before"] == "COPY_DEST"
    v = vulkan_barrier("CopyDst", "ShaderRead")
    assert v["after"][0] == "SHADER_READ_ONLY_OPTIMAL"
