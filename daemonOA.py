import threading
from time import sleep

from PyOa import DocHandler, OaParse, OaTaskQue

OA = OaTaskQue()
print('  ● The task que length:  ★', len(OA.task_queue))
t_task_watch = threading.Thread(target=OA.daemon_task)
t_task_watch.setDaemon(True)
t_task_watch.start()
handler = DocHandler()
while True:
    if OA.task_queue:
        x = OA.task_queue.popleft()
        wid = x.get('workItemId')
        todoUrl = x.get('todoUrl')
        pageHtml = handler.get_doc_detail(url=todoUrl, workId=wid)
        x['html'] = pageHtml
        page = OaParse(pageHtml)
        page.parse_page()
        print('  ● Dealing doc: {}'.format(page.title))
        handler.send_cmt(page, "已阅")
        handler.send_end(page)
        print('  ● The task que length:  ★', len(OA.task_queue))
        sleep(10)
    else:
        continue
