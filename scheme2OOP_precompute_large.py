# Import the required modules
from sage.rings.finite_rings.finite_field_constructor import FiniteField
from sage.schemes.elliptic_curves.constructor import EllipticCurve

import gmpy2
from gmpy2 import mpz
import numpy as np
import random
#import time
import timeit
import random






def is_prime(q):
    return gmpy2.is_prime(q)



print("phase 1 finding suitable eliptic curve")

n=45
k=7
#elliptic curve parameters
a = 3  # Coefficient of x^2 in the elliptic curve equation
b = 17  # Coefficient of x in the elliptic curve equation

for p in range(mpz(2) **223 ,mpz(2) **224): # Prime number for the finite field
    if is_prime(p):
        #print(p)
        # Create the finite field
        F = FiniteField(p)
        # Create the elliptic curve over the finite field
        E = EllipticCurve(F, [a, b])
        num=E.order()
        print(num)
        if is_prime(num):
            # Print the elliptic curve equation
            print("Elliptic curve equation: {}".format(E))
            # Find the generator point and its order
            G = E.gens()[0]  # Generator point
            print("field is in:", p)
            print("Order of the curve:", num)
            order = G.order()  # Order of the generator
            # Print the generator and its order
            print("\nGenerator point: {}".format(G))
            print("Order of the generator: {}".format(order))
            break
        
        
        



def message_generator(num,n,G):
    m=[]
    for i in range(n):
        m.append(random.randint(1, num)*G)

    return m


def large_random_sample(num, n):
    result = set()
    while len(result) < n:
        result.add(random.randint(1, num))
    return list(result)



class Sender:
    def __init__(self,G, num, n,M):
        self.num = num
        self.n = n
        self.g = G
        self.r, self.C,self.bulletin, self.alpha = self.sender_setup(self.g, self.n,self.num,M)

    def sender_step1(self, R1, k):
        self.S1 = self.sender_step1_helper(self.bulletin, self.num, R1, k, self.n,self.r)
        return self.r, self.C, self.S1

    def sender_setup(self, G, n, num,M):
        alpha = large_random_sample(num, n)
        bulletin = []
        r = random.randint(1, num)
        C=[]
        for i in range(n):
            bulletin.append(alpha[i]* G)
        for i in range(n):
            C.append( M[i] +(r* bulletin[i]))
        return r,C,bulletin, alpha

    def sender_step1_helper(self, bulletin, num, R1, k, n,r):
        S1 = []
        for i in range(k):
            S1.append(r* R1[i])
        return S1

class Receiver:
    def __init__(self, num, k, sigma, bulletin):
        self.num = num
        self.k = k
        self.sigma = sigma
        self.R1, self.secret = self.receiver_step1(k, sigma, bulletin, num)

    def receiver_step1(self, k, sigma, bulletin, num):
        secret = large_random_sample( num, k)
        R1 = []
        for i in range(k):
            R1.append(secret[i]* bulletin[sigma[i]])
        return R1, secret

    def receiver_step2(self, C, S1):
        self.R2 = self.receiver_step2_helper(self.k, self.sigma, self.num, S1, self.secret, C)
        return self.R2

    def receiver_step2_helper(self, k, sigma, num, S1, secret, C):
        R2 = []
        for i in range(k):
            temp = power_mod(secret[i], num-2, num)
            next_temp = temp * S1[i] 
            R2.append(C[sigma[i]] - next_temp)
        return R2
    
    
    
    
    
    
    print("phase 2 performing Oblivious transfer")


for i in range(10000): 
    sigma=random.sample(range(n), k)    # Indices of the shares for the receiver
    
    # Generate the message
    M = message_generator(num, n,G)
    
    # Create the sender object
    sender = Sender(G,num,n,M)
    

    start_time = timeit.default_timer()
    # Create the receiver object
    receiver = Receiver(num, k, sigma, sender.bulletin)
    
    # Sender step 1
    r, C, S1 = sender.sender_step1(receiver.R1,k)
    
    # Receiver step 2
    R2 = receiver.receiver_step2(C, S1)
    print("--- %s seconds ---" %(timeit.default_timer() - start_time))
    #print("Message shares (R2):", R2)
    action=True
    for i in range(k):
        if(R2[i]!=M[sigma[i]]):
            action=False
            print(r,sender.bulletin,M,sigma,receiver.R1,S1,R2)
            print(action)
            break
    if(action==False):
        break
    print(action)