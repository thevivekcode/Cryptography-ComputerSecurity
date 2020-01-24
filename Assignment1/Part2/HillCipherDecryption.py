
# coding: utf-8

# In[1]:


import math
import sys
import numpy as np


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


def cipherTextinput():
    with open("./InputFiles/cipherText.txt","r") as chipherTextFile:
        cipherText = chipherTextFile.read().replace("\n","").replace(" ","")
        return list(map(charToInt,list(cipherText)))
#         return list(plainText)


# In[5]:


##takes input key and cpherText in" int np.array" format
def decryption(K,C):
    PT=[np.dot(K,CT) for CT in C]
    return list(map(intTochar,list(np.reshape(PT,(1,-1)).flat)))


# In[6]:


# Ax+My = 1 = gcd(A,M) = gcd(M,A%M)
x=1
y=0
cf=0  #highest commmon factor
def gcd(A,M):
    global x
    global y
    global cf
    if M==0:
        x=1
        y=0
        cf=A
    else:
        gcd(M,A%M)
        temp=x
        x=y
        y=temp-(A//M)*y
#         print(x,y,cf)


# In[7]:


def invKey(key,keySize):
    det = np.round(np.linalg.det(key))

    gcd(det,26)
    global cf
    global x
    if(cf!=1):
        print("WRONG KEY !!")
        print("Key is not Coprime to 26")
        exit()

    invKey = np.linalg.inv(key)

    adj = np.round(invKey*det)*(x%26) #cf is the modular inverse of det w.r.t 26

    keymodInv = np.mod(adj.astype(int),26)
    return keymodInv


# In[8]:


def decrypt():
    (key,keySize) = keyInput()
    cipherTextList = cipherTextinput()

    keymodInv = invKey(key,keySize)

    cipherTextMatrix = np.reshape(cipherTextList,(-1,keySize))

#     print(keymodInv)

    plainTextList=decryption(keymodInv,cipherTextMatrix)

    # print(plainTextList)


    s = "".join(plainTextList)
#     print(s)
    return s


# In[9]:


op = decrypt()
op

