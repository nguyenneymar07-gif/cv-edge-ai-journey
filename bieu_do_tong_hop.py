import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("tong_hop.csv")
goc = df[df["bo_loc"] == "tho"][
    ["kich_ban", "file", "nhieu"]
]

goc = goc.rename(columns={"nhieu": "nhieu_goc"})
df = df.merge(goc, on=["kich_ban", "file"])
df["giam_nhieu"] = df["nhieu_goc"] - df["nhieu"]

tong_hop = df[df["bo_loc"].isin(["tb5", "med5"])]
ket_qua = tong_hop.groupby(
    ["kich_ban", "bo_loc"]
)["giam_nhieu"].agg(["mean", "std"])
print(ket_qua)
