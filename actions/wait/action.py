import time

def wait(details):
    print("INFO: Waiting for 10 seconds")
    time.sleep(details["duration"])
    print("INFO: Done waiting")