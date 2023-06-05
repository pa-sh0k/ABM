import json
from math import sqrt
with open("base_mm.json", "r") as f:
    base_mm = json.loads(f.read())

with open("nn_mm.json", "r") as f:
    nn_mm = json.loads(f.read())

N = len(nn_mm)

D = [nn_mm[i] - base_mm[i] for i in range(N)]

D_bar = sum(D) / N

S_D__squared = sum([(D[i] - D_bar)**2 for i in range(N)]) / (N - 1)

T = (D_bar - 0) / sqrt(S_D__squared / N)

print(T)

