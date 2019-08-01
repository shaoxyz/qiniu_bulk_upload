from __future__ import absolute_import

from celery.utils.log import get_task_logger
from qiniu import Auth, put_file

from bulk_upload_service.celery_app import app
from bulk_upload_service.config import QINIU_ACCESS_KEY, QINIU_SECRET_KEY, QINIU_BUCKET_NAME

logger = get_task_logger(__name__)

q = Auth(QINIU_ACCESS_KEY, QINIU_SECRET_KEY)


@app.task
def upload(localfilePath, key):
    token = q.upload_token(QINIU_BUCKET_NAME, key, 60 * 60 * 24)  # 1天

    localfile = localfilePath
    ret, info = put_file(token, key, localfile)
    logger.info(f"文件已传至 七牛云 {ret}")
    return ret
