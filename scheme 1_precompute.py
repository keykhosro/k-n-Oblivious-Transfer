# -*- coding: utf-8 -*-
"""
Created on Mon May 20 03:20:59 2024

@author: khosro
"""


from math import sqrt
from math import floor
import numpy as np
import random
#import time
import timeit
import random




def is_prime(q):
    if q <= 1:
        return False
    if q == 2:
        return True
    if q % 2 == 0:
        return False
    limit = floor(sqrt(q)) + 1
    for i in range(3, limit, 2):
        if q % i == 0:
            return False
    return True


for q in range(1985994,10000000000):
    if is_prime(q):
        if is_prime(2*q+1):
            P=2*q+1
            print(q)
            break


def message_generator(q,n):
    m=[]
    for i in range(n):
        m.append(np.random.randint(1, 2*q))

    return m




class Sender:
    def __init__(self, q, n,M):
        self.q = q
        self.n = n
        self.g = self.rand_generator(q)
        self.r, self.C, self.bulletin, self.alpha = self.sender_setup(self.g, n, q,M)

    def sender_step1(self, R1, k):
        self.S1 = self.sender_step1_helper(self.bulletin, self.q, R1, k, self.r)
        return self.r, self.C, self.S1

    def rand_generator(self, q):
        x = np.random.randint(1, 2 * q)
        P = 2 * q + 1
        while (pow(x, 2, P) == 1) or (pow(x, q, P) == (P - 1)):
            x = np.random.randint(1, 2 * q)

        return x

    def sender_setup(self, g, n, q,M):
        alpha = random.sample(range(1, q), n)
        r = np.random.randint(1, q)
        bulletin = []
        C=[]
        for i in range(n):
            bulletin.append(pow(g, alpha[i], 2 * q + 1))
        for i in range(n):
            C.append((M[i] * pow(bulletin[i], r, 2 * q + 1)) % (2 * q + 1))
        return r,C,bulletin, alpha

    def sender_step1_helper(self, bulletin, q, R1, k,r):
        S1 = []
        for i in range(k):
            S1.append(pow(R1[i], r, 2 * q + 1))
        return S1

class Receiver:
    def __init__(self, q, k, sigma, bulletin):
        self.q = q
        self.k = k
        self.sigma = sigma
        self.R1, self.secret = self.receiver_step1(k, sigma, bulletin, q)

    def receiver_step1(self, k, sigma, bulletin, q):
        secret = random.sample(range(1, q), k)
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
            temp = pow(secret[i], -1, q)
            next_temp = pow(S1[i], temp, 2 * q + 1)
            another_temp = pow(next_temp, -1, 2 * q + 1)
            R2.append((C[sigma[i]] * another_temp) % (2 * q + 1))
        return R2

timev=[]
# Define the parameters
print(q,P)
n=45
k=7
#sigma = [0, 2, 4]  # Indices of the shares for the receiver
for i in range(10000): 
    sigma=random.sample(range(n), k)    # Indices of the shares for the receiver
    
    # Generate the message
    M = message_generator(q, n)
    
    # Create the sender object
    sender = Sender(q, n,M)
    

    start_time = timeit.default_timer()
    # Create the receiver object
    receiver = Receiver(q, k, sigma, sender.bulletin)
    
    # Sender step 1
    r, C, S1 = sender.sender_step1(receiver.R1, k)
    
    # Receiver step 2
    R2 = receiver.receiver_step2(C, S1)
    elapsed_time=timeit.default_timer() - start_time
    print("--- %s seconds ---" %(elapsed_time))
    timev.append(elapsed_time)
    #print("Message shares (R2):", R2)
    action=True
    for i in range(k):
        if(R2[i]!=M[sigma[i]]):
            action=False
                
    if(action==False):
        print(r,sender.alpha,sender.bulletin,M,sigma,receiver.R1,S1,R2)
        print(action)
        break
    print(action)
print("--- average time %s seconds ---" %(np.average(timev)))
print("--- time taken for 10,000 OTs %s seconds ---" %(np.sum(timev)))