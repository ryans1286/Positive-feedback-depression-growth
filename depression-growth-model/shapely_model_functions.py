# Import shapely tools
from shapely import geometry
from shapely.geometry import Point, Polygon, MultiPolygon
from shapely.ops import unary_union

# Import required math tools
import numpy as np
import scipy
from scipy import stats
from scipy.stats import linregress
import pandas as pd

"""
---INITIATE MODEL---
Function creates an empty list to store depressions. Run before beginning 
simulation loops.
Inputs: 
        None
Returns:
        Empty list to hold new depressions
"""


def initiate_model():
    return []


"""
---CREATE LIST OF LISTS TO SAVE DATA---
This function creates the list of lists for storing data from each timstep.
Inputs:
        None
Returns:
        This function returns an empty list of lists for use in the function
        save_timestep().
"""


def create_empty_data_lists():
    return [[], [], [], [], []]


"""
---ADD NEW DEPRESSIONS TO MODEL SPACE---
Adds new depressions to the model space. New depression coordinates are selected
from a normal distribution with shape equal to the model space dimensions.
Inputs:
        number = the number of new depressions to add
        model_size = the linear dimension of the square model space

Returns:
        Function returns a list of Shapely polygons. Return must be 
        converted to MultiPolygons or GeoSeries to plot. 
Dependencies:
        This function does not depend on any other functions in this model.
"""


def add_new_depressions(number, model_size):
    # Choose coordinates of new depression centers from normal distribution
    coordinates = [(np.random.uniform(low=0, high=model_size),
                    np.random.uniform(low=0, high=model_size)) for i in range(number)]
    # Give new depressions an area selected from a lognormal distribution
    init_buffer = np.sqrt(np.random.lognormal(mean=0.1, sigma=0.5, size=number) / np.pi)
    # Buffer points to create polygon depressions, add depressions to list.
    polygons = [Point(coordinates[j]).buffer(init_buffer[j]) for j in range(number)]
    return polygons


"""
---CALCULATE CHANGE IN DEPRESSION AREA---
This function calculates the difference in area between two shapes. It is used
within scale_to_buffer to find the correct buffer value to achieve the desired
change in depression area. 
Inputs:
        x = buffer values (float)
        shape = Shapely polygon object
        a_next = the desired area value
Returns:
        Function returns difference in areas between two Shapely polygons.
Dependencies:
        This function is used within scale_to_buffer.
"""


def a_diff(x, shape, a_next):
    return a_next - shape.buffer(x).area


"""
---CALCULATE BUFFER VALUE---
This function approximates the buffer needed for the solution to the 
differential equation:
    dA/dt = cA^k
    dA = cA^k dt
    A_next - A_last = c*(A_last)^k *dt
    A_next = A_last + c*(A_last)^k *dt
to find the buffer value that gives the next area value.
Inputs:
        shape = Shapely polygon object
        scale_factor = exponent "k" in differential equation
        c = constant of proportionality in differential equation
        dt = timestep length

        ***Keep c*dt small to avoid model instability!***
Returns: 
        Function returns buffer value to increase shape area such that it 
        satisfies the differential equation above. Minimization uses 
        scipy.optimize.root. This method is faster than bisect
Dependencies:
        This function runs within the grow_depressions function.
c*dt needs to be small such that the dA is 'small' between timesteps
"""


def scale_to_buffer(shape, scale_factor, c, dt):
    a_next = c * dt * shape.area ** scale_factor + shape.area
    sol = scipy.optimize.root(a_diff, [0], args=(shape, a_next))
    return sol.x[0]

"""
Same objective as scale_to_buffer() function, but calculates the 4th order Runge-Kutta approximation.
"""
def RK4_scale_to_buffer(shape, scale_factor, c, dt):
    k1 = dt * c * shape.area ** scale_factor
    k2 = dt * c * (shape.area + k1 / 2) ** scale_factor
    k3 = dt * c * (shape.area + k2 / 2) ** scale_factor
    k4 = dt * c * (shape.area + k3) ** scale_factor

    a_next = shape.area + (1 / 6) * (k1 + 2 * k2 + 2 * k3 + k4)
    sol = scipy.optimize.root(a_diff, [0], args=(shape, a_next))

    return sol.x[0]


"""
Model flow:
    1. Add initial depressions to the model space.
    2. Grow depressions.
    3. Merge overlapping depressions.
    4. Add new depressions.
    5. Repeat Steps 2, 3, and 4
"""

"""
---Grow depressions---
This function solves the next timestep of the differential equation:
    dA/dt = cA^k
    dA = cA^k dt
    A_next - A_last = c*(A_last)^k *dt
    A_next = A_last + c*(A_last)^k *dt
Inputs:
        shapes = list of Shapely polygons/points
        scale_factor = scaling exponent "k" in the differential equation
        c = proportionality constant 
        dt = timestep length

        ***Keep c*dt small to avoid model instability!***

Returns:
        Function returns python list of polygons. Must be coverted to MultiPolygons
        or GeoSeries to plot. 
"""


def grow_depressions(shapes, scale_factor, c, dt):
    # Convert list of polygons to class Shapely geometry MultiPolygons
    polys = geometry.MultiPolygon(shapes)
    # Create an array of buffers for depression growth
    bufferArray = np.array([RK4_scale_to_buffer(p, scale_factor, c, dt) for p in polys])
    # Increase depression areas using the buffer array
    scaledShapes = [Polygon(polys[k]).buffer(bufferArray[k]) for k in range(len(polys))]
    return scaledShapes


"""
---MERGE OVERLAPPING DEPRESSIONS---
This function uses Shapely's unary_union function to merge polygons. It does 
nothing new or unique outside of the unary_union. This function exists as a 
reminder of what the unary_union function is doing. 
Inputs:
        shapes = list of Shapely polygons

Returns:
        Function returns as list of Shapely Multipolygons. 
"""


def merge_depressions(shapes):
    if type(shapes) != 'Polygon':
        return list(unary_union(shapes))


"""
---SAVE TIMESTEP DATA---
This function records the timestep, total number of depressions added to the
model, total number of depressions (counting mergers), the areas, and the 
perimeters of each depression. 
Inputs:
        lists = Python list of lists, 
                rows represent ["t_step", "N_t", "N_m", "area", "perimeter"]
        shapes = Python list or Shapely MultiPolygons list
        tstep = timestep (iteration number)
        dt = timelegth of a single timestep 

Returns:
        Function returns updated list of lists. The lists are extended for 
        each successive timestep. 
        [[list of timesteps],
         [list of total number of depressions added to model space],
         [list of total number of depressions including mergers],
         [list of areas],
         [list of perimeters]]
"""


def save_timestep(lists, shapes, tstep, dt, n):
    areas = [s.area for s in shapes]
    perimeters = [s.length for s in shapes]
    N_t = int(np.floor((tstep) * dt)) * n + n
    N_m = len(areas)
    tstepList = [tstep for i in range(len(areas))]
    N_t_list = [N_t for i in range(len(areas))]
    N_m_list = [N_m for i in range(len(areas))]
    lists[0].extend(tstepList)
    lists[1].extend(N_t_list)
    lists[2].extend(N_m_list)
    lists[3].extend(areas)
    lists[4].extend(perimeters)
    return lists


