# region imports
import numpy as np
from scipy.optimize import fsolve
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import warnings

#As always, psuedo code was written and given to ChatGPT, then used to create this code.
# endregion

# I wanna ignore the warnings.
warnings.filterwarnings("ignore")

# region functions
def ff(Re, rr, CBEQN=False):
    """
    This function calculates the friction factor for a pipe based on the
    notion of laminar, turbulent and transitional flow.
    :param Re: the Reynolds number under question.
    :param rr: the relative pipe roughness (expect between 0 and 0.05)
    :param CBEQN:  boolean to indicate if I should use Colebrook (True) or laminar equation
    :return: the (Darcy) friction factor
    """
    if CBEQN:
        # Implementing Colebrook equation
        cb = lambda f: 1 / np.sqrt(f) + 2.0 * np.log10((rr / 3.7) + (2.51 / (Re * np.sqrt(f)))) - 0
        result = fsolve(cb, 0.02)  # Initial guess for f is 0.02
        return result[0]
    else:
        return 64 / Re


def plotMoody(plotPoint=False, pt=(0, 0)):
    """
    This function produces the Moody diagram for a Re range from 1 to 10^8 and
    for relative roughness from 0 to 0.05 (20 steps).  The laminar region is described
    by the simple relationship of f=64/Re whereas the turbulent region is described by
    the Colebrook equation.
    :return: just shows the plot, nothing returned
    """
    # Creating logspace arrays for Reynolds number ranges
    ReValsCB = np.logspace(np.log10(4000), 8, 20)  # for turbulent flow
    ReValsL = np.logspace(np.log10(600.0), np.log10(2000.0), 20)  # for laminar flow
    ReValsTrans = np.logspace(np.log10(2000), np.log10(4000), 20)  # for transition flow

    # Creating array for range of relative roughnesses
    rrVals = np.array(
        [0, 1E-6, 5E-6, 1E-5, 5E-5, 1E-4, 2E-4, 4E-4, 6E-4, 8E-4, 1E-3, 2E-3, 4E-3, 6E-3, 8E-8, 1.5E-2, 2E-2, 3E-2,
         4E-2, 5E-2])

    # Calculating friction factor in the laminar and transition range
    ffLam = np.array([ff(Re, 0, False) for Re in ReValsL])
    ffTrans = np.array([ff(Re, 0.02, True) for Re in ReValsTrans])

    # Calculating friction factor values for each rr at each Re for turbulent range
    ffCB = np.array([[ff(Re, rr, True) for Re in ReValsCB] for rr in rrVals])

    # Constructing the plot with loglog for laminar, transition, and turbulent parts
    plt.loglog(ReValsL, ffLam, 'b', label='Laminar Flow')
    plt.loglog(ReValsTrans, ffTrans, 'g--', label='Transition Flow')
    for idx, rr in enumerate(rrVals):
        plt.loglog(ReValsCB, ffCB[idx], 'k', label=f'rr={rr}' if idx in [0, len(rrVals) - 1] else "")

    # Plot styling and annotations
    plt.xlim(600, 1E8)
    plt.ylim(0.008, 0.10)
    plt.xlabel("Reynolds number (Re)", fontsize=16)
    plt.ylabel("Friction factor (f)", fontsize=16)
    plt.title("Moody Diagram")
    ax = plt.gca()
    ax.tick_params(axis='both', which='both', direction='in', top=True, right=True, labelsize=12)
    ax.yaxis.set_minor_formatter(FormatStrFormatter("%.3f"))
    plt.grid(which='both')

    if plotPoint:
        plt.plot(pt[0], pt[1], 'ro', markersize=12, markeredgecolor='red', markerfacecolor='none')

    plt.legend()
    plt.show()


def main():
    plotMoody()


# endregion

# region function calls
if __name__ == "__main__":
    main()
# endregion
