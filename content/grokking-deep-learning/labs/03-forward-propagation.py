import numpy as np

inputs = np.array([1., 2., 3.])

weights_1 = np.array([
    [0.1, 0.2, 0.3, 0.4],
    [0.5, 0.6, 0.7, 0.8],
    [0.9, 1.0, 1.1, 1.2],
])

weights_2 = np.array([
    [0.1, 0.2],
    [0.3, 0.4],
    [0.5, 0.6],
    [0.7, 0.8],
])

layer_1 = np.dot(inputs, weights_1)
prediction = np.dot(layer_1, weights_2)

print(inputs.shape)
print(layer_1.shape)
print(prediction.shape)
print(prediction)