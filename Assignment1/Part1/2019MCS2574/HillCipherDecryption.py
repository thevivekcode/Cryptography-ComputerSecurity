
# coding: utf-8

# In[4]:


import math
import sys
import numpy as np


# In[5]:


#for char to int where a=0...z=25
def charToInt(s):
    value=ord(s)-ord('a')
    return value

#for int to char where 0=a...25=z
def intTochar(s):
    return chr(s%26 +ord('a'))


# In[6]:


def keyInput(fileInput):
    with open(fileInput,"r") as keyFile:
        keyString = keyFile.read().replace("\n"," ").split()
        keyList = list(map(int,keyString))
        keyLen = int(math.sqrt(len(keyList)))
        key =  np.reshape((np.array(keyList[:(keyLen**2)])),(keyLen,keyLen))
        return key,keyLen


# In[7]:


def cipherTextinput(fileInput):
    with open(fileInput,"r") as chipherTextFile:
        cipherText = chipherTextFile.read().replace("\n","").replace(" ","")
        return list(map(charToInt,list(cipherText)))
#         return list(plainText)


# In[8]:


##takes input key and cpherText in" int np.array" format
def decryption(K,C):
    PT=[np.dot(K,CT) for CT in C]
    return list(map(intTochar,list(np.reshape(PT,(1,-1)).flat)))


# In[9]:


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


# In[22]:


(key,keySize) = keyInput(sys.argv[1])
cipherTextList = cipherTextinput(sys.argv[2])

det = np.round(np.linalg.det(key))

gcd(det,26)

if(cf!=1):
    print("WRONG KEY !!")
    print("Key is not Coprime to 26")
    exit()

invKey = np.linalg.inv(key)

adj = np.round(invKey*det)*(x%26) #cf is the modular inverse of det w.r.t 26

adj = np.mod(adj.astype(int),26)

cipherTextMatrix = np.reshape(cipherTextList,(-1,keySize))

plainTextList=decryption(adj,cipherTextMatrix)

# print(plainTextList)
for i in range(len(plainTextList)-1, len(plainTextList)-keySize-1, -1):
    if(plainTextList[i] == 'x'):
        del plainTextList[i]


s = "".join(plainTextList)
print(s)

outputFile = open("DecryptionOutput.txt","w+")
outputFile.write(s)
outputFile.close()
