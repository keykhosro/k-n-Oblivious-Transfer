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



def large_random_sample(q, n):
    result = set()
    while len(result) < n:
        result.add(random.randint(1, q))
    return list(result)


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






def random_2048_bit_prime():
    # Generate a random 2048-bit starting point
    a = mpz(random.getrandbits(2048))
    a |= (1 << 2047)  # ensure it is 2048-bit
    a |= 1             # ensure odd
    # Search for the next probable prime
    while not is_prime(a):
        a += 2
    return a

# Generate random 2048-bit primes
p = random_2048_bit_prime()
q = random_2048_bit_prime()
while q == p:   # ensure distinct
    q = random_2048_bit_prime()



#a = mpz(2) ** 1023 +mpz(2)**1022
#while True:
#    if is_prime(a):
#        p = a
#        break
#    a += 1
#
#b = mpz(2) ** 1023 
#while True:
#    if is_prime(b):
#        q = b
#        break
#    b += 1

N = p * q

e, d = key_generator(p, q)

timev=[]

start_time = timeit.default_timer()

A = generate_coprime_numbers(N, 1)
#print("Debug: candidate A =", A)
val = pow(A[0], e, N)
while not is_prime(val):
    A = generate_coprime_numbers(N, 1)
    #print("Debug: candidate A =", A)
    val = pow(A[0], e, N)

elapsed_time = timeit.default_timer() - start_time
print("--- %s seconds ---" % (elapsed_time))
print("Final A:", A)


