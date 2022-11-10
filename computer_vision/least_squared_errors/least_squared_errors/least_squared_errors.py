import numpy as np


def data_to_X_and_y(data: np.array):
    X = data[:, 0]
    y = data[:, 1]
    n_samples = X.shape[0]
    X = np.reshape(X, (n_samples, 1))
    y = y.reshape(n_samples, 1)
    return X, y


def calculate_normal_equation(X: np.array, y: np.array) -> np.array:
    n_samples = X.shape[0]
    X = np.append(X, np.ones((n_samples, 1)), axis=1)

    theta = np.dot(np.linalg.inv(np.dot(X.T, X)), np.dot(X.T, y))

    return theta


def predict(X: np.array, theta: np.array) -> np.array:
    X = np.append(X, np.ones((X.shape[0], 1)), axis=1)
    return np.dot(X, theta)
