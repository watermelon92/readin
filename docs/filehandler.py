# coding=utf-8
import os, zipfile, sys
from django.conf import settings

UPLOAD_FILES_DIR = os.path.join(settings.BASE_DIR, 'uploadedfiles')


def handle_uploaded_file(f, num, des_dir_name):
    release_file_dir = os.path.join(UPLOAD_FILES_DIR, str(num))
    des_dir = os.path.join(release_file_dir, des_dir_name)
    file_root = ''
    with zipfile.ZipFile(f, 'r') as zf:
        for fn in zf.namelist():
            right_fn = fn.encode('cp437').decode('utf-8')  # 将文件名正确编码
            abs_right_fn = os.path.join(release_file_dir, right_fn)

            if right_fn[-1] == '/':
                os.makedirs(abs_right_fn, mode=0o777) #创建文件夹
                if right_fn.count('/') == 1:
                    file_root = right_fn
                continue

            with open(abs_right_fn, 'wb') as output_file:  # 创建并打开新文件
                output_file.write(zf.read(fn))

        origin_dir = os.path.join(release_file_dir, file_root)
        os.rename(origin_dir, des_dir)
        file_url = os.path.join(str(num), des_dir_name, 'index.html')

        file_tuple = (des_dir, file_url)

        return file_tuple
