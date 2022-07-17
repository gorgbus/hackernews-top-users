from django.shortcuts import render
from django.http import HttpResponseForbidden, HttpResponseRedirect
from .tasks import get_comment
from .models import Comment, StopLoop
from djangoProject.celery import app

import requests
import time
import datetime

# Create your views here.
def get_data(request):
    res = requests.get('https://hacker-news.firebaseio.com/v0/maxitem.json')
    current = int(time.time())

    id = res.json()

    run = StopLoop.objects.get(id=1)

    if run.running and not run.stopped:
        return HttpResponseForbidden('Already running')

    StopLoop.objects.filter(id=1).update(stopped=False, running=True)
    
    for id in range(id, 0, -1):
        stop = StopLoop.objects.get(id=1)

        if stop.stopped:
            break

        get_comment.delay(current, id)

    app.control.purge()

    commments = Comment.objects.all().reverse()

    for comment in commments:
        diff = current - comment.time

        if (((diff / 60) / 60) / 24) > 7:
            comment.delete()
        else:
            break

    return HttpResponseRedirect('/')

def get_users(request):
    dates = request.GET
    invalid = False

    current = str(datetime.datetime.now())
    current = f"{current[:10]} 23:59:59"
    current = datetime.datetime.strptime(current, '%Y-%m-%d %H:%M:%S')
    current = int(time.mktime(current.timetuple()))

    comments = Comment.objects.all()

    period = 'week'
    
    if 'od' and 'do' in dates:
        od = dates['od']
        do = dates['do']
        do = f"{do} 23:59:59"

        if len(od) != 0 and len(do) != 0:
            od = datetime.datetime.strptime(od, '%Y-%m-%d')
            od = int(time.mktime(od.timetuple()))

            do = datetime.datetime.strptime(do, '%Y-%m-%d %H:%M:%S')
            do = int(time.mktime(do.timetuple()))

            week = 1000 * 60 * 60 * 24 * 7

            if od > do or od < (current - week) or do > current:
                invalid = True
            else:
                period = f"{dates['od'][8:10]}.{dates['od'][5:7]}. - {dates['do'][8:10]}.{dates['do'][5:7]}."
                comments = Comment.objects.filter(time__range=(od, do))
        else:
            invalid = True

    users = {}

    for comment in comments:
        if comment.author not in users:
            users[comment.author] = 1
        else:
            users[comment.author] += 1

    sorted_users = sorted(users.items(), key=lambda x: x[1], reverse=True)

    return render(request, 'users.html', { 'users': sorted_users, 'invalid': invalid, 'period': period })