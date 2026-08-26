from support.aux_functions.models_constants import decay_be,decay_al
import math

measured_N10 = 104401.2612
measured_N26 = 633407.7934
time = 175000

corrected_N10 = measured_N10*(math.e**(decay_be*time))
corrected_N26 = measured_N26*(math.e**(decay_al*time))

print("N10Be:",measured_N10, "N26Al:",measured_N26)
print("C_N10Be:",corrected_N10, "C_N26Al:",corrected_N26)