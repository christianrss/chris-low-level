USAGES = ["Undefined", "CopyDst", "ShaderRead", "RenderTarget", "Present"]

def validate_transition(before, after):
    # TODO [D7-GFX-VALIDATE]
    raise NotImplementedError("D7-GFX-VALIDATE")

def d3d12_barrier(before, after):
    # TODO [D7-GFX-D3D12]
    raise NotImplementedError("D7-GFX-D3D12")

def vulkan_barrier(before, after):
    # TODO [D7-GFX-VULKAN]
    raise NotImplementedError("D7-GFX-VULKAN")
