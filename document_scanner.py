import cv2 
import numpy as np

im = cv2.imread("image_and_video/anh_giay_trang.jpg")
if im is None :
    raise FileNotFoundError("khong tim thay anh")
    
height, width = im.shape[:2]
scale = 600 / height
new_height = 600
new_width = int(width * scale) # pixel chỉ nhận giá trị nguyên
im = cv2.resize(im,(new_width, new_height))   #opencv chi nhan thu tu theo rong dai

imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
imgray = cv2.GaussianBlur(imgray, (5, 5), 0)
im_edge = cv2.Canny(imgray, 75, 200)
contours, hierarchy = cv2.findContours(im_edge, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
biggest = max(contours, key = cv2.contourArea) if contours else None 

if biggest is not None and cv2.contourArea(biggest) > 500:
    peri = cv2.arcLength(biggest, True)  #tính chu vi đường bao
    epsilon = 0.02 * peri
    approx = cv2.approxPolyDP(biggest, epsilon, True)


if approx is not None and len(approx) == 4:
    print("Da tim thay 4 goc")
else:
    print("khong phai 4 goc ma la ", len(approx), " goc")
    
for point in approx:
    x, y = point[0]
    cv2.circle(im, (x, y), 5, (0, 0, 255), -1)
cv2.drawContours(im, [approx], -1, (0, 255, 0), 2)
cv2.imshow("contours", im)
cv2.waitKey(0)
cv2.destroyAllWindows()





