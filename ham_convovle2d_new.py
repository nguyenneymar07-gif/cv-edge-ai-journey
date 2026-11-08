import cv2
import numpy as np
import time


def convolution(img, kernel):
    h, w = img.shape
    kh, kw = kernel.shape
    pad_h = kh // 2
    pad_w = kw // 2
    padded = np.pad(
        img,
        ((pad_h, pad_h), (pad_w, pad_w)),
        mode='reflect'
    )
    output = np.zeros((h, w),dtype=np.float32)
    for i in range(h):
        for j in range(w):
            vung = padded[i:i + kh, j:j + kw]
            output[i, j] = np.sum(vung * kernel)
    return output
    
anh = cv2.imread('image_and_video/anh_giay_xeo.jpg',cv2.IMREAD_GRAYSCALE)
if anh is None:
    raise SystemExit("Khong doc duoc anh")
h, w = anh.shape
anh = cv2.resize(anh, (int(w * 600 / h), 600)).astype(np.float32)

kernels = {
    "lam_mo_9x9": np.ones((9, 9), np.float32) / 81,
    "sobel_doc": np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], np.float32),
}

for ten, k in kernels.items():
    t0 = time.time()
    cua_ban = convolution(anh, k)
    t_ban = time.time() - t0

    t0 = time.time()
    cua_cv = cv2.filter2D(anh, -1, k, borderType=cv2.BORDER_REFLECT_101)
    t_cv = time.time() - t0

    chenh = np.abs(cua_ban - cua_cv)[5:-5, 5:-5].max()
    print(f"{ten}: chenh = {chenh:.6f} | ban: {t_ban:.2f}s | cv2: {t_cv:.4f}s")

    hien = np.clip(np.abs(cua_ban), 0, 255).astype(np.uint8)
    cv2.imshow(ten, hien)

cv2.waitKey(0)
cv2.destroyAllWindows()