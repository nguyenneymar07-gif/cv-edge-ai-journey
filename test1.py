import cv2
import numpy as np
import statistics
from collections import deque
import sys


SO_MAU        = 300
CUA_SO        = 5
NGUONG_VAO    = 5.0
NGUONG_RA     = 3.0
NHAY_TOI_DA   = 15.0   # % nhảy tối đa cho phép giữa 2 khung
DIEN_TICH_MIN = 500
DOI_DIEN_TICH = 0.5    # đổi quá 50% thì nghi ngờ
MAX_BO_LIEN_TIEP = 5   # bỏ liên tiếp quá số này thì chấp nhận lại (tránh kẹt)

def nhieu(day):
    if len(day) < 3:
        return 0.0
    return statistics.pstdev([b - a for a, b in zip(day, day[1:])])

lich_su = deque(maxlen=CUA_SO)
tho, muot = [], []
huong = "GIUA"
sai_so_muot = None
dien_tich_truoc = None
bo_lien_tiep = 0
so_khung_bi_bo = 0

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise RuntimeError("Không mở được camera")

# Khóa phơi sáng: giá trị tùy driver, cần thử
cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)   # Linux V4L2: 1 = manual. Windows thử 0 hoặc -1
# cap.set(cv2.CAP_PROP_EXPOSURE, -6)     # chỉnh tay nếu cần

lower = np.array([140, 60, 100])
upper = np.array([175, 255, 255])
kernel = np.ones((5, 5), np.uint8)

import csv, time

f_csv = open("dichuyen_7.csv", "w", newline="")
ghi = csv.writer(f_csv)
ghi.writerow(["khung", "t", "dien_tich", "tho", "cu_tb5", "moi", "bi_bo", "huong"])

cu = deque(maxlen=5)   # bộ lọc cũ (trung bình trượt) chạy song song để so sánh
khung = 0
t0 = time.time()

while True:
    ok, frame = cap.read()
    if not ok:
        break
    
    khung += 1
    
    frame = cv2.flip(frame, 1)

    hsv = cv2.cvtColor(cv2.GaussianBlur(frame, (5, 5), 0), cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower, upper)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    biggest = max(contours, key=cv2.contourArea) if contours else None
    dien_tich = cv2.contourArea(biggest) if biggest is not None else 0

    if dien_tich > DIEN_TICH_MIN:
        x, y, w, h = cv2.boundingRect(biggest)
        rong = frame.shape[1]
        sai_so = ((x + w // 2) - rong / 2) / (rong / 2) * 100
        cu.append(sai_so)
        cu_tb = sum(cu) / len(cu)
        bi_bo = 0

        # --- Lớp 1: loại khung bất thường ---
        bat_thuong = False
        if sai_so_muot is not None:
            if abs(sai_so - sai_so_muot) > NHAY_TOI_DA:
                bat_thuong = True
        if dien_tich_truoc is not None:
            if abs(dien_tich - dien_tich_truoc) / dien_tich_truoc > DOI_DIEN_TICH:
                bat_thuong = True

        if bat_thuong and bo_lien_tiep < MAX_BO_LIEN_TIEP:
            bi_bo = 1
            
            bo_lien_tiep += 1
            so_khung_bi_bo += 1
            color = (0, 165, 255)  # cam: khung bị bỏ
        else:
            bo_lien_tiep = 0
            dien_tich_truoc = dien_tich
            color = (0, 255, 0)

            # --- Lớp 2: median, lớp 3: trung bình ---
            lich_su.append(sai_so)
            med = statistics.median(lich_su)
            sai_so_muot = med if sai_so_muot is None else \
                0.5 * med + 0.5 * sai_so_muot   # EMA nhẹ trên kết quả median

            tho.append(sai_so)
            muot.append(sai_so_muot)

            if huong == "GIUA":
                if sai_so_muot < -NGUONG_VAO:
                    huong = "SANG TRAI"
                elif sai_so_muot > NGUONG_VAO:
                    huong = "SANG PHAI"
            elif abs(sai_so_muot) < NGUONG_RA:
                huong = "GIUA"
                
        ghi.writerow([
        khung, round(time.time() - t0, 3), int(dien_tich),
        round(sai_so, 3), round(cu_tb, 3),
        "" if sai_so_muot is None else round(sai_so_muot, 3),
        bi_bo, huong,
        ])

        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
        if sai_so_muot is not None:
            cv2.putText(frame, f"{huong} ({sai_so_muot:.2f})",
                        (x, max(y - 10, 15)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
    else:
        lich_su.clear()
        cu.clear()
        sai_so_muot = None
        dien_tich_truoc = None
        bo_lien_tiep = 0
        huong = "GIUA"
        cv2.putText(frame, "KHONG THAY VAT", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

    cv2.imshow("webcam", frame)
    if (cv2.waitKey(1) & 0xFF == ord("q")) or len(tho) >= SO_MAU:
        break

cap.release()
cv2.destroyAllWindows()
f_csv.close()

if len(tho) > 2:
    print("so khung nhan  :", len(tho))
    print("so khung bi bo :", so_khung_bi_bo)
    print("min / max tho  :", min(tho), "/", max(tho))
    print("min / max muot :", min(muot), "/", max(muot))
    print("nhieu tho      :", nhieu(tho))
    print("nhieu muot     :", nhieu(muot))
else:
    print("Không đủ dữ liệu")