import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("tong_hop.csv")
goc = df[df["bo_loc"] == "tho"][
    ["kich_ban", "file", "nhieu"]
]

goc = goc.rename(columns={"nhieu": "nhieu_goc"})
df = df.merge(goc, on=["kich_ban", "file"])
df["giam_nhieu_pct"] = (
    (df["nhieu_goc"] - df["nhieu"]) / df["nhieu_goc"]
) * 100

tong_hop = df[df["bo_loc"].isin(["tb5", "med5"])]
ket_qua = tong_hop.groupby(
    ["kich_ban", "bo_loc"]
)["giam_nhieu_pct"].agg(["mean", "std"])
print(ket_qua)

import matplotlib.pyplot as plt
import numpy as np

# Lấy dữ liệu
mean = ket_qua["mean"].unstack()
std = ket_qua["std"].unstack()

# Tạo vị trí cột
x = np.arange(len(mean))
rong = 0.35

# Vẽ biểu đồ
plt.bar(
    x - rong/2,
    mean["med5"],
    rong,
    label="med5",
    yerr=std["med5"],
    capsize=5
)

plt.bar(
    x + rong/2,
    mean["tb5"],
    rong,
    label="tb5",
    yerr=std["tb5"],
    capsize=5
)

# Trang trí
plt.xticks(x, mean.index)
plt.xlabel("Kịch bản")
plt.ylabel("Mức giảm nhiễu (%)")
plt.title("Trung bình trượt (tb5) so với median (med5) với cửa sổ 5")
plt.legend()
plt.grid(axis="y", alpha=0.3)
plt.figtext(
    0.5, 0.01,
    "Ghi chú: Thanh sai số biểu thị độ lệch chuẩn (STD) của các lần đo\nchoi và dichuyen (n=7),tructiep và giantiep (n=3)",
    ha="center",
    fontsize=9
)
plt.tight_layout(rect=[0, 0.05, 1, 1])
plt.savefig("image_and_video/bo_loc_A.png", dpi=150)
plt.tight_layout()
plt.show()
#unstack(): chuyển bo_loc từ MultiIndex thành các cột riêng biệt (med5, tb5).
#yerr=std["med5"]: thể hiện độ lệch chuẩn bằng thanh sai số.
#capsize=5: tạo hai đầu mút cho thanh sai số.