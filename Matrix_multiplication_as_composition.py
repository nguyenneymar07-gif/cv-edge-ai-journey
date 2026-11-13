import numpy as np
goc = np.deg2rad(30)
R = np.array([[np.cos(goc), -np.sin(goc)],
              [np.sin(goc),  np.cos(goc)]])
diem = np.array([[1, 0], [0, 1], [1, 1]]).T   # mỗi CỘT là một điểm
print(R @ diem)

xoay = R @ diem
dai_truoc = np.linalg.norm(diem, axis = 0)
dai_sau   = np.linalg.norm(xoay, axis = 0)
print("truoc:\n ",dai_truoc)
print("sau:\n ",dai_sau)
print(np.allclose(dai_truoc,dai_sau))

def matran_xoay(do):
    goc = np.deg2rad(do)
    return np.array([[np.cos(goc), -np.sin(goc)],
                     [np.sin(goc),  np.cos(goc)]])

r30 = matran_xoay(30)
r60 = matran_xoay(60)
print("r30: \n",r30)
print("r30 + r30: \n",r30 @ r30)
print("r60: \n",r60)
print(np.allclose(r30 @ r30, r60))

S = 2 * np.eye(2)
print("R @ S =\n", R @ S)
print("S @ R =\n", S @ R)
print(np.allclose(R @ S, S @ R))  