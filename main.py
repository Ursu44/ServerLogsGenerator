import time

from server_logs import generate

while True:
    time.sleep(1)
    print(generate())