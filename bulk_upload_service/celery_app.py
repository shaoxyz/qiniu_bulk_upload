from __future__ import absolute_import

from celery import Celery

app = Celery('bulk_upload_service', include=['bulk_upload_service.celery_tasks'])

app.config_from_object('bulk_upload_service.celery_config')


if __name__ == '__main__':
    app.start()