import os, zipfile, hashlib, sys
from django.conf import settings

UPLOAD_FILES_DIR = os.path.join(settings.BASE_DIR, 'uploadedfiles')


def handle_uploaded_file(f, num):
    release_file_dir = os.path.join(UPLOAD_FILES_DIR, str(num))
    # new_dir = os.path.join(release_file_dir,new_dir_name)
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

        # renameFile(release_file_dir, new_dir)
        file_location = os.path.join(release_file_dir, file_root)
        file_url = os.path.join(str(num), file_root, 'index.html')

        file_tuple = (file_location, file_url)

        return file_tuple


# 1、接收上传文件
# 2、创建路径upload/docid/datetime
# 3、解压文件到该文件夹下
# 4、把地址存到数据库
# 5、做一个路由函数处理


# def handle_filedir(str):
#     hl = hashlib.md5()
#     hl.update(str.encode(encoding='utf-8'))
#
#     return hl.hexdigest()

# def renameFile(old_dir, new_dir):
#     lists = os.listdir(old_dir)
#     for item in lists:
#         path = os.path.join(old_dir,item)
#         if os.path.isdir(path):
#             os.rename(path, new_dir)
