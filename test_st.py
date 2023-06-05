import json
from math import sqrt

with open("base_mm.json", "r") as f:
    base_mm = json.loads(f.read())

with open("nn_mm.json", "r") as f:
    nn_mm = json.loads(f.read())

N = len(nn_mm)

X, Y = nn_mm, base_mm

X_bar = sum(X) / N
Y_bar = sum(Y) / N

S_X__squared = sum([(X[i] - X_bar)**2 for i in range(N)]) / (N - 1)
S_Y__squared = sum([(Y[i] - Y_bar)**2 for i in range(N)]) / (N - 1)

"""
S_X__squared / S_Y__squared = 1.3367279817001143 < 2
"""

S_pooled = sqrt((S_X__squared + S_Y__squared) * (N - 1) / (2*N - 1))

T = (X_bar - Y_bar) / (S_pooled * sqrt(2/N))

print(T)

"""
T = 16.819282040554487
"""