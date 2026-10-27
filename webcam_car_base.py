import cv2
from collections import deque
import statistics

def nhieu(day):
    return statistics.pstdev([b - a for a, b in zip(day, day[1:])])

lich_su = deque(maxlen=10)
tho  = []
muot = []

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise RuntimeError("Không mở được camera")

lower = (140, 60, 100)
upper = (175, 255, 255)

while True:
    ok, frame = cap.read()
    if not ok:
        break
    
    blurred_frame = cv2.GaussianBlur(frame, (5, 5), 0)
    hsv = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower, upper)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    biggest = max(contours, key=cv2.contourArea) if contours else None
    if biggest is not None and cv2.contourArea(biggest) > 500:
        x, y, w, h = cv2.boundingRect(biggest)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2 )
        toa_do_tam = (x + w // 2, y + h //2)
        rong_khung = frame.shape[1]
        lech = toa_do_tam[0] - rong_khung / 2
        sai_so = lech / (rong_khung / 2) * 100
        lich_su.append(sai_so)
        sai_so_muot = sum(lich_su) / len(lich_su)
        tho.append(sai_so)
        muot.append(sai_so_muot)
        if len(tho) >= 150:
            break
        print(f"{sai_so_muot:.2f}")
        s_tho  = statistics.pstdev(tho)
        s_muot = statistics.pstdev(muot)
        if sai_so_muot < -5 :
            huong = "SANG TRAI"
        elif sai_so_muot > 5:
            huong = "SANG PHAI"
        else:
            huong = "GIUA"
        cv2.putText(frame, f"{huong} (sai so: {sai_so_muot:.2f}) <s_tho: {s_tho:.2f}> <s_muot: {s_muot:.2f}>", (x, max(y - 10, 15)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
    else:
        lich_su.clear()
        cv2.putText(frame, f"KHONG THAY VAT", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
    cv2.imshow("webcam", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
cap.release()
cv2.destroyAllWindows()

if len(tho) > 2:
    print("so khung    :", len(tho))
    print("min / max   :", min(tho), "/", max(tho))
    print("mean        :", statistics.mean(tho))
    print("nhieu tho   :", nhieu(tho))
    print("nhieu muot  :", nhieu(muot))