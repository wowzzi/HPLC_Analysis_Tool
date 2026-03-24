settings_dict = {
    'minimum peak height': 1.0,
    'minimum indices between peaks': 40,
    'minimum peak prominence': 0.2,
    'integration window factor': 0.05,
    'connect peaks distance': 300,
    'slope end cut-off value (mAU/min)': 10,
    'back to main menu': ""
}
setting_explained = {
    'minimum peak height': "The minimum peak height defines the minimum height (signal) a peak must achieve to be detected.",
    'minimum indices between peaks': "The minimum indices between peaks defines the minimum number of data-points that detected peaks must be spread apart.",
    'minimum peak prominence': "The minimum peak prominence defines how well defined the peak must be to be detected,"
                                "\nA low prominence value will increase peak detection sensitivity."
                                "\nValues < ~0.05 should be avoided else fake peaks will be detected",
    'integration window factor': "This factor is applied to the peak slope to determine where the peak starts and ends."
                                "\nA lower factor will broaden the peaks a higher factor will narrow them affecting taller peaks more than shorter ones",
    'connect peaks distance': "This value will connect peaks integration windows if they are less than the set number of values apart",
    'slope floor': "The slope floor is an arbitrary slope cut-off for the peak integration window"
                    "if the slope value was calulcation by integration window factor to cut off at a slope greater than this value, this value will be used instead."
}