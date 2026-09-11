USAGES=["Undefined","CopyDst","ShaderRead","RenderTarget","Present"]
_ALLOWED={("Undefined","CopyDst"),("CopyDst","ShaderRead"),("ShaderRead","RenderTarget"),("RenderTarget","Present"),("Present","RenderTarget")}
def validate_transition(before,after):
    # PEDAGOGY-SOLUTION: D7-GFX-VALIDATE
    if (before,after) not in _ALLOWED: raise ValueError("invalid transition")
    return True
def d3d12_barrier(before,after):
    # PEDAGOGY-SOLUTION: D7-GFX-D3D12
    validate_transition(before,after);m={"Undefined":"COMMON","CopyDst":"COPY_DEST","ShaderRead":"PIXEL_SHADER_RESOURCE","RenderTarget":"RENDER_TARGET","Present":"PRESENT"};return {"before":m[before],"after":m[after]}
def vulkan_barrier(before,after):
    # PEDAGOGY-SOLUTION: D7-GFX-VULKAN
    validate_transition(before,after);m={"Undefined":("UNDEFINED","TOP_OF_PIPE","NONE"),"CopyDst":("TRANSFER_DST_OPTIMAL","TRANSFER","TRANSFER_WRITE"),"ShaderRead":("SHADER_READ_ONLY_OPTIMAL","FRAGMENT_SHADER","SHADER_READ"),"RenderTarget":("COLOR_ATTACHMENT_OPTIMAL","COLOR_ATTACHMENT_OUTPUT","COLOR_ATTACHMENT_WRITE"),"Present":("PRESENT_SRC_KHR","BOTTOM_OF_PIPE","NONE")};return {"before":m[before],"after":m[after]}
