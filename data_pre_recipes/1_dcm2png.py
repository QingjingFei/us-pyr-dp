# dcm转png
import pydicom
import matplotlib.pyplot as plt
import scipy.misc
import imageio
import pandas as pd
import numpy as np
import os


def DcmToPng(file_path, png_path):  # sourcery skip: avoid-builtin-shadow
    # 获取所有图片名称
    cnt = 0
    dirs = sorted(os.listdir(file_path))
    for dir in dirs:
        # print(dirs)
        new_dir = os.path.join(file_path, dir)
        print('-------------------------------------------')
        print('Folder: ', new_dir)
        new_png_path = os.path.join(png_path, dir)
        for child in sorted(os.listdir(new_dir)):
            cwd_dir = os.path.join(new_dir, child)
            cwd_png_path = os.path.join(new_png_path, child)
            while os.path.isdir(cwd_dir):
                cwd_png_path = os.path.join(cwd_png_path, os.listdir(cwd_dir)[0])
                cwd_dir = os.path.join(cwd_dir, os.listdir(cwd_dir)[0])
            dir = os.path.dirname(cwd_dir)
            dir_png = os.path.dirname(cwd_png_path)
            if not os.path.exists(dir_png):
                os.makedirs(dir_png)
            else:
                continue
            for file in sorted(os.listdir(dir)):
                fullpath = os.path.join(dir, file)
                file_name, ext = os.path.splitext(file)
                # legal format of ext should be: '' or '.dcm' or 'dicom'
                if ext.lower() not in ('', '.dcm', '.dicom'):
                    print('Error!!!!!!!!!!', fullpath)
                    continue
                out_path = os.path.join(dir_png, file_name) + ".png"
                cnt += 1
                print('File: ', fullpath)
                ds = pydicom.read_file(fullpath)
                img = ds.pixel_array  # 提取图像信息，(y, x, z)
                imageio.imsave(out_path, img)

    print(f'Totally {cnt} DICOM files have changed.')

if __name__ == '__main__':
    src_path = r'./DOING/20230830_dcm__'
    des_path = r'./DOING/20230830_png__'

    DcmToPng(src_path, des_path)