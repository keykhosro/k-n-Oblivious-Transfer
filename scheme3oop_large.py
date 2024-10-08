# -*- coding: utf-8 -*-
"""
Created on Sun May  5 01:06:08 2024

@author: khosro
"""

import gmpy2
from gmpy2 import mpz
import numpy as np
import random
import timeit



def is_prime(q):
    return gmpy2.is_prime(q)

# Adjusted the prime search for large q


def message_generator(q, n):
    m = []
    for i in range(n):
        m.append(random.randint(1, q))
    return m

def large_random_sample(q, n):
    result = set()
    while len(result) < n:
        result.add(random.randint(1, q))
    return list(result)



class Sender:
    def __init__(self):
        self.bulletin, self.d, self.x = self.sender_setup()

    def sender_setup(self):
        a = mpz(2) ** 1023 +mpz(2)**1022
        while True:
            if is_prime(a) and is_prime(2*a+1):
                p = 2*a + 1
                break
            a += 1

        b = mpz(2) ** 1023 
        while True:
            if is_prime(b) and is_prime(2*b+1):
                q = 2*b + 1
                break
            b += 1

        N = p * q
        x = rand_generator(p, q)
        e, d = key_generator(p, q)
        bulletin = [N, e, pow(x, e, N)]
        return bulletin, d, x

    def sender_step1(self, R1, M, n):
        N, e, xe = self.bulletin
        primeset = generate_primes(n)
        S1 = []
        C = []
        for i in range(len(R1)):
            S1.append(pow(R1[i], self.d, N))
        for i in range(n):
            C.append((M[i] * self.x * pow(primeset[i], self.d, N)) % (N))
        return C, S1

class Receiver:
    def __init__(self, n, k, sigma, bulletin):
        self.n = n
        self.k = k
        self.sigma = sigma
        self.bulletin = bulletin
        self.R1, self.secret = self.receiver_step1()

    def receiver_step1(self):
        N, e, xe = self.bulletin
        secret = generate_coprime_numbers(N, self.k)
        primeset = generate_primes(self.n)
        R1 = []
        for i in range(self.k):
            R1.append((primeset[self.sigma[i]] * pow(secret[i], e, N) * xe) % N)
        return R1, secret

    def receiver_step2(self, C, S1):
        N, e, xe = self.bulletin
        R2 = []
        for i in range(self.k):
            next_temp = (gmpy2.invert(S1[i], N) * self.secret[i]) % (N)
            R2.append((C[self.sigma[i]] * next_temp) % (N))
        return R2


def rand_generator(p, q):
    N = p * q
    x = random.randint(1, N)
    while (pow(x, 4, N) == 1) or (gmpy2.gcd(x, N) != 1):
        x = random.randint(1, N)
    return x

def key_generator(p, q):
    phi = (p - 1) * (q - 1)
    e = random.randint(1, phi)
    while (gmpy2.gcd(e, phi) != 1):
        e = random.randint(1, phi)
    d = pow(e, -1, phi)
    return [e, d]


def generate_coprime_numbers(N, k):
    coprimes = []
    while len(coprimes) < k:
        candidate = random.randint(1, N - 1)
        if gmpy2.gcd(candidate, N) == 1:
            coprimes.append(candidate)
    return coprimes

def generate_primes(N):
    primes = [3]  # Start with 3 as the first prime
    num = 5  # Start checking from 5
    while len(primes) < N:
        if is_prime(num):
            primes.append(num)
        num += 2  # Increment by 2 to skip even numbers
    return primes



timev=[]
# Example usage
n = 45
k = 7

sender = Sender()

for i in range(10000):
    sigma = random.sample(range(n), k)


    N, e, xe = sender.bulletin

    receiver = Receiver(n, k, sigma, sender.bulletin)

    M = message_generator(N, n)

    start_time = timeit.default_timer()

    C, S1 = sender.sender_step1(receiver.R1, M, n)
    R2 = receiver.receiver_step2(C, S1)
    elapsed_time=timeit.default_timer() - start_time
    print("--- %s seconds ---" %(elapsed_time))
    timev.append(elapsed_time)
    
    action = True
    for i in range(k):
        if R2[i] != M[receiver.sigma[i]]:
            action = False
            break
    if(action==False):
        print(sender.x, sender.bulletin, M, receiver.sigma, receiver.R1, S1, R2)
        print(action)
        break

    print(action)
print("--- average time %s seconds ---" %(np.average(timev)))
print("--- time taken for 10,000 OTs %s seconds ---" %(np.sum(timev)))