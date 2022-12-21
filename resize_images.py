import os
from typing import Set
from PIL import Image

def resize_img(path: str):
    with Image.open(path) as img:
        # print(f'{img.mode}')
        mode = img.mode

        if img.mode == 'CMYK':
            img = img.convert('RGB')

        if img.size != (671, 471):
            img = img.resize((671, 471))

        # print(f'Converted ({mode}) {inpath=} to: {outpath=}')
        img.save(path, bitmap_format="bmp")


def resize_imgs_in_dir(root: str, exclude: Set[str] = None):
    exclude = exclude or set()

    for dirpath, dirnames, filenames in os.walk(root):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            resize_img(filepath)

        for dirname in dirnames:
            if dirname in exclude:
                continue

            dirpath = os.path.join(dirpath, dirname)
            resize_imgs_in_dir(dirpath)


if __name__ == "__main__":
    root = os.path.dirname(__file__)
    datasets = os.path.join(root, "datasets", "midv-2020")
    for doctype in os.listdir(datasets):
        docpath = os.path.join(datasets, doctype)
        resize_imgs_in_dir(docpath)
