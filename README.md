# Paper 

**Author:** Pedro Oliveira
**Date:** August 2026
**GitHub:** [@thepedroland](https://github.com/thepedroland)

This code can be used to generate results for the paper *[X]* and plot figures X...X
---
## Overview

This repository simulates the accumulation of cosmogenic nuclides over time for buried samples, 
coupling cosmogenic nuclide production by spalattion, negative muon capture and fast muon throughout the 
entire depth profile.

- **Scaling method:** LSDn
- **Production pathways modeled:**
  - **Spallation**: average scaled from scaling factor CRONUS Calc based on area latitude and altitude
  - **Negative muon capture and fast muons**: calculated as a function of depth and Rc using Balco (2017)
    - **Time-varying cutoff rigidity (Rc): calibrated from Mijjum et al. (2025)
      - Rc variation from 0-35Myr saved in data/Rc_results.csv
- Used constants can be found in support/models_constants.py
---
## Software/ Package Requirements 
Versions are listed as the ones working when results were generated for this paper. Newer versions might be available, 
however, it is not guaranteed they will work smoothly.

| Package      | Version |
|--------------|---------|
| Python       | 3.13.12 |
| MATLAB       | 26a     |
| matlabengine | 26.1    |
| numpy        | 2.3.5   |
| pandas       | 2.3.3   |
| torch        | 2.11.0  |
| matplotlib   | 3.10.8  |

---
## Workflow

The results used for figures X are in generate_data/python_data_results/results_data, if you want to replicate follow:

***Reproduce dataset**
Run MC simulations and generate results using:
Run _RUN_num_model_burial_trajectory.py_ check the HowToUse.md for further steps.
  Result/plot files pattern
  ..."_[Sample ID]_R[Starting reference]_Ddensity..."

***Plot figures**
Figures can be plotted using _generate_figures_ scripts
Note: if you want to use this banana plot but for your own data please check this [code](banana.plot)

Cosmogenic nuclide data and model parameters used in this work can be found as excel files in _**generate_figures/tables**_

## References

- Greg Balco, Production rate calculations for cosmic-ray-muon-produced 10Be and 26Al benchmarked against geological calibration data, Quaternary Geochronology, Volume 39,
2017, Pages 150-173, ISSN 1871-1014,https://doi.org/10.1016/j.quageo.2017.02.001. (https://www.sciencedirect.com/science/article/pii/S1871101416301649)

- Mijjam

## Citation
If you use any part of the scripts in this repository please cite:
- ...
