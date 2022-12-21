import os
import cv2
import scipy.stats as st

from utils import display

def input_image_paths(root: str):
    for file in os.listdir(root):
        yield os.path.join(root, file)
        
def generate_template_from(root: list[str]):
    imgs = [cv2.imread(imgpath) for imgpath in root]
    template = st.tmax(imgs)
    assert template.shape == imgs[0].shape

    # display(template)
    # display(cv2.subtract(imgs[0], template))
    
    return template

if __name__ == "__main__":
    root = os.path.dirname(__file__)
    root = os.path.join(root, 'datasets', 'midv-2020')

    for doctype in os.listdir(root):
        docpath = os.path.join(root, doctype)
        templatepath = os.path.join(docpath, 'base_template.bmp')
        imgs = input_image_paths(os.path.join(docpath, 'original_genuine'))
        template = generate_template_from(imgs)
        cv2.imwrite(templatepath, template)