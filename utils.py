import time
import random

def action_runner(delay):
    print("Running action")
    time.sleep(delay)
    print("Action completed")

for i in range(10):
    action_runner(random.randint(1, 10))