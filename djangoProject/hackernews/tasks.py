from .models import Comment, StopLoop
from djangoProject.celery import app

import requests

@app.task(bind=True)
def get_comment(self, current, id):
    if Comment.objects.filter(id=id).exists():
        StopLoop.objects.filter(id=1).update(stopped=True, running=False)

        return

    res = requests.get(f'https://hacker-news.firebaseio.com/v0/item/{id}.json')

    diff = current - res.json()['time']

    if (((diff / 60) / 60) / 24) > 7:
        StopLoop.objects.filter(id=1).update(stopped=True, running=False)

        return

    if res.json()['type'] != 'comment':
        return

    if 'by' in res.json():
        author = res.json()['by']

        comment = Comment()
        comment.author = author
        comment.id = id
        comment.time = res.json()['time']

        comment.save()
