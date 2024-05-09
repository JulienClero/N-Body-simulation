# N-Body-simulation
My first attempt at making a N-Body simulation running in Python. It as more functionalities than GALAXSIM but isn't parallelized and isn't interactive.

# Functioning
The simulation uses cartesian coordinates for physics and computations. You have the choice to use either RK-2 solver or RK-4 solver, there is no error control nor variable timestep. Timestep is ofcourse choosable and you have to precise it into the simulation data list.

The simulation work as such :
- A Python list contains lists of dictionaries (Each list is a simulation preset), each dictionary contains all the informations about a body (Initial conditions, Mass, Radius, Coefficient of drag,...)
- A Tkinter UI allows you to choose which preset to load and with which solver.
- Computes it and gives you important values in the console such as the minimal distance between two bodies.

# Future

- Parallelization is an objective 
- Implement a more rigorous collision system
