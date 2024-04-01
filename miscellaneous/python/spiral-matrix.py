def spiral_matrix(n):
    N = n ** 2
    top = 0
    bottom = n - 1
    left = 0
    right = n - 1
    i = 0
    j = 0
    di = 0
    dj = 1
    matrix = [n * [0] for _ in range(n)]
    matrix[0][0] = 1
    for k in range(2, N + 1):
        if top <= i + di <= bottom and left <= j + dj <= right and matrix[i + di][j + dj] == 0:
            i += di
            j += dj
        else:
            di, dj = dj, -di
            i, j = i + di, j + dj
        matrix[i][j] = k
    return matrix