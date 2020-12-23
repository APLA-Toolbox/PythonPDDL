import os
import glob
import matplotlib as mpl

mpl.use("TkAgg")
mpl.set_loglevel("WARNING")
import matplotlib.pyplot as plt

plt.style.use("ggplot")


def get_all_pddl_from_data():
    tested_files = []
    domains_problems = []
    i = 0
    for root, _, files in os.walk("data/", topdown=False):
        for name in files:
            if ".gitkeep" in name:
                continue
            tested_files.append(os.getcwd() + "/" + os.path.join(root, name))
            if i % 2 != 0:
                domains_problems.append((tested_files[i - 1], tested_files[i]))
            i += 1
    return domains_problems


def plot_data(times, total_nodes, plot_title):
    plt.plot(total_nodes, times, "b:o")
    plt.xlabel("Number of opened nodes")
    plt.ylabel("Planning computation time")
    plt.title(plot_title)
    plt.xscale('symlog')
    plt.yscale('log')
    plt.grid(True)
    plt.show()


def scatter_data(times, total_nodes, plot_title):
    plt.scatter(total_nodes, times)
    plt.xlabel("Number of opened nodes")
    plt.ylabel("Planning computation time")
    plt.title(plot_title)
    plt.xscale('symlog')
    plt.yscale('log')
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    print(get_all_pddl_from_data())
