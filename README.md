MethodOfAngularCoefficients is a Python project that provides 
to calculate the Clausing coefficient for a cylindrical tube using the angular coefficients method.
![round_tube_sep](https://github.com/eprush/MethodOfAngularCoefficients/assets/91796933/c945c4fe-9000-4b82-a1e7-6bd013944e41)


To run it, just run the file [main](main.py) . Then graphs of the necessary dependencies will be plotted on the screen.
If it is necessary to change the points on these graphs, refer to the signature of the functions 
plot_num_of_cells and plot_len .

def plot_num_of_cells(R, L, nums) displays a graph of CC dependence on the partition parameter./
These parameters are set by an array of numbers of the integer type

def plot_len(R, lens, nums, k) displays graphs of the dependence of CC on the length of the pipe L and the relative deviation of CC from the true value for various partitioning parameters.
The x coordinates of the graph are set by the lens array. Accordingly, the splitting parameters are set by an array of numbers of the integer type.
The default parameter k is necessary if you also need to plot experimental data, that is, k sets CC at points in the lens array.

def create_x was created in order to create an array of experimental data from Table 1.1. (report)
