import numpy as np
import matplotlib.pyplot as plt


s = np.random.rand(10000, 10) < 0.5
ratio = np.cumsum(s,axis=0) / np.arange(1, 10000+1).reshape(-1, 1)
print(s)
print(ratio)


def plot_fig(cumulative_heads_ratio, heads_prob, save=True):
    # Get the number of tosses in a series
    num_tosses = cumulative_heads_ratio.shape[0]
    # Set the width and height in inches
    plt.figure(figsize=(8, 3.5))
    # Plot cumulative heads ratio
    plt.plot(cumulative_heads_ratio)
    # Plot the horizontal line of value `heads_prob`, with black dashed linetype
    plt.plot([0, num_tosses], [heads_prob, heads_prob], "k--", linewidth=2, label="{}%".format(round(heads_prob*100, 1)))
    # Plot the horizontal line of value 0.5 with black solid linetype
    plt.plot([0, num_tosses], [0.5, 0.5], "k-", label="50.0%")
    plt.xlabel("Number of coin tosses")
    plt.ylabel("Heads ratio")
    plt.legend(loc="lower right")
    # Set x ranges and y ranges
    xmin, xmax, ymin, ymax = 0, num_tosses, 0.42, 0.58
    plt.axis([xmin, xmax, ymin, ymax])
    # if save:
    #     save_fig("law_of_large_numbers_plot")
    plt.show()


plot_fig(ratio, 0.5)