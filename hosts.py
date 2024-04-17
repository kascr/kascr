import socket
import threading
from tqdm import tqdm

num_threads = 150  # 自定义线程数
hosts_file = "hosts.txt"  # 广告域名文件路径
out_file = "hosts.1"  # 结果输出文件路径

# 读取广告域名列表
with open(hosts_file) as f:
    hosts = [line.strip() for line in f]

# 创建一个锁，以确保多线程写入文件时不会发生冲突
lock = threading.Lock()

# 每个线程要执行的任务
def check_hosts_thread(start_idx, pbar):
    for i in range(start_idx, len(hosts), num_threads):
        host = hosts[i]
        ip_list = []
        try:
           addrs = socket.getaddrinfo(
           host, None)
           for item in addrs:
              if item[4][0] not in ip_list:
                 ip_list.append(item[4][0])
        except Exception as e:
           pass
        else:
           with lock:
              with open(out_file, "a") as f:
                 f.write("127.0.0.1 " + host + "\n")
        pbar.update()

# 创建并启动线程
threads = []
pbar = tqdm(total=len(hosts))
for i in range(num_threads):
    t = threading.Thread(target=check_hosts_thread, args=(i, pbar))
    threads.append(t)
    t.start()

# 等待所有线程完成
for t in threads:
    t.join()

pbar.close()
print("跑完啦!")

