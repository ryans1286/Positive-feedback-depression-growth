import geopandas as gpd
import pandas as pd
import pickle
import os
from shapely_model_functions import *

"""
DATA STORAGE

Name the directory and the index file paths for simulation data. 
"""
dirname = "output"
index_file = dirname + "/" + "simulation_index.txt" #keeps track of all the simulations run

if os.path.exists(dirname) == False:
    os.mkdir(dirname)

if os.path.exists(index_file) == False:
    with open(index_file, 'w') as f:
        f.write("simnum\tn\tr\tc\tdt\tmerger_choice\n")
        
pickle_model = 'yes' #do you want to pickle the model periodically?
pickle_interval = 5 #whole number total time interval to pickle the model
pickle_termination = 'yes' #do you want to pickle the final timestep?

"""
PARAMETERS

Simulation run times depend on the growth rate exponent, the initial number of depressions,
and whether or not mergers are allowed. 

If you wish to run a set of simulations with different parameters, the following 
parameters can be input as lists and run as a loop: number, scales, mergers
"""
total_time = 50 #maximum time to run the model
number = [500] #initial number of depressions to place in the model
c = 0.25 #proportionality constant
dt = 0.01 #time step length
size = 1000 #model dimension in meters
scales = [1.5] #growth rate exponents, 0.5, 1, 1.25, 1.5
mergers = ['no'] #type 'yes' or 'no' 
number_of_simulations = 10 #for each set of parameters

timesteps = int(total_time/dt)


"""
RUN THE SIMULATIONS
"""

for merger_choice in mergers:
    for n in number:
        for r in scales:
            for simnum in range(number_of_simulations):
                if merger_choice == 'yes':
                    m = 'm'
                elif merger_choice == 'no':
                    m = 'nm'
                    
                sim_name = str(r) + "_" + str(m) + "_" + str(n) + "_sim-" + str(simnum)
                
                # Add simulation paramters to index file
                param_names = ['sim_num', 'n', 'r', 'c', 'dt', 'mergers']
                params = [simnum, n, r, c, dt, merger_choice]
                with open(index_file, 'a') as f:
                    f.write("{}\t{}\t{}\t{}\t{}\t{}\n".format(simnum, n, r, c, dt, merger_choice))
                    
                df = pd.DataFrame()
                
                # Create empty data structures needed to run model
                all_depressions = initiate_model() #creates an empty list
                all_depressions.extend(add_new_depressions(n, size)) #Adds initial depression shapely objects to the model space

                for tstep in range(timesteps):
                    if len(all_depressions) < 100:
                        break

                    if merger_choice  == 'yes':
                        all_depressions = merge_depressions(grow_depressions(all_depressions, r, c, dt))
                    else:
                        all_depressions = grow_depressions(all_depressions, r, c, dt)
                        
                    max_area = gpd.GeoSeries(all_depressions).area.max()
                    
                    #Stop the model when the largest depression exceeds 1/4 the total model area
                    if max_area > 0.25 * size**2:
                        break

                    #Stop the model in the unlikely event that nearly all of the depressions merge before meeting the max area criterion
                    if len(all_depressions) < 100:
                        break
                    
                    #Add a new column of areas to simulation data CSV every 100 time steps
                    #Write this to file in case the model terminates unexpectedly
                    if tstep % 100 == 0:
                        areas = [s.area for s in all_depressions]
                        areas = np.array(areas)
                        areas = np.append(areas, np.zeros(n-len(areas)) + np.nan)
                        df["t="+str(int(tstep*dt))] = areas #areas list length extended with NaNs so Pandas doesn't complain
                        df.to_csv(dirname + "/" + sim_name + ".csv")
                    
                    if pickle_model == 'yes':
                        if tstep*dt % pickle_interval == 0:
                            
                            #Pickle the model
                            pickle_fname = dirname + "/" + sim_name + "_time={}.pkl".format(int(tstep*dt))
                            pf = open(pickle_fname, 'wb')
                            pickle.dump(all_depressions, pf)
                            pf.close()

                areas = [s.area for s in all_depressions]
                areas = np.array(areas)
                areas = np.append(areas, np.zeros(n-len(areas)) + np.nan)
                df["t="+str(int((tstep)*dt))] = areas
                df.to_csv(dirname + "/" + sim_name + ".csv")
                
                #Pickle the model
                if pickle_termination == 'yes':
                    pickle_fname = dirname + "/" + sim_name + "_time={}.pkl".format(int(tstep*dt))
                    pf = open(pickle_fname, 'wb')
                    pickle.dump(all_depressions, pf)
                    pf.close()
                    
                simnum += 1
                
                #Clear the memory
                lst = [df]
                del df
                del lst
