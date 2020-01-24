
# coding: utf-8

# In[92]:


import math
import numpy as np
import sys


# In[93]:


#for char to int where a=0...z=25
def charToInt(s):
    value=ord(s)-ord('a')
    return value

#for int to char where 0=a...25=z
def intTochar(s):
    return chr(s%26 +ord('a'))


# In[94]:


def keyInput(Kfiles):
    with open(Kfiles,"r") as keyFile:
        keyString = keyFile.read().replace("\n"," ").split()
        keyList = list(map(int,keyString))
        keyLen = int(math.sqrt(len(keyList)))
        key =  np.reshape((np.array(keyList[:(keyLen**2)])),(keyLen,keyLen))
        return key,keyLen




# In[95]:


def plainTextInput(PTfiles):
    with open(PTfiles,"r") as plainTextFile:
        plainText = plainTextFile.read().replace("\n","").replace(" ","")
        return list(map(charToInt,list(plainText)))
#         return list(plainText)


# In[96]:


#takes input key and plaintext in "int np.array" format
def encryption(K,P):
    CT=[np.dot(K,PT) for PT in P]
    s=""
    return s.join(list(map(intTochar,list(np.reshape(CT,(1,-1)).flat))))


# In[98]:


(key,keyLen) = keyInput(sys.argv[1])
# print(key, keyLen)
plainTextList = plainTextInput(sys.argv[2])
paddLen = keyLen-len(plainTextList)%keyLen
# print(paddLen)
for i in range(paddLen):
    plainTextList.append(23)
# print(plainTextList)
plainText = np.reshape(np.array(plainTextList),(-1,keyLen))
print(plainText)

cipherFile = open("EncryptionOutput.txt","w+")
cipherText = encryption(key,plainText)
cipherFile.write(cipherText)
cipherFile.close()
