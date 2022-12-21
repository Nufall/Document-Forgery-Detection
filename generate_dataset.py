import os
from turtle import shape
import cv2

from utils import display
from typing import Iterable, Optional, Union, Literal

Category = Union[Literal["genuine"], Literal["forged"]]
Subset = Union[Literal["training"], Literal["validation"]]

class DatasetGenerator:    
    def __init__(self, PROJECT_ROOT: str, TEMPLATE_PATH: str) -> None:
        self.PROJECT_ROOT = PROJECT_ROOT
        self.TEMPLATE_PATH = TEMPLATE_PATH
        self.DATASET_SIZE: Optional[int] = 32
        # min(
        #     len(os.listdir(os.path.join(self.PROJECT_ROOT, "original_genuine"))),
        #     len(os.listdir(os.path.join(self.PROJECT_ROOT, "original_forged"))),
        # ) 
        # self.DATASET_SIZE = None
        self.TEMPLATE: cv2.Mat = cv2.imread(TEMPLATE_PATH)
        print(f'{self.DATASET_SIZE=}')


    def original_images(self, category: Category) -> Iterable[str]:
        directory = os.path.join(self.PROJECT_ROOT, f"original_{category}")
        for i, name in enumerate(os.listdir(directory)):
            if self.DATASET_SIZE is not None and i > self.DATASET_SIZE:
                print(f"Found {i} images in {directory}")
                return
            yield name, os.path.join(directory, name)


    def subtract_images(self, category: Category, subset: Subset):
        for imgname, imgpath in self.original_images(category):
            img = cv2.imread(imgpath)
            try:
                delta = cv2.subtract(img, self.TEMPLATE)
                newpath = os.path.join(self.PROJECT_ROOT, subset, category, imgname)
                cv2.imwrite(newpath, delta)
            except Exception as e:
                print(f'{imgpath}; {self.TEMPLATE_PATH}')
                # print(e)
                print(img.shape)
                print(self.TEMPLATE.shape)
                # print(f'{img.shape=}; {self.TEMPLATE.shape=}')

if __name__ == "__main__":
    root = os.path.dirname(__file__)
    root = os.path.join(root, 'datasets', 'midv-2020-scanned','experiment 2')

    for doctype in os.listdir(root):
        if doctype == '.DS_Store': continue

        docpath = os.path.join(root, doctype)
        templatepath = os.path.join(docpath, 'aligned_template.bmp')

        print(f'{docpath=}')
        print(f'{templatepath=}')

        validation = os.path.join(docpath, 'validation')
        validation_forged = os.path.join(docpath, 'validation', 'forged')
        validation_genuine = os.path.join(docpath, 'validation', 'genuine')

        if not os.path.isdir(validation): os.mkdir(validation)
        if not os.path.isdir(validation_forged): os.mkdir(validation_forged)
        if not os.path.isdir(validation_genuine): os.mkdir(validation_genuine)

        gen = DatasetGenerator(docpath, templatepath)
        gen.subtract_images("genuine", "validation")
        gen.subtract_images("forged",  "validation")
