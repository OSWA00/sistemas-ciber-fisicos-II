import numpy as np
import matplotlib.pyplot as plt
from least_squared_errors import calculate_normal_equation, predict, data_to_X_and_y

if __name__ == "__main__":

    paths = ["data1.txt", "data2.txt", "data3.txt"]

    datasets = [np.loadtxt(f"data/{path}") for path in paths]

    fig_index = 0

    for dataset in datasets:
        X, y = data_to_X_and_y(dataset)
        theta = calculate_normal_equation(X, y)
        predictions = predict(X, theta)

        fig = plt.figure(figsize=(8, 6))
        plt.plot(X, y, "b.")
        plt.plot(X, predictions, "c-")
        plt.xlabel("X")
        plt.ylabel("y")
        plt.savefig(f"results/{fig_index}.png")
        fig_index += 1
