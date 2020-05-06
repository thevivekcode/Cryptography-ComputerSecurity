
# coding: utf-8

# # RSA Encryption and Decryption

# In[1]:


import math
import numpy as np


# In[2]:


def chatToint(c):
    if c >='0' and c<='9':
        return (ord(c) - 21)
    else:
        return ord(c) - ord('a')

def intTochar(i):
    if i >= 27:
        return chr(i+21)
    else:
        return chr(i+97)


# In[3]:


def calVal(l,x):
    newl = l[::-1]
    val = 0
    for i in range(len(newl)):
        val += newl[i]*pow(x,i)
    return val

def calList(Cval,x,blockSize):
    val = Cval
    l = []
    for i in range(blockSize,-1,-1):
        q = val//(pow(x,i))
        val = val%(pow(x,i))
        l.append(q)
    return l[::-1]
        


# In[4]:


def RSA_encryption(M,e,N):
    '''
    M = message
    e = encryption Key
    N = p*q
    '''
    blockSize = int(math.log(N,37))
    messagelist = list(map(chatToint,list(M)))
    messageBlocks = [messagelist[i*blockSize:(i+1)*blockSize] for i in range((len(messagelist)+blockSize-1)//blockSize)]
    cipherText =""
    if len(messageBlocks[-1])!= blockSize:
        for i in range(blockSize-len(messageBlocks[-1])):
            messageBlocks[-1].append(chatToint('{'))
    
    for i in messageBlocks:
        val = calVal(i,37)
        Cval = pow(val,e,N)
        i_new = calList(Cval,37,blockSize)

        cipherText = cipherText + str("".join(list(map(intTochar,i_new))))
    return cipherText
        


# In[5]:


def RSA_decryption(M,d,N):
    '''
    M = message
    d = decryption Key
    N = p*q
    '''
    blockSize = int(math.log(N,37))+1
    messagelist = list(map(chatToint,list(M)))
    messageBlocks = [messagelist[i*blockSize:(i+1)*blockSize] for i in range((len(messagelist)+blockSize-1)//blockSize)]
    plainText =""
    for i in messageBlocks:
        val = calVal(i[::-1],37)
        Cval = pow(val,d,N)
        i_new = calList(Cval,37,blockSize-2)
        plainText = plainText + str("".join(list(map(intTochar,i_new))[::-1]))
    return plainText


# In[6]:


ct=RSA_encryption("aaa",3,28471)
ct


# In[7]:


pt =RSA_decryption('aaab4m',18667,28471)
pt

