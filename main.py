import requests
import json
import random
from queue import Queue
from threading import Thread

# Read the current ids from a file, and don't fetch them!
filename = 'queers.json'
queers = {}
with open(filename, 'r') as file:
    queers = json.loads(file.read())

exist = [int(x) for x in queers.keys()]

q = Queue()
for id in range(13000, 14000):
    if id not in exist: q.put(id)

# This will be used to collect the ids which throw errors, for manual intervention later.
error_ids = []


# This is the worker process! This is where the magic happens.
# It grabs a number from the queue, and requests it. It then appends it to
# queers. This is a problem, because they are out of order, but it is not a
# problem for today!
def worker_proc():
    while not q.empty():
        try:
            target = q.get()
            url = f'https://www.queeringthemap.com/moment/{target}'
            text = requests.get(url).text
            queers[target] = json.loads(text)['description']
        except:
            print(f'error at {target}, passing')
            error_ids.append(target)


# for x in range(1,100):
#     try:
#         url = f'https://www.queeringthemap.com/moment/{x}'
#         text = requests.get(url).text
#         queers[x] = json.loads(text)['description']
#         try:
#             print(f'{x}: {queers[x]}' )
#         except:
#             print(f'print error at {x}')
#     except:
#         print(f'error at {x}, passing...')


processes = []

for _ in range(10):
    process = Thread(target=worker_proc)
    processes.append(process)

for process in processes:
    process.start()

for process in processes:
    process.join()


file = open(filename, 'w')
file.write(json.dumps(queers))
file.close()

print(f'ERRORS AT:')
print(error_ids)