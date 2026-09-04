rule LowLevel_Reversing_Lab_V1 {
    strings:
        // TODO [RE-YARA-01]: add strings that uniquely identify our benign lab target.
        $marker = "LOWLEVEL-REVERSING-LAB-V1" ascii

    condition:
        $marker
}
