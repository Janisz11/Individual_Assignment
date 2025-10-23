import random

def random_matrix(n, seed=1234):
   
    random.seed(seed)
    return [[random.random() for _ in range(n)] for _ in range(n)]


def matmul_basic(A, B):
  
    n = len(A)
    C = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            s = 0.0
            for k in range(n):
                s += A[i][k] * B[k][j]
            C[i][j] = s
    return C
