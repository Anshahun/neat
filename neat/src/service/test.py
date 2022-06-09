import time

from celery import group, Task
from celery.backends.base import BaseBackend
from celery.canvas import Signature
from celery.result import AsyncResult, GroupResult
import celery

from neat.src.app import moudles
from neat.src.service import tasks
import json

from neat.src.service.tasks import command

l = {}
def on_raw_message(body):
    print(body)

if __name__ == '__main__':
    a, b = 1, 1
    #t:AsyncResult = tasks.hello.delay(2,2)
    #g:GroupResult = group(tasks.hello.s(2, 2), tasks.hello.s(4, 4),tasks.hello.s(6,6))()

    #g.get(on_message=on_raw_message, propagate=False)
    #tinfo:list = l[r.id]
    #print(tinfo[-1][''])
    #g.save()
    #for i in GroupResult.restore(g.id).results:
     #   i:AsyncResult
      #  AsyncResult.failed()
       # print(i.date_done)
    #res = AsyncResult('0118e596-7cc8-448a-9c4a-0e582fc57543').result
    server = moudles.Server('192.168.28.131',22,'breath','naxiehuaer')
    s:AsyncResult = command.delay(server, 'echo hello world')
    time.sleep(5)
    print(AsyncResult(s.id).traceback)