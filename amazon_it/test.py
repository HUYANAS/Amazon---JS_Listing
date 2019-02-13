
import threading
import queue

def requ(q):
    print(t.name)

q = queue.Queue()

for i in range(1, 11):
    t = threading.Thread(target=requ, args=(q,))
    t.start()
    t.join()


# # 等待线程
# for i in range(1, 11):
#     t.join()
print('Jiesu')