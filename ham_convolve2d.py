import cv2
import numpy as  np

image = cv2.imread('image_and_video/anh_giay_xeo.jpg',cv2.IMREAD_GRAYSCALE)
if image is None:
    raise SystemExit("Khong doc duoc anh")
img = image.astype(np.float32)
kernel = np.ones((3, 3)) / 9
print(kernel)

def convolution(img, kernel): #tính tương quan, không lật kerne
    h, w = img.shape
    kh, kw = kernel.shape

    pad_h = kh // 2
    pad_w = kw // 2

    padded = np.pad(
        img,
        ((pad_h, pad_h), (pad_w, pad_w)),
        mode='reflect'
    )

    output = np.zeros((h, w), dtype=np.float32)
    
    for i in range(h):
        for j in range(w):
            vung = padded[i:i + kh, j:j + kw]
            output[i, j] = np.sum(vung * kernel)
    return output
    

result = convolution(img, kernel)

print("Min:", np.min(result))
print("Max:", np.max(result))
print("Mean:", np.mean(result))

result_show = np.clip(result, 0, 255).astype(np.uint8)

cv2.imshow("Original", image)
cv2.imshow("Blur", result_show)

cv2.waitKey(0)
cv2.destroyAllWindows()