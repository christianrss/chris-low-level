// PEDAGOGY-SOLUTION: RE-YARA-01

rule LowLevel_Reversing_Lab_V1 {
    meta:
        description = "Detects only the benign educational reversing target"
        purpose = "training"

    strings:
        $marker = "LOWLEVEL-REVERSING-LAB-V1" ascii
        $accepted = "accepted" ascii
        $rejected = "rejected" ascii

    condition:
        $marker and $accepted and $rejected
}
