import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":
    data = []
    with open("data/12.txt") as f:
        for line in f:
            data.append(line.strip())

    negative_index = [value.find("-") for value in data]

    new_data = []
    for value, neg in zip(data, negative_index):
        if neg == 0:
            new_val = float(value[1:]) * -1.0
        else:
            new_val = float(value)

        new_data.append(new_val)

    new_data = np.array(new_data)


    reference = np.full(len(new_data), 0.3)

    plt.plot(new_data)
    plt.plot(reference)
    plt.title("Error")
    plt.xlabel("Samples")
    plt.ylabel("Error")
    plt.grid(True)
    plt.show()

