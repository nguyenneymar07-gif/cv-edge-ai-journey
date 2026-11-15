import numpy as np
S = np.array([[2, 0], [0, 1]])
goc = np.deg2rad(30)
R = np.array([[np.cos(goc), -np.sin(goc)], [np.sin(goc), np.cos(goc)]])

for ten, A in [("S", S), ("R30", R)]:
    tri_rieng, vec_rieng = np.linalg.eig(A)
    print(ten, tri_rieng)
    print(vec_rieng)