import time


def wait(tag, seconds):
    if (seconds < 1):
        time.sleep(seconds)
        return
    for i in range(int(seconds)):
        time.sleep(1)
        print(f"{tag} wait {i+1} seconds")

