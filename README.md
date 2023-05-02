# Positive-feedback-depression-growth
 Data, model, and figure generation code to accompany the manuscript:
 
 R.M. Strickland, M.D. Covington, J.D. Gulley, R.B. Kayastha, J.M. Blackstock (2023). Englacial drainage drives positive feedback depression growth on the Ngozumpa Glacier, Nepal, submitted to Geophysical Research Letters.
 
 If you make use of "voitalov-tail-estimation.py", please refer to and cite https://github.com/ivanvoitalov/tail-estimation 
 
# Description of Contents:

* GRL-make-figures.ipynb - 
This notebook contains code to reproduce Figure 2 and Figure 3 in the manuscript. Users will need the Python packages: pathlib, geopandas, pandas, pickle, numpy, scipy, matplotlib, and seaborn. 

* voitalov-tail-estimation.py - 
This script estimates the power-law tail exponent. This script was written and published with Voitalov et al. (2019). Please see https://github.com/ivanvoitalov/tail-estimation for documentation. 

* model_run-tail-estimations.ipynb -
This notebook calculates the tail exponents for the simulated depression size distributions. It combines the results from each parameter set of 11 simulations and produces the .dat files needed to execute the Voitalov tail estimation script. The resulting plots from this script are found in the "model-data/tail-estimation-plots" directory. 

* ngozumpa_run-tail-estimations.ipynb - 
This notebook calculates the tail exponents for depressions on the Ngozumpa Glacier using the 2019 DEM. The resulting plot from this script is found in "ngozumpa-data/2019_Ngozumpa-depressions-tail-estimation.pdf". 

* depression-growth-model/ - 
This directory contains the two Python files needed to run the depression growth model. "shapely_model_functions.py" contains the function definitions built using the shapely python package. "run_simulations.py" contains the script to run the model. Users will need to modify the script with the desired parameters. 

* model-data/ - 
This directory contains four sub-directories with model output data and the tail estimation plots. "model-data/csv-files/" contains sub-directories with the model output from each parameter set. "model-data/combined-dat-files/" contains the .dat files of model output data used to run the Voitalov tail estimation script. 
