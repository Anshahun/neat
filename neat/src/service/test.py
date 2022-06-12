from celery import group
from celery.result import GroupResult


l = {}


def on_raw_message(body):
    print(body)


def test(li):
    for i in li:
        yield {'i':i+1}


if __name__ == '__main__':
    a, b = 1, 1
    # t:AsyncResult = tasks.hello.delay(2,2)
    li = [1,2,3]
    j=2
    #g:GroupResult = group(tasks.hello.s(i['i'], j) for i in list(test(li)))()

    # g.get(on_message=on_raw_message, propagate=False)
    # tinfo:list = l[r.id]
    # print(tinfo[-1][''])
    # g.save()
    # for i in GroupResult.restore(g.id).results:
    #   i:AsyncResult
    #  AsyncResult.failed()
    # print(i.date_done)
    # res = AsyncResult('0118e596-7cc8-448a-9c4a-0e582fc57543').result
    # server = moudles.Server('192.168.28.131',22,'breath','naxiehuaer')
    # s:AsyncResult = command.delay(server, 'echo hello world')
    # time.sleep(5)
    # print(AsyncResult(s.id).traceback)
    #print(next(test(li)))
    # list(test(li))
    #print(res)
    #g.get(on_message=on_raw_message, propagate=False)
    #post = list(__generate_task_result(GroupResult.restore('6817a88b-dabb-448e-9474-496fad9df979', app=celeryApp.app)))
    #print(post)