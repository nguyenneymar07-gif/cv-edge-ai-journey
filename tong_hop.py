"""
Tổng hợp nhiều lần đo: tính nhiễu / đỉnh / độ trễ cho nhiều bộ lọc,
rồi in bảng trung bình ± độ lệch giữa các lần đo.

Cách dùng:
    python tong_hop.py                    # đọc mọi file *.csv trong thư mục (trừ tong_hop.csv)
    python tong_hop.py binhthuong_*.csv choi_*.csv dichuyen_*.csv

Đặt tên file theo dạng  <kich_ban>_<so>.csv, ví dụ:
    binhthuong_1.csv, binhthuong_2.csv, choi_1.csv, dichuyen_1.csv
Phần <kich_ban> (bỏ đuôi _số) dùng để gom các lần đo cùng kịch bản.
"""
import sys
import glob
import os
import re

import numpy as np
import pandas as pd

CUA_SO = (3, 5, 10)
MAX_TRE = 10  # thử độ trễ tối đa 10 khung


def nhieu(x):
    """Độ lệch chuẩn của hiệu giữa hai mẫu liên tiếp (giống hàm trong code đo)."""
    d = np.diff(x)
    return float(np.std(d)) if len(d) > 1 else 0.0


def tre(tho, loc):
    """
    Ước lượng độ trễ (số khung): tìm k sao cho loc[t] gần nhất với tho[t-k].
    Chỉ có ý nghĩa khi vật DI CHUYỂN; vật đứng yên thì kết quả không đáng tin.
    """
    best_k, best_err = 0, np.inf
    n = len(tho)
    for k in range(MAX_TRE + 1):
        if n - k < 5:
            break
        err = np.mean((loc[k:] - tho[: n - k]) ** 2)
        if err < best_err:
            best_k, best_err = k, err
    return best_k


def cac_bo_loc(df):
    """Trả về dict {tên bộ lọc: chuỗi numpy} tính từ cột 'tho' (cùng dữ liệu thô)."""
    tho = df["tho"]
    out = {"tho": tho.to_numpy(float)}
    for n in CUA_SO:
        out[f"tb{n}"] = tho.rolling(n, min_periods=1).mean().to_numpy(float)
        out[f"med{n}"] = tho.rolling(n, min_periods=1).median().to_numpy(float)
    # bộ lọc "mới" đã ghi sẵn trong CSV (loại khung + median + EMA)
    if "moi" in df.columns:
        moi = pd.to_numeric(df["moi"], errors="coerce").ffill().bfill()
        out["moi(file)"] = moi.to_numpy(float)
    return out


def kich_ban_tu_ten(path):
    stem = os.path.splitext(os.path.basename(path))[0]
    return re.sub(r"[_\-]?\d+$", "", stem) or stem


def main():
    files = sys.argv[1:]
    if not files:
        files = [f for f in glob.glob("*.csv") if os.path.basename(f) != "tong_hop.csv"]
    else:
        files = [g for pat in files for g in glob.glob(pat)]
    files = sorted(set(files))
    if not files:
        sys.exit("Không tìm thấy file CSV nào.")

    rows = []
    thong_tin_file = []
    for f in files:
        df = pd.read_csv(f)
        if "tho" not in df.columns or len(df) < 20:
            print(f"Bỏ qua {f}: thiếu cột 'tho' hoặc quá ít khung ({len(df)})")
            continue
        kb = kich_ban_tu_ten(f)
        bo = int(df["bi_bo"].sum()) if "bi_bo" in df.columns else 0
        thong_tin_file.append({"kich_ban": kb, "file": f, "so_khung": len(df), "khung_bi_bo": bo})

        series = cac_bo_loc(df)
        tho = series["tho"]
        for ten, loc in series.items():
            rows.append({
                "kich_ban": kb,
                "file": f,
                "bo_loc": ten,
                "nhieu": nhieu(loc),
                "max_abs": float(np.max(np.abs(loc))),
                "tre": 0 if ten == "tho" else tre(tho, loc),
            })

    if not rows:
        sys.exit("Không có dữ liệu hợp lệ.")

    kq = pd.DataFrame(rows)
    info = pd.DataFrame(thong_tin_file)

    print("\n=== Số lần đo mỗi kịch bản ===")
    print(info.groupby("kich_ban").agg(
        so_lan=("file", "count"),
        khung_tb=("so_khung", "mean"),
        bi_bo_tb=("khung_bi_bo", "mean"),
    ).round(1).to_string())

    thu_tu = ["tho"] + [f"tb{n}" for n in CUA_SO] + [f"med{n}" for n in CUA_SO] + ["moi(file)"]

    def fmt(mean, std, n):
        return f"{mean:8.3f} ± {0 if np.isnan(std) else std:6.3f}"

    for kb, g in kq.groupby("kich_ban"):
        so_lan = g["file"].nunique()
        print(f"\n=== Kịch bản: {kb}  ({so_lan} lần đo) ===")
        if so_lan < 3:
            print("  (cảnh báo: dưới 3 lần đo, độ lệch chưa đáng tin)")
        tho_nhieu = g[g["bo_loc"] == "tho"]["nhieu"].mean()
        print(f"{'bo_loc':<10}{'nhieu (tb ± sd)':>22}{'giam so voi tho':>18}"
              f"{'max|x| (tb ± sd)':>22}{'tre (khung)':>14}")
        for ten in thu_tu:
            h = g[g["bo_loc"] == ten]
            if h.empty:
                continue
            n_m, n_s = h["nhieu"].mean(), h["nhieu"].std()
            x_m, x_s = h["max_abs"].mean(), h["max_abs"].std()
            giam = "" if ten == "tho" or tho_nhieu == 0 else f"{(1 - n_m / tho_nhieu) * 100:6.1f} %"
            print(f"{ten:<10}{fmt(n_m, n_s, so_lan):>22}{giam:>18}"
                  f"{fmt(x_m, x_s, so_lan):>22}{h['tre'].mean():>14.1f}")

    kq.to_csv("tong_hop.csv", index=False)
    print("\nĐã lưu chi tiết từng lần đo vào tong_hop.csv")
    print("Ghi chú: cột 'tre' chỉ đáng tin ở kịch bản vật di chuyển.")
    print("Muốn kết luận hai bộ lọc khác nhau: chênh lệch trung bình phải lớn hơn độ lệch (sd) giữa các lần đo.")


if __name__ == "__main__":
    main()