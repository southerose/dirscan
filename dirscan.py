import sys
import os
import requests
import threading
import queue
import time

q = queue.Queue()


def main():
    # 获取脚本所在目录
    path = os.path.dirname(os.path.realpath(__file__))

    # 参数个数小于4时，显示脚本提示信息并退出
    if len(sys.argv) < 4:
        show()
        sys.exit()

    # 分别获取第1、2、3个参数值
    domains = sys.argv[1]
    file = sys.argv[2]
    threads = sys.argv[3]

    # 打开脚本目录所在的url文件
    for domain in open(path + '/' + domains):
        # 拼接url与字典
        for dir in open(path + '/' + file):
            urls = domain + dir
            urls = urls.replace('\n', '')
            # 将拼接后的URL放入队列中
            q.put(urls)

    # 多线程扫描的实现
    for i in range(int(threads)):
        t = threading.Thread(target=scan())
        t.start()


# 定义扫描函数
def scan():
    # 判断队列是否为空，为空则继续执行进入循环
    while not q.empty():
        # 取出队列中的url
        urls = q.get()

        # 请求的站点返回值为200 or 403，则写入ok.txt文件中
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
    print('Usage: dirscan  domains文件 file文件名 线程数')
    print('Example: dirscan domains.txt dict.txt 10')


if __name__ == '__main__':
    main()
