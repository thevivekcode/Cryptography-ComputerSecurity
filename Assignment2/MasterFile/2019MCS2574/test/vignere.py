
# coding: utf-8

# In[1]:


import numpy as np


# In[2]:


def chatToint(c):
    return ord(c) - ord('a')

def intTochar(i):
    return chr(i+97)


# In[3]:


def VigenereEncryption(key,plainText):
    key = list(map(chatToint,list(key)))
    plainText = list(map(chatToint,list(plainText.lower())))
    keySize  =len(key)
    textSize = len(plainText)
    q = textSize//keySize
    r = textSize%keySize
    finalKey = key*q + key[:r]
    return "".join(list(map(intTochar,np.mod(np.array(finalKey) + np.array(plainText),26))))

def VigenereDecryption(key,cipherText):
    key = list(map(chatToint,list(key)))
    cipherText = list(map(chatToint,list(cipherText.lower())))
    keySize  =len(key)
    textSize = len(cipherText)
    q = textSize//keySize
    r = textSize%keySize
    finalKey = key*q + key[:r]
    return "".join(list(map(intTochar,np.mod(np.array(cipherText) - np.array(finalKey) ,26))))

