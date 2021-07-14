import sys
import os
import requests
import threading
import queue
import time

q = queue.Queue()


def scan():
    while not q.empty():
        urls = q.get()
        try:
            code = requests.get(urls).status_code
            if code == 200 or code == 403:
                print(urls + '|' + str(code))
                f = open('ok.txt', 'a+')
                f.write(urls + '\n')
                f.close()
            else:
                print(urls + '|' + str(code))
                time.sleep(1)
        except requests.ConnectionError:
            print('ConnectionError!Plase wait 1 seconds!')
            time.sleep(1)
        except:
            print('UnknownError!Plase wait 1 seconds!')
            time.sleep(1)

def show():
    print('Usage: dirscan  URL文件 file文件名 线程数')
    print('Example: dirscan url.txt dict.txt 10')


if __name__ == '__main__':
    path = os.path.dirname(os.path.realpath(__file__))
    print(path)
    if len(sys.argv) < 4:
        show()
        sys.exit()
    url = sys.argv[1]
    file = sys.argv[2]
    threads = sys.argv[3]
    for url in open(path + '/' + url):
        for dir in open(path + '/' + file):
            urls=url+dir
            urls=urls.replace('\n','')
            q.put(urls)

    for i in range(int(threads)):
        t = threading.Thread(target=scan())
        t.start()
