import cv2

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise RuntimeError("Không mở được camera")

lower = (100, 120, 70)
upper = (130, 255, 255)

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
        print(f"{sai_so:.2f}")
    
        if sai_so < -5 :
            huong = "SANG TRAI"
        elif sai_so > 5:
            huong = "SANG PHAI"
        else:
            huong = "GIUA"
        cv2.putText(frame, f"{huong}_(sai so: {sai_so:.2f})", (x, max(y - 10, 15)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
    else:
        cv2.putText(frame, f"KHONG THAY VAT", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
    cv2.imshow("webcam", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
cap.release()
cv2.destroyAllWindows()