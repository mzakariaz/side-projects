import numpy as np

def calculate(array):
    if len(array) != 9:
        raise ValueError("List must contain nine numbers.")
    array = np.reshape(array, (3, 3))
    calculations = {
        'mean': [[x for x in np.mean(array, axis = 0)], [x for x in np.mean(array, axis = 1)], np.mean(array)],
        'variance': [[x for x in np.var(array, axis = 0)], [x for x in np.var(array, axis = 1)], np.var(array)],
        'standard deviation': [[x for x in np.std(array, axis = 0)], [x for x in np.std(array, axis = 1)], np.std(array)],
        'max': [[x for x in np.max(array, axis = 0)], [x for x in np.max(array, axis = 1)], np.max(array)],
        'min': [[x for x in np.min(array, axis = 0)], [x for x in np.min(array, axis = 1)], np.min(array)],
        'sum': [[x for x in np.sum(array, axis = 0)], [x for x in np.sum(array, axis = 1)], np.sum(array)]
        }
    return calculations