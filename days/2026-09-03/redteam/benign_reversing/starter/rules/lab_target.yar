rule LowLevel_Reversing_Lab_V1 {
    meta:
        description: "Detecta somente o binário educacional deste laboratório"

    strings:
        // TODO [RE-YARA-01]: add strings that uniquely identify our benign lab target.
        $marker = "LOWLEVEL-REVERSING-LAB-V1" ascii
        $accepted = "accepted" ascii
        $rejected = "rejected" ascii

    condition:
        $marker and $accepted and $rejected
}
