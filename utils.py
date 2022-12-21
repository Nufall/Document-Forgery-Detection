import cv2

def display(img, title: str = ''):
    cv2.imshow(title, img)
    if cv2.waitKey(0) & 0xff == ord('q'):
        exit(0)
