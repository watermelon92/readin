import os, zipfile, hashlib, sys, shutil, codecs
from django.conf import settings

UPLOAD_FILES_DIR = os.path.join(settings.BASE_DIR, 'uploadedfiles')


def handle_uploaded_file(f, num, new_dir_name):
    release_file_dir = os.path.join(UPLOAD_FILES_DIR, str(num))
    new_dir = os.path.join(release_file_dir,new_dir_name)


    filePath = f
    with zipfile.ZipFile(filePath, 'r') as zf:
        for fn in zf.namelist():
            right_fn = fn.encode('cp437').decode('utf-8')  # 将文件名正确编码
            right_fn = os.path.join(release_file_dir, right_fn)

            if right_fn[-1] == '/':
                os.makedirs(right_fn, mode=0o777)
                continue

            with codecs.open(right_fn, 'w+', encoding='utf-8') as output_file:  # 创建并打开新文件
                with zf.open(fn, 'r') as origin_file:  # 打开原文件
                    shutil.copyfileobj(origin_file, output_file)  # 将原文件内容复制到新文件

        renameFile(release_file_dir,new_dir)

        return os.path.join(release_file_dir,new_dir_name)


# 1、接收上传文件
# 2、创建路径upload/docid/datetime
# 3、解压文件到该文件夹下
# 4、把地址存到数据库
# 5、做一个路由函数处理


def handle_filedir(str):
    hl = hashlib.md5()
    hl.update(str.encode(encoding='utf-8'))

    return hl.hexdigest()

def renameFile(old_dir, new_dir):
    lists = os.listdir(old_dir)
    for item in lists:
        path = os.path.join(old_dir,item)
        if os.path.isdir(path):
            os.rename(path, new_dir)
