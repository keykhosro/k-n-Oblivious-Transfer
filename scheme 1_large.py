# -*- coding: utf-8 -*-
"""
Created on Wed May  1 06:54:08 2024

@author: khosro
"""

import gmpy2
from gmpy2 import mpz
import random
import numpy as np
import timeit

def is_prime(q):
    return gmpy2.is_prime(q)

# Adjusted the prime search for large q
q = mpz(2) ** 2048 +342378456
while True:
    if is_prime(q) and is_prime(2*q+1):
        P = 2*q + 1
        print(q)
        break
    q += 1

def message_generator(q, n):
    m = []
    for i in range(n):
        m.append(random.randint(1, 2*q))
    return m

def large_random_sample(q, n):
    result = set()
    while len(result) < n:
        result.add(random.randint(1, q))
    return list(result)


class Sender:
    def __init__(self, q, n):
        self.q = q
        self.n = n
        self.g = self.rand_generator(q)
        self.bulletin, self.alpha = self.sender_setup(self.g, n, q)

    def sender_step1(self, M, R1, k):
        self.r, self.C, self.S1 = self.sender_step1_helper(self.bulletin, self.q, M, R1, k, self.n)
        return self.r, self.C, self.S1

    def rand_generator(self, q):
        x = random.randint(1, 2 * q)
        P = 2 * q + 1

        while (pow(x, 2, P) == 1) or (pow(x, q, P) == (P - 1)):
            x = random.randint(1, 2 * q)

        return x

    def sender_setup(self, g, n, q):
        alpha = large_random_sample( q, n)
        bulletin = []
        for i in range(n):
            bulletin.append(pow(g, alpha[i], 2 * q + 1))
        return bulletin, alpha

    def sender_step1_helper(self, bulletin, q, M, R1, k, n):
        r = random.randint(1, q)
        S1 = []
        C = []
        for i in range(k):
            S1.append(pow(R1[i], r, 2 * q + 1))
        for i in range(n):
            C.append((M[i] * pow(bulletin[i], r, 2 * q + 1)) % (2 * q + 1))
        return r, C, S1

class Receiver:
    def __init__(self, q, k, sigma, bulletin):
        self.q = q
        self.k = k
        self.sigma = sigma
        self.R1, self.secret = self.receiver_step1(k, sigma, bulletin, q)

    def receiver_step1(self, k, sigma, bulletin, q):
        secret = large_random_sample( q, k)
        R1 = []
        for i in range(k):
            R1.append(pow(bulletin[sigma[i]], secret[i], 2 * q + 1))
        return R1, secret

    def receiver_step2(self, C, S1):
        self.R2 = self.receiver_step2_helper(self.k, self.sigma, self.q, S1, self.secret, C)
        return self.R2

    def receiver_step2_helper(self, k, sigma, q, S1, secret, C):
        R2 = []
        for i in range(k):
            temp = gmpy2.invert(secret[i], q)
            next_temp = pow(S1[i], temp, 2 * q + 1)
            another_temp = gmpy2.invert(next_temp, 2 * q + 1)
            R2.append((C[sigma[i]] * another_temp) % (2 * q + 1))
        return R2

timev = []
# Define the parameters
print(q, P)
n = 45
k = 7

for i in range(10000):
    sigma = random.sample(range(n), k)
    sender = Sender(q, n)
    M = message_generator(q, n)

    start_time = timeit.default_timer()
    receiver = Receiver(q, k, sigma, sender.bulletin)
    r, C, S1 = sender.sender_step1(M, receiver.R1, k)
    R2 = receiver.receiver_step2(C, S1)
    elapsed_time = timeit.default_timer() - start_time
    print("--- %s seconds ---" % elapsed_time)
    timev.append(elapsed_time)

    action = True
    for i in range(k):
        if R2[i] != M[sigma[i]]:
            action = False

    if not action:
        print(r, sender.alpha, sender.bulletin, M, sigma, receiver.R1, S1, R2)
        print(action)
        break
    print(action)

print("--- average time %s seconds ---" % np.average(timev))
print("--- time taken for 10,000 OTs %s seconds ---" % np.sum(timev))
