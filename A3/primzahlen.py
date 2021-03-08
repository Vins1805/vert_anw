from typing import List, Union
import threading
import concurrent.futures
import numpy as np
import time


class Barriere():
    def __init__(self, n):
        self.lock = threading.Lock()
        self.n = n

    def p(self):
        """ Acquire. """
        self.lock.acquire()
        print("lock acquired")
        return self.n

    def v(self):
        """ Release. """
        self.lock.release()
        print("lock releases")


def read_txt(filepath) -> list:
    with open(filepath, "r") as reader:
        return [int(line.replace("\n", "")) for line in reader.readlines() if not line.startswith("#")]


def factorial(end, start=1):
    result = 1
    for i in range(start, end+1):
        result = result * i
    return result


def is_prime_number(end: int, start: int=1, barrier: Barriere=None, return_bool=False, _factorial=True) -> Union[bool, int]:
    if return_bool:
        if end == 0:
            return False
        elif barrier:
            n = barrier.n
        else:
            n = end
        if not _factorial:
            return end % n == n-1
        return factorial(end-1, start) % n == n-1
    n = barrier.p()
    result = factorial(end, start) % n
    barrier.v()
    return result


def split_up(n: int, t: int) -> List[tuple]:

    assert t > 0, "Threads should be bigger then 0."
    
    splitted_prime = list()
    for i in range(0, t):
        splitted_prime += [(int(i*(n-1)/t+1), int((i+1)*(n-1)/t) if i+1 != t else n-1)]
    return splitted_prime

def build_threads(n):

    sharedVar = Barriere(n)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(lambda p: is_prime_number(*p), [(*i[::-1], sharedVar) for i in split_up(n, threads)]))
        print(f"Is {n} a prime number: {is_prime_number(np.prod(results), barrier=sharedVar, return_bool=True, _factorial=False)}")


if __name__ == "__main__":
    system_start_time = time.time()
    process_start_time = time.process_time()
    
    
    threads = 32
    
    real_prime_numbers = read_txt("echte_primzahlen.txt")
    fake_prime_numbers = read_txt("fake_primzahlen.txt")

    total_time = 0

    if False:
        n = 1000000
        
        build_threads(n)
        print(f"current total time: {total_time} (CPU)")
    
    if True:
        for pn in real_prime_numbers:
            if pn < threads*2:
                print(f"skipped number {pn} due to conflicts with threads.")
                continue
            #print(f"{pn} is prime number: {is_prime_number(pn)}")
            build_threads(pn)
            print(f"current total time: {total_time} (CPU)")

    if True:
        for pn in fake_prime_numbers:
            if pn < threads*2:
                print(f"skipped number {pn} due to conflicts with threads.")
                continue
            #print(f"{pn} is prime number: {is_prime_number(pn)}")
            build_threads(pn)
            print(f"current total time: {total_time} (CPU)")
    

    system_end_time = time.time()
    process_end_time = time.process_time()
    print(f"system time: {system_end_time - system_start_time}")
    print(f"process time: {process_end_time - process_start_time}")

    
    
    
    




