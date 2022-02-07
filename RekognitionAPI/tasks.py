from __future__ import absolute_import, unicode_literals
from celery import shared_task
import time
import main.tasksPy.task as task

@shared_task
def add(x1, x2):
	time.sleep(10)
	y = x1 + x2
	print('処理完了')
	return y

@shared_task
def rekognition():
    print("処理開始")
    task.main()
    print("処理終了")
    return