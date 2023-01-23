# Positive-feedback-depression-growth
 Data, model, and figure generation code to accompany the manuscript:
 
 R.M. Strickland, M.D. Covington, J.D. Gulley, J. Blackstock (2023). Positive feedback growth of depressions on the debris-covered Ngozumpa Glacier, Nepal, submitted to Geophysical Research Letters.
 
 ## Contents:
 
 * figure-2_GRL.png
 * figure-3_GRL.png
 * GRL-make-figures.ipynb
 * model_run-tail-estimations.ipynb
 * ngozumpa_run-tail-estimations.ipynb
 * voitalov-tail-estimation.py
 * USGSAgisoftPhotoScanWorkflow.pdf
 * ngozumpa-data/
   * 2019_Ngozumpa-depressions.csv
   * 2019_Ngozumpa-depressions.dat
   * 2019_Ngozumpa-depressions-tail-estimation.pdf
   * Rasters/
     * 2019_NgozumpaDEM_UTM_1m.tif
     * 2019_Ngozumpa-depressions_NaN.tif
     * 2019_Ngozumpa-depression-depths.tif
   * Vectors/
     * 2019_Ngozumpa-depressions.shp
     * 2019_Ngozumpa-depressions.dbf
     * 2019_Ngozumpa-depressions.prj
     * 2019_Ngozumpa-depressions.qpj
     * 2019_Ngozumpa-depressions.shx
 * model-data/
   * combined-dat-files/
     * [32 .dat files of simulation data]
   * csv-files/
     * 0-5_m_output/
       * csv-files/
         * 500/
           * [11 .csv files for this paramter set]
         * 750/
           * [11 .csv files for this paramter set]
         * 1000/
           * [11 .csv files for this paramter set]
         * 1250/
           * [11 .csv files for this paramter set]
     * 0-5_nm_output/
       * csv-files/
         * 500/
         * 750/
         * 1000/
         * 1250/
     * 1_m_output/
       * csv-files/
         * 500/
         * 750/
         * 1000/
         * 1250/
     * 1_nm_output/
       * csv-files/
         * 500/
         * 750/
         * 1000/
         * 1250/
     * 1-25_m_output/
       * csv-files/
         * 500/
         * 750/
         * 1000/
         * 1250/
     * 1-25_nm_output/
       * csv-files/
         * 500/
         * 750/
         * 1000/
         * 1250/
     * 1-5_m_output/
       * csv-files/
         * 500/
         * 750/
         * 1000/
         * 1250/
     * 1-5_nm_output/
       * csv-files/
         * 500/
         * 750/
         * 1000/
         * 1250/
   * pickle-files/
   * tail-estimation-plots/
     * [32 .pdf tail-estimation plots for simulations]
     * ReadMe_tail-estimation-plots.txt
 * depression-growth-model/
   * run_simulations.py
   * shapely_model_functions.py
   * ReadMe_model.txt
