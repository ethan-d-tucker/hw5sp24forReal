# region imports
import numpy as np
from scipy.integrate import solve_ivp  # This is the missing import for solving ODE systems
import matplotlib.pyplot as plt
# endregion

# region functions
def ode_system(t, X, *params):
    '''
    Define the system of ODEs for the valve dynamics.
    '''
    # Unpack the parameters
    A, Cd, ps, pa, V, beta, rho, Kvalve, m, y = params

    # Unpack the state variables (added unpacking of state variables)
    x, xdot, p1, p2 = X

    # Calculate derivatives (added calculation of derivatives)
    xddot = (p1 - p2) * A / m  # Acceleration of the piston
    p1dot = y * Kvalve * (ps - p1) / rho - xdot / (V * beta)  # Rate of change of pressure p1
    p2dot = y * Kvalve * (p2 - pa) / rho + xdot / (V * beta)  # Rate of change of pressure p2

    # Return the derivatives as a list
    return [xdot, xddot, p1dot, p2dot]

def main():
    '''
    Main function to solve the ODE system and plot the results.
    '''
    # Time span for the simulation (set up time array for simulation)
    t_span = (0, 0.02)
    t_eval = np.linspace(0, 0.02, 200)

    # Physical constants for the system (added correct argument values)
    myargs = (4.909E-4, 0.6, 1.4E7, 1.0E5, 1.473E-4, 2.0E9, 850.0, 2.0E-5, 30, 0.002)

    # Initial conditions (added initial conditions)
    ic = [0, 0, 1.0E5, 1.0E5]

    # Solve the system of ODEs (added solve_ivp function call)
    sln = solve_ivp(ode_system, t_span, ic, args=myargs, t_eval=t_eval)

    # Unpack the results (corrected the indexing of the solution)
    xvals = sln.y[0]
    xdotvals = sln.y[1]
    p1vals = sln.y[2]
    p2vals = sln.y[3]

    # Plot the results (corrected the plotting code)
    plt.figure(figsize=(12, 6))

    plt.subplot(2, 1, 1)
    plt.plot(t_eval, xvals, 'r-', label='$x$')
    plt.ylabel('Position ($x$)')
    plt.legend(loc='upper left')
    ax2 = plt.twinx()
    ax2.plot(t_eval, xdotvals, 'b-', label='$\dot{x}$')
    ax2.set_ylabel('Velocity ($\dot{x}$)')
    ax2.legend(loc='upper right')

    plt.subplot(2, 1, 2)
    plt.plot(t_eval, p1vals, 'b-', label='$P_1$')
    plt.plot(t_eval, p2vals, 'r-', label='$P_2$')
    plt.xlabel('Time (s)')
    plt.ylabel('Pressure (Pa)')
    plt.legend(loc='upper right')

    plt.tight_layout()
    plt.show()

# endregion

# region function calls
if __name__ == "__main__":
    main()
# endregion
