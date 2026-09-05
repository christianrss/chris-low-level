struct VSOut{float4 pos:SV_Position;float2 uv:TEXCOORD0;}; float4 PSMain(VSOut i):SV_Target0{return float4(i.uv,0,1);}
