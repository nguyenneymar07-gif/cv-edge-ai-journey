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
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)    
    blurred_frame = cv2.GaussianBlur(gray_frame, (5, 5), 0)
    edge_frame = cv2.Canny(blurred_frame, 50, 250)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower, upper)
    result = cv2.bitwise_and(frame, frame, mask=mask)
    
    cv2.imshow("webcam", frame)
    cv2.imshow("webcam_gray", gray_frame)
    cv2.imshow("webcam_edge", edge_frame)
    cv2.imshow("mask", mask)
    cv2.imshow("result", result)
    
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
cap.release()
cv2.destroyAllWindows()
