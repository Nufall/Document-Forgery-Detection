import os
import cv2
from PIL import Image

root = r'D:\Downloads\dataset\scan_rotated\images\alb_id'
for x in os.listdir(root):
    y = os.path.join(root, x)
    with Image.open(y) as img:
        if img.mode == 'CMYK':
            img = img.convert('RGB')
        n = y.replace('.jpg', '.bmp')
        img.save(n, bitmap_format="bmp")
        os.remove(y)
