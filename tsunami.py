"""Main interface to the Fortran simulator."""

import os.path
import subprocess
from sys import platform

import matplotlib
# use an interactive backend
matplotlib.use("QtAgg")
import matplotlib.pyplot as plt
import numpy as np

FORTRAN_COMPILER = "gfortran"
FORTRAN_SOURCE = "tsunami.f90"

TSUNAMI_EXECUTABLE = "tsunami"
TSUNAMI_RESULTS_FILE = "tsunami_results.txt"
WATER_HEIGHT_FIG = "water_height.png"

def compile_program():
    """Compile the Fortran program."""
    subprocess.run([FORTRAN_COMPILER, FORTRAN_SOURCE, "-o", TSUNAMI_EXECUTABLE])


def run_program(output_file: str | None = None):
    """Run the Fortran program."""
    # compile the program if the executable does not exist
    if not os.path.exists(TSUNAMI_EXECUTABLE):
        compile_program()

    # run the executable and write the output to a file if output_file is provided
    if output_file:
        subprocess.run(["./" + TSUNAMI_EXECUTABLE], stdout=open(output_file, "w"))
    else:
        subprocess.run(["./" + TSUNAMI_EXECUTABLE])


def visualize():
    """Generate a plot of the results."""
    # run the program if the results file does not exist
    if not os.path.exists(TSUNAMI_RESULTS_FILE):
        run_program(TSUNAMI_RESULTS_FILE)

    input_file = TSUNAMI_RESULTS_FILE

    if platform == "win32":
        unicodeVar = "utf-16"
    else:
        unicodeVar = "utf-8"

    matplotlib.use("Agg")
    matplotlib.rcParams.update({"font.size": 16})

    # read data into a list
    data = [
        line.rstrip().split()
        for line in open(input_file, encoding=unicodeVar).readlines()
    ]

    time = [float(line[0]) for line in data]
    h = np.array([[float(x) for x in line[1:]] for line in data])
    x = np.arange(1, h.shape[1] + 1)
    time_steps = [0, 25, 50, 75]

    fig = plt.figure(figsize=(8, 10))
    axes = [
        plt.subplot2grid((4, 1), (row, 0), colspan=1, rowspan=1) for row in range(4)
    ]

    for ax in axes:
        n = axes.index(ax)
        ax.plot(x, h[time_steps[n], :], "b-")
        ax.fill_between(x, 0, h[time_steps[n], :], color="b", alpha=0.4)
        ax.grid()
        ax.set_xlim(1, 100)
        ax.set_ylim(0, 1)
        ax.set_ylabel("Height", fontsize=16)
        ax.set_xticks([25, 50, 75, 100])
        ax.set_yticks([0, 0.25, 0.5, 0.75, 1])

    for ax in axes:
        n = axes.index(ax)
        ax.set_title("Time step " + "%3i" % time_steps[n])

    for ax in axes[:-1]:
        ax.set_xticklabels([])

    axes[3].set_xlabel("", fontsize=16)
    axes[-1].set_xlabel("Spatial grid index")

    plt.savefig(WATER_HEIGHT_FIG)
