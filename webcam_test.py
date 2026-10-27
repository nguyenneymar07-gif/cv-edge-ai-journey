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
    #findContours trả về 2 giá trị: contours là danh sách các đường bao, _ là các thông tin khác (không cần dùng đến)
    #RETR_EXTERNAL chỉ lấy đường bao ngoài cùng
    #CHAIN_APPROX_SIMPLE nén bớt điểm cho nhẹ. Kết quả contours là một danh sách (có thể rỗng).
    biggest = max(contours, key=cv2.contourArea) if contours else None
    if biggest is not None and cv2.contourArea(biggest) > 500:
        rect = cv2.boundingRect(biggest)
        #Tính hình chữ nhật bao quanh contour. rect là bộ 4 số: rect[0] = x (góc trên-trái), rect[1] = y, rect[2] = chiều rộng, rect[3] = chiều cao.
        x, y, w, h = rect
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        #Vẽ khung lên ảnh gốc: góc trên-trái là (x, y), góc dưới-phải là (x + w, y + h), màu xanh lá (BGR), nét dày 2 pixel.
        toa_do = (x + w // 2, y + h // 2)
        cv2.putText(frame, f"({toa_do[0]}, {toa_do[1]})", (x, max(y - 10, 15)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        #Viết chữ lên ảnh. Các tham số lần lượt: ảnh cần viết, nội dung (f-string chèn tọa độ tâm), vị trí (phía trên khung 10 pixel), kiểu chữ, cỡ chữ 0.5, màu xanh lá, độ dày nét 1.
    cv2.imshow("webcam", frame)
    cv2.imshow("mask", mask)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
cap.release()
cv2.destroyAllWindows()    