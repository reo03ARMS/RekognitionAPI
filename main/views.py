from celery.result import AsyncResult
from django.shortcuts import render

from RekognitionAPI.tasks import add,rekognition

def celery_test(request):
	task_id = add.delay(5, 5)

	result = AsyncResult(task_id)
	print('result:', result, ' : ', result.state, ' : ', result.ready())

	context = {'result': result}

	return render(request, 'main/celery_test.html', context)

def rekognition_test(request):
    task_id = rekognition.delay()
    result = AsyncResult(task_id)
    print('result:', result, ' : ', result.state, ' : ', result.ready())
    context = {'result': result}
    return render(request, 'main/rekognition_test.html', context)
    