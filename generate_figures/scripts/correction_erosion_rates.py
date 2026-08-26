from support.aux_functions.models_constants import decay_be,decay_al
import math
from support.aux_functions.misc_functions import load_dataset
from support.aux_functions.constant_steady_lines_model import steady_state_model

bl = steady_state_model()

all_sample_names,all_n10,all_n26,all_description_sample = load_dataset()
for sample_id, measured_N10,measured_N26,description_sample in zip(all_sample_names,all_n10,all_n26,all_description_sample):
    if description_sample == "flood":
        time = bl.burial_decay_time(measured_N10,measured_N26)
        print(time)

    # corrected_N10 = measured_N10*(math.e**(decay_be*time))
    # corrected_N26 = measured_N26*(math.e**(decay_al*time))
#