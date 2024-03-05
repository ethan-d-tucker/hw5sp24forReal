# region imports
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as pyplot
from math import floor, ceil
import time

# region functions
def RSquared(x, y, coeff):
    '''
    Calculate the R-squared value for a set of x,y data and a LeastSquares fit with polynomial having coefficients.
    '''
    AvgY = np.mean(y)
    SSTot = sum((yi - AvgY) ** 2 for yi in y)
    SSRes = sum((yi - Poly(xi, *coeff)) ** 2 for xi, yi in zip(x, y))
    RSq = 1 - SSRes / SSTot  # Calculate R-squared value
    return RSq

def Poly(xdata, *a):
    '''
    Calculate the value for a polynomial given xdata and coefficients of the polynomial.
    '''
    y = np.zeros_like(xdata)
    for i, ai in enumerate(a):
        y += ai * xdata ** i
    return y

def PlotLeastSquares(x, y, coeff, showpoints=True, npoints=500):
    '''
    Makes a formatted plot for a polynomial fit to the x,y data.
    '''
    Xmin, Xmax = min(x), max(x)
    Ymin, Ymax = min(y), max(y)

    xvals = np.linspace(Xmin, Xmax, npoints)
    yvals = Poly(xvals, *coeff)

    RSq = RSquared(x, y, coeff)  # Calculate R-squared value for the plot

    pyplot.plot(xvals, yvals, linestyle='dashed', color='black', linewidth=2)
    pyplot.title(r'$R^2={:0.3f}$'.format(RSq))
    pyplot.xlim(floor(Xmin * 10) / 10, ceil(Xmax * 10) / 10)
    pyplot.ylim(floor(Ymin), ceil(Ymax * 10) / 10)
    if showpoints:
        pyplot.plot(x, y, linestyle='none', marker='o', markerfacecolor='white', markeredgecolor='black', markersize=10)
    pyplot.xlabel('X values')
    pyplot.ylabel('Y values')
    pyplot.show()

def LeastSquaresFit(x, y, power=1):
    '''
    Fits x, y data with a polynomial of degree=power and returns the coefficients for the polynomial fit.
    '''
    coeff, _ = curve_fit(Poly, x, y, p0=np.ones(power + 1))
    return coeff


# I thought it would be cool for each graph to be on one page, so this is where I needed some extra ChatGPT help.
def main():
    x = np.array([0.05, 0.11, 0.15, 0.31, 0.46, 0.52, 0.70, 0.74, 0.82, 0.98, 1.17])
    y = np.array([0.956, 1.09, 1.332, 0.717, 0.771, 0.539, 0.378, 0.370, 0.306, 0.242, 0.104])

    # Get coefficients for linear and cubic fits
    coeff_linear = LeastSquaresFit(x, y, 1)
    coeff_cubic = LeastSquaresFit(x, y, 3)

    # Setup subplots
    fig, axs = pyplot.subplots(3, 1, figsize=(10, 15))

    # Plotting the linear fit
    PlotLeastSquaresSubplot(axs[0], x, y, coeff_linear, "Linear Fit", showpoints=True)

    # Plotting the cubic fit
    PlotLeastSquaresSubplot(axs[1], x, y, coeff_cubic, "Cubic Fit", showpoints=True)

    # Plotting both fits and original data on the same subplot
    xvals = np.linspace(min(x), max(x), 500)
    yvals_linear = Poly(xvals, *coeff_linear)
    yvals_cubic = Poly(xvals, *coeff_cubic)
    axs[2].plot(xvals, yvals_linear, label=f'Linear Fit, $R^2$={RSquared(x, y, coeff_linear):.3f}', linestyle='--')
    axs[2].plot(xvals, yvals_cubic, label=f'Cubic Fit, $R^2$={RSquared(x, y, coeff_cubic):.3f}', linestyle='-.')
    axs[2].scatter(x, y, label='Original Data', color='red', zorder=5)
    axs[2].set_title('Linear and Cubic Fits to Data')
    axs[2].set_xlabel('X values')
    axs[2].set_ylabel('Y values')
    axs[2].legend()

    pyplot.tight_layout()
    pyplot.show()

def PlotLeastSquaresSubplot(ax, x, y, coeff, title, showpoints=True, npoints=500):
    Xmin, Xmax = min(x), max(x)
    Ymin, Ymax = min(y), max(y)

    xvals = np.linspace(Xmin, Xmax, npoints)
    yvals = Poly(xvals, *coeff)

    RSq = RSquared(x, y, coeff)  # Calculate R-squared value for the plot

    ax.plot(xvals, yvals, linestyle='dashed', color='black', linewidth=2)
    ax.set_title(f'{title}, $R^2$={RSq:.3f}')
    ax.set_xlim(floor(Xmin * 10) / 10, ceil(Xmax * 10) / 10)
    ax.set_ylim(floor(Ymin), ceil(Ymax * 10) / 10)
    if showpoints:
        ax.plot(x, y, linestyle='none', marker='o', markerfacecolor='white', markeredgecolor='black', markersize=10)
    ax.set_xlabel('X values')
    ax.set_ylabel('Y values')

if __name__ == "__main__":
    main()


