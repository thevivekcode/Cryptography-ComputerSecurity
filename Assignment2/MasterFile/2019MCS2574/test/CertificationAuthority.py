


import gmpy2
import random
import RSA



def generate_prime(state,bit_count):
    rand_state = gmpy2.random_state(state)
    temp = gmpy2.mpz_rrandomb(rand_state, bit_count)
    return gmpy2.next_prime(temp)


# In[4]:


def generate_strongPrime(bit_count):
    primeSet = set()
    while(len(primeSet)<10):
        state = random.randrange(10,80)
        p1 = generate_prime(state,bit_count)
        p2 = gmpy2.next_prime(p1)
        p3 = gmpy2.next_prime(p2)
        if (p1 + p3)/2 < p2: #p2 is strong prime
            primeSet.add(p2)
    return list(primeSet)



# In[5]:


def generateKey(p,q):
    n = p*q
    phiN = (p-1)*(q-1)
    state = random.randrange(10,80)
    e = generate_prime(state,10) # taking e to be small 10 bit number
    while gmpy2.gcd(e,phiN)!=1:
        e+=2
    d = gmpy2.invert(e,phiN)
    return e,d,n




# In[6]:


def generateCAKey(primeList):
    p = primeList[0]
    q = primeList[1]
    (e_CA,d_CA,n_CA) = generateKey(p,q)
    return e_CA,d_CA,n_CA



# In[7]:


def generate_Sender_1_Key(primeList):
    p = primeList[2]
    q = primeList[3]
    (e_S1,d_S1,n_S1) = generateKey(p,q)
    return e_S1,d_S1,n_S1


# In[8]:


def generate_Sender_2_Key(primeList):
    p = primeList[4]
    q = primeList[5]
    (e_S2,d_S2,n_S2) = generateKey(p,q)
    return e_S2,d_S2,n_S2


# In[12]:


if __name__ == "__main__":
    primeList = generate_strongPrime(512)
    (e_CA,d_CA,n_CA) = generateCAKey(primeList)
    (e_S1,d_S1,n_S1) = generate_Sender_1_Key(primeList)
    (e_S2,d_S2,n_S2) = generate_Sender_2_Key(primeList)


    with open('CA_public_key','w') as f:
        str1 = "CA_public_Key : "+ str(e_CA)+" "+str(n_CA)+"\n"
        f.write(str1)
    # encrypting the public keys of the senders

    e_S1E =  RSA.RSA_encryption(str(e_S1),d_CA,n_CA)
    n_S1E =  RSA.RSA_encryption(str(n_S1),d_CA,n_CA)
    e_S2E =  RSA.RSA_encryption(str(e_S2),d_CA,n_CA)
    n_S2E =  RSA.RSA_encryption(str(n_S2),d_CA,n_CA)

    with open('public_directory','w') as f:
        str2 = "S1_public_Key : "+str(e_S1E)+" "+str(n_S1E)+"\n"
        str3 = "S2_public_Key : "+str(e_S2E)+" "+str(n_S2E)+"\n"
        f.write(str2)
        f.write(str3)

    # encrypting the private keys of the senders
    with open('receiver_private_key','w') as f:
        str4 = "S1_private_Key : "+str(d_S1)+" "+str(n_S1)+"\n"
        f.write(str4)

    with open('sender_private_key','w') as f:
        str5 = "S2_private_Key : "+str(d_S2)+" "+str(n_S2)+"\n"
        f.write(str5)
