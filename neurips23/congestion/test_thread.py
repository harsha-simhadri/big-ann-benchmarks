from neurips23.congestion.base import AbstractThread
import os
import time
import random
from queue import Queue
from threading import Lock

class ExampleThread(AbstractThread):
    def inline_main(self):
        print(f"Thread PID: {os.getpid()}")
        print(f"Running ExampleThread iteration {i}")
        time.sleep(10*random.random())

class ProducerThread(AbstractThread):
    def __init__(self, queue: Queue, lock: Lock):
        super().__init__()
        self.queue = queue
        self.lock = lock

    def inline_main(self):
        for i in range(10):
            time.sleep(random.uniform(0.1, 1))  # Random sleep to simulate real-world delays
            with self.lock:
                self.queue.put(i)
                print(f"Producer: Produced item {i} current size {self.queue.qsize()}")

class ConsumerThread(AbstractThread):
    def __init__(self, queue: Queue, lock: Lock):
        super().__init__()
        self.queue = queue
        self.lock = lock

    def inline_main(self):
        while True:
            time.sleep(random.uniform(0.2, 1.5))  # Random delay to simulate real-world processing
            with self.lock:
                if not self.queue.empty():
                    item = self.queue.get()
                    print(f"Consumer: Consumed item {item} current size {self.queue.qsize()}")
                    if item == 9:
                        break

# Example usage
if __name__ == "__main__":
    queue = Queue()
    lock = Lock()

    producer = ProducerThread(queue, lock)
    consumer = ConsumerThread(queue, lock)

    producer.start_thread()
    consumer.start_thread()

    producer.join_thread()
    consumer.join_thread()

