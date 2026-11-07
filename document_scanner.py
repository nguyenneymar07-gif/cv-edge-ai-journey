import cv2 
import numpy as np

im = cv2.imread("image_and_video/anh_giay_an.jpg")
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

approx = None
if biggest is not None and cv2.contourArea(biggest) > 500:
    peri = cv2.arcLength(biggest, True)  #tính chu vi đường bao
    epsilon = 0.02 * peri
    approx = cv2.approxPolyDP(biggest, epsilon, True)

if approx is not None and len(approx) == 4:
    print("Da tim thay 4 goc")
else:
    n = 0 if approx is None else len(approx)
    print("so goc cua ung vien tot nhat:", n)
    debug = im.copy()
    cv2.drawContours(debug, contours, -1, (0, 255, 0), 2)   # contours = danh sach 5 cai lon nhat
    cv2.imshow("canny", im_edge)
    cv2.imshow("5 contour lon nhat", debug)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    raise SystemExit("Khong tim duoc 4 goc")
    
for point in approx:
    x, y = point[0]
    cv2.circle(im, (x, y), 5, (0, 0, 255), -1)
cv2.drawContours(im, [approx], -1, (0, 255, 0), 2)
cv2.imshow("contours", im)
cv2.waitKey(0)
cv2.destroyAllWindows()

def sapxep(pts):
    s = pts.sum(axis=1)
    d = np.diff(pts, axis=1)
    top_left = pts[np.argmin(s)]
    bottom_right = pts[np.argmax(s)]
    top_right = pts[np.argmin(d)]
    bottom_left = pts[np.argmax(d)]
    return np.array([top_left, top_right, bottom_right, bottom_left], dtype=np.float32)

pst = approx.reshape(4,2).astype("float32")
pst = sapxep(pst)

rong1 = np.linalg.norm(pst[1] - pst[0])
rong2 = np.linalg.norm(pst[2] - pst[3])
rong = max(int(rong1), int(rong2))

cao1 = np.linalg.norm(pst[0] - pst[3])
cao2 = np.linalg.norm(pst[1] - pst[2])
cao = max(int(cao1), int(cao2))
# linalg.norm: tính khoảng cách giữa 2 điểm trong không gian 2D

dich = np.array([[0, 0], [rong - 1, 0], [rong - 1, cao - 1], [0, cao - 1]], dtype="float32")
M = cv2.getPerspectiveTransform(np.array([pst[0], pst[1], pst[2], pst[3]], dtype="float32"), dich)
phang = cv2.warpPerspective(im, M, (int(rong), int(cao)))
#warpPerspective nhận kích thước theo thứ tự (rộng, cao), ngược với shape của mảng

cv2.imshow("goc", im)
cv2.imshow("phang", phang)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.imshow("canny", im_edge)
print("so goc:", None if approx is None else len(approx))