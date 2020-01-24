
# coding: utf-8

# In[1]:


import math
import numpy as np
import sys


# In[2]:


#for char to int where a=0...z=25
def charToInt(s):
    value=ord(s)-ord('a')
    return value

#for int to char where 0=a...25=z
def intTochar(s):
    return chr(s%26 +ord('a'))


# In[3]:


def keyInput():
    with open("./InputFiles/key.txt","r") as keyFile:
        keyString = keyFile.read().replace("\n"," ").split()
        keyList = list(map(int,keyString))
        keyLen = int(math.sqrt(len(keyList)))
        key =  np.reshape((np.array(keyList[:(keyLen**2)])),(keyLen,keyLen))
        return key,keyLen
        
        


# In[4]:


def plainTextInput():
    with open("./InputFiles/plainText.txt","r") as plainTextFile:
        plainText = plainTextFile.read().replace("\n","").replace(" ","")
        return list(map(charToInt,list(plainText)))
#         return list(plainText)


# In[5]:


#takes input key and plaintext in "int np.array" format
def encryption(K,P):
    CT=[np.dot(K,PT) for PT in P]
    s=""
    return s.join(list(map(intTochar,list(np.reshape(CT,(1,-1)).flat))))


# In[9]:


def encrypt():
    (key,keyLen) = keyInput()
    # print(key, keyLen)
    plainTextList = plainTextInput()
    paddLen = keyLen-len(plainTextList)%keyLen
    # print(paddLen)
    for i in range(paddLen):
        plainTextList.append(23)
    # print(plainTextList)
    plainText = np.reshape(np.array(plainTextList),(-1,keyLen))
    # print(plainText)

    # cipherFile = open("cipherOutput","w+")
    cipherText = encryption(key,plainText)
#     print(cipherText)
    # cipherFile.write(cipherText)
    return cipherText


 


# In[10]:


op = encrypt()
op

