import requests
import time

res = requests.get('https://hacker-news.firebaseio.com/v0/maxitem.json')
current = int(time.time())

id = res.json()

comments = []

for id in range(id, 0, -1):
    req_url = f'https://hacker-news.firebaseio.com/v0/item/{id}.json'

    res = requests.get(req_url)

    diff = current - res.json()['time']

    if (diff / 60 / 60) > 6:
        break

    if res.json()['type'] != 'comment':
        continue

    comments.append(res.json())

users = {}

for comment in comments:
    if 'by' in comment:
        if comment['by'] not in users:
            users[comment.author] = 1
        else:
            users[comment.author] += 1

sorted_users = sorted(users.items(), key=lambda x: x[1], reverse=True)

print(sorted_users)

