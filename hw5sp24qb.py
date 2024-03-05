# region imports
import hw5sp24qa as pta  # Import the provided module for plotting and friction factor calculation
import random as rnd
from matplotlib import pyplot as plt
import warnings

# Suppress runtime warnings
warnings.filterwarnings("ignore")
# endregion

# region functions
def ffPoint(Re, rr):
    """
    This function takes Re and rr as parameters and outputs a friction factor according to the following:
    1.  if Re>4000 use Colebrook Equation
    2.  if Re<2300 use f=64/Re
    3.  else calculate a probabilistic friction factor where the distribution has a mean midway between the prediction
        of the f=64/Re and Colebrook Equations and a standard deviation of 20% of this mean
    :param Re:  the Reynolds number
    :param rr:  the relative roughness
    :return:  the friction factor
    """
    if Re >= 4000:
        return pta.ff(Re, rr, CBEQN=True)  # Use Colebrook for turbulent flow
    if Re <= 2300:
        return pta.ff(Re, rr)  # Use laminar flow equation
    # Calculate the prediction of Colebrook and Laminar Equations in Transition region
    CBff = pta.ff(Re, rr, CBEQN=True)  # Colebrook Equation prediction for transition region
    Lamff = 64/Re  # Laminar Equation prediction for transition region
    mean = (CBff + Lamff) / 2
    sig = 0.2 * mean
    # Generate a random friction factor from a normal distribution for transition region
    return rnd.normalvariate(mean, sig)

def PlotPoint(Re, f, rr):
    """
    This function plots a specific point on the Moody diagram with a red icon.
    The icon is an upward triangle for transition flow (2300 < Re < 3500) or a circle otherwise.
    :param Re: Reynolds number
    :param f: friction factor
    :param rr: relative roughness  # Added parameter rr to use in the plot label
    """
    # Determine the marker style based on the flow regime
    if 2300 < Re < 3500:
        marker_style = '^'  # Upward triangle for transition flow
    else:
        marker_style = 'o'  # Circle for laminar or turbulent flow

    # Plot the point with the selected marker style in red
    plt.plot(Re, f, marker=marker_style, color='red', linestyle='None', markersize=10, label=f'Re={Re}, rr={rr}')

    # Assuming you're calling plotMoody to draw the diagram first
    pta.plotMoody()  # Draw the Moody diagram
    plt.legend()
    plt.show()

def main():
    """
    Main function to read user input and plot the point on the Moody diagram
    """
    Re = float(input("Enter the Reynolds number:  "))
    rr = float(input("Enter the relative roughness:  "))
    f = ffPoint(Re, rr)
    PlotPoint(Re, f, rr)  # Modified to pass rr as an argument to PlotPoint

# endregion

# region function calls
if __name__ == "__main__":
    main()
# endregion
