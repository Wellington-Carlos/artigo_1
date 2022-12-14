"""
Author: Trevor Amestoy
Cornell University
Spring 2022

Contains scripts used to solve and plot the behavior of the Lotka-Volterra
system of ODEs.
"""
# Import core modules
import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate

# Import custome functions
from lotka_volterra_functions import type_II_equilibrium
from lotka_volterra_functions import type_II_lotka_volterra

################################################################################
def plot_interactive_trajectories(a, b, c, d, h, K, m, z = 0):
    """
    Plots the trajectories of many initial conditions integrated over a provided
    ODE.
    Parameters:
    -----------
    a: float
        The availability of prey to the predator.
    b: float
        The prey death rate.
    c: float
        The rate that prey is converted to new predators.
    d: float
        The predator death rate.
    h: float
        The handling time of the predator after catching prey.
    K: float
        The prey population carrying capacity.
    m: float
        The predator interference rate.

    Returns:
    --------
    None.
    """

    # ODE
    ode_function = type_II_lotka_volterra

    # Initial populations
    initial_conditions = np.linspace(0.1, 5, 5)

    # Group parameters
    params = (a, b, c, d, h, K, m, z)

    # Define a set of colors for each initial condition trajectory
    trajectory_colors = plt.cm.turbo(np.linspace(0.1, 1, len(initial_conditions)))

    # Define a time range to integrate the system over
    t = np.linspace(0, 150, 1000)

    # Solve for the equilibrium point
    EQ = type_II_equilibrium(params)

    for value, line_color in zip(initial_conditions, trajectory_colors):

        # Starting point for each trajectory
        P0 = [E*value for E in EQ]

        # Integrate the ODE
        Path = integrate.odeint(ode_function, P0, t, (params))

        # Plot trajectory
        plt.plot(Path[:,0], Path[:,1], color = line_color, label = '(%.f, %.f)' % (P0[0], P0[1]))

    ymax = plt.ylim(ymin=0)[1]
    xmax = plt.xlim(xmin=0)[1]

    # Define number of grid points
    grid_points = 20

    # Define x and y ranges
    x = np.linspace(0, xmax, grid_points)
    y = np.linspace(0, ymax, grid_points)

    # Meshgrid
    X,Y = np.meshgrid(x,y)

    # Calculate growth rate at each grid point
    growth_X, growth_Y = ode_function([X,Y], 0, a, b, c, d, h, K, m)

    # Direction at each grid point; hypotenuse of prey direction and predator Direction
    growth_direction = np.hypot(growth_X, growth_Y)

    # Avoid division by zero
    growth_direction[growth_direction == 0] = 1

    # Normalize arrow length
    growth_X /= growth_direction
    growth_Y /= growth_direction

    plt.title('Trajet??rias populacionais')

    # Add arrows via quiver
    quiver = plt.quiver(X, Y, growth_X, growth_Y, growth_direction, pivot = 'mid', cmap = plt.cm.viridis)

    # Labels and axis limits
    plt.xlabel('Presas')
    plt.ylabel('Predadores')
    plt.legend(bbox_to_anchor = (1.05, 1.0), title = "Popula????o Inicial\n (Presa, Predador)")
    plt.grid()
    plt.xlim(0, xmax)
    plt.ylim(0, ymax)
    plt.show()

    return



################################################################################

def plot_time_trajectories(a, b, c, d, h, K, m, z = 0):
    """
    Plots both predator and prey populations through time.

    Parameters:
    -----------
    a: float
        The availability of prey to the predator.
    b: float
        The prey death rate.
    c: float
        The rate that prey is converted to new predators.
    d: float
        The predator death rate.
    h: float
        The handling time of the predator after catching prey.
    K: float
        The prey population carrying capacity.
    m: float
        The predator interference rate.


    Returns:
    --------
    None.
    """

    # ODE
    ode_function = type_II_lotka_volterra

    # Initial populations
    initial_conditions = np.linspace(0.1, 5, 5)

    # Group parameters
    params = (a, b, c, d, h, K, m, z)

    # Define a set of colors for each initial condition trajectory
    trajectory_colors = plt.cm.turbo(np.linspace(0.1, 1, len(initial_conditions)))

    # Define a time range to integrate the system over
    t = np.linspace(0, 150, 1000)

    # Solve for the equilibrium point
    EQ = type_II_equilibrium(params)

    # Initialize two subplots
    fig, ax = plt.subplots(2,1)

    for value, line_color in zip(initial_conditions, trajectory_colors):

        # Starting point for each trajectory
        P0 = [E*value for E in EQ]

        # Integrate the ODE
        Path = integrate.odeint(ode_function, P0, t, (params))

        # Plot time-trajectory
        ax[0].plot(t, Path[:,0], color = line_color, label = 'P0=(%.f)' % (P0[0]))
        ax[1].plot(t, Path[:,1], color = line_color, label = 'P0=(%.f)' % (P0[1]))

    ax[0].grid()
    ax[1].grid()
    ax[0].set_xlabel('Tempo')
    ax[0].set_ylabel('Presas')
    ax[1].set_xlabel('Tempo')
    ax[1].set_ylabel('Predadores');

    plt.suptitle('Popula????o vs tempo')

    # Labels and axis limits
    plt.show()

    return
