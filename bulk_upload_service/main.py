# coding: utf-8
import os
import sys
import redis

from bulk_upload_service.config import FILE_LINK

sys.path.append(os.getcwd())
from bulk_upload_service.celery_tasks import upload

redisClient = redis.Redis(decode_responses=True)


def get_key(filename):
    """随便弄个hash当key"""
    filehash = (
        hash(os.path.splitext(filename)[0])
        if hash(os.path.splitext(filename)[0]) > 0
        else hash(os.path.splitext(filename)[0]) + sys.maxsize
    )
    return "bulk_" + str(filehash) + os.path.splitext(filename)[1]


def do_bulk_upload(path):
    all_folders = os.listdir(path)
    res = []
    for folder in all_folders:
        if folder == ".DS_Store":  # MacOS下的隐藏文件
            continue

        filepath = path + os.sep + folder
        all_files = os.listdir(filepath)
        for filename in all_files:
            if filename == ".DS_Store":
                continue

            item = dict()

            item["name"] = folder + "-" + filename
            item["source_name"] = folder + "-" + filename
            item["file_url"] = FILE_LINK + get_key(filename)

            res.append(item)

            if redisClient.hexists("qiniu_bulk_upload", item["name"]):
                continue

            upload.delay(path + os.sep + folder + os.sep + filename, get_key(filename))

    return


if __name__ == "__main__":
    path = "/Users/shaoxyz/Downloads/demo"  # 需要批量上传的路径 默认此路径下有一个或一个以上文件夹

    do_bulk_upload(path)
