import pandas as pd
import matplotlib.pyplot as plt
import statistics

def nhieu(s):
    s = s.dropna().tolist()
    if len(s) < 3:
        return 0.0
    return statistics.pstdev([b - a for a, b in zip(s, s[1:])])

import sys
ten = "choi_7.csv"
df = pd.read_csv(ten)
fig, ax = plt.subplots(2, 1, figsize=(11, 7), sharex=True)

ax[0].plot(df["khung"], df["tho"], color="lightgray", label="thô")
ax[0].plot(df["khung"], df["cu_tb5"], color="tab:red", label="cũ: trung bình 5")
ax[0].plot(df["khung"], df["moi"], color="tab:green", label="mới: loại + median + EMA")
bo = df[df["bi_bo"] == 1]
ax[0].scatter(bo["khung"], bo["tho"], color="orange", marker="x", zorder=5, label="khung bị bỏ")
ax[0].axhline(5, ls="--", c="k", lw=0.5)
ax[0].axhline(-5, ls="--", c="k", lw=0.5)
ax[0].set_ylabel("sai số (%)")
ax[0].legend()

ax[1].plot(df["khung"], df["dien_tich"], color="tab:blue")
ax[1].set_ylabel("diện tích contour")
ax[1].set_xlabel("khung")

plt.tight_layout()
plt.savefig(ten.replace(".csv", ".png"), dpi=150)
plt.show()

print("nhiễu thô  :", round(nhieu(df["tho"]), 3))
print("nhiễu cũ   :", round(nhieu(df["cu_tb5"]), 3))
print("nhiễu mới  :", round(nhieu(df["moi"]), 3))
print("khung bị bỏ:", int(df["bi_bo"].sum()), "/", len(df))
print("max |cũ|   :", df["cu_tb5"].abs().max(), " max |mới|:", df["moi"].abs().max())