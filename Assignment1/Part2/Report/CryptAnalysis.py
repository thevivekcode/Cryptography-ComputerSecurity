
# coding: utf-8

# In[1]:


# COl759
import numpy as np
import time
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


def IdCoincidence(charOrdList):
    freq ={}
    N = len(charOrdList)
    for i in charOrdList:
        if i in freq:
            freq[i]+=1
        else:
            freq[i]=1
    num = 0
    for i in freq:
        num += freq[i]*(freq[i]-1)
    ic = num/(N*(N-1))
    return ic


# In[4]:


def ngram():
    unigram = ["e", "t", "a", "o", "i", "n", "s", "h", "r", "d"]
    bigram = ["th", "he", "in", "er", "an", "re", "nd", "at", "on", "nt"]
    trigram = ["the", "and", "ing", "ent", "ion", "tio", "for", "nde","has","nce"]
    return bigram, trigram, unigram


# In[5]:


def frequency(cipherTextPairs):
    freqDict ={}
    for i in cipherTextPairs:
        if i in freqDict:
            freqDict[i]+=1
        else:
            freqDict[i]=1
    return freqDict


# In[6]:


def inputKeySize():
    # print("Enter the keySize \n")
    # print("cipher text is taken automatically from ./InputFiles/cipherText.txt")
    keySize = int(sys.argv[2])
    cipher = open(sys.argv[1],'r')
    cipherTextList = list(cipher.read().replace("\n","").replace(" ",""))
    remainder = len(cipherTextList)%keySize
    if remainder !=0:
        return keySize, cipherTextList[:-remainder]
    else:
        return keySize, cipherTextList


def ngramGenerator(keySize,cipherTextList):
    cipherTextPairs = np.reshape(np.array(cipherTextList),(-1,keySize))
    ngram = []
    for i in cipherTextPairs:
        ngram.append("".join(i))
    return ngram



# In[7]:


def topTenFreq():
    (keySize, cipherTextList) = inputKeySize()
#     print(cipherTextList)
    ngram = ngramGenerator(keySize, cipherTextList)
    freqDict = frequency(ngram)
    sortedfreq = sorted(freqDict , key = freqDict.get)[::-1]
    return sortedfreq[:15] , keySize


# In[8]:


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


# In[9]:


##takes input key and cpherText in" int np.array" format
def decryption(K,C):
    PT=[np.dot(K,CT) for CT in C]
    return list(map(intTochar,list(np.reshape(PT,(1,-1)).flat)))


# In[10]:


def invKey(key,keySize):
#     print("func invKey :")
#     print(key)
    det = np.round(np.linalg.det(key))

    gcd(det,26)
    global cf
    global x
    if(cf!=1):
        return np.zeros((keySize,keySize))

    invKey = np.linalg.inv(key)

    adj = np.round(invKey*det)*(x%26) #cf is the modular inverse of det w.r.t 26

    keymodInv = np.mod(adj.astype(int),26)
    return keymodInv


# In[11]:


def cipherTextinput():
    with open(sys.argv[1],"r") as chipherTextFile:
        cipherText = chipherTextFile.read().replace("\n","").replace(" ","")
        return list(map(charToInt,list(cipherText)))


# In[12]:


def decrypt(keymodInv,keySize):
    cipherTextList = cipherTextinput()
    remainder = len(cipherTextList)%keySize
    if remainder !=0:
        cipherTextMatrix = np.reshape(cipherTextList[:-remainder],(-1,keySize))
    else:
        cipherTextMatrix = np.reshape(cipherTextList,(-1,keySize))
    plainTextList=decryption(keymodInv,cipherTextMatrix)
    s = "".join(plainTextList)
    return s


# In[13]:


def forOne(topTenCipherList,Eng_topTen,keySize):
    opFile = open("analysis","w+")
    count=0
    for i in range(len(Eng_topTen)):
        for j in range(len(topTenCipherList)):
            eng = np.reshape(np.array(list(map(charToInt,list(Eng_topTen[i])))),(keySize,-1))
            ciph = np.reshape(np.array(list(map(charToInt,list(topTenCipherList[j])))),(keySize,-1))

            Cmatrix = eng
            Pmatrix = ciph

            Pmatrix_inv = invKey(Pmatrix, keySize)
            if not np.array_equal(Pmatrix_inv , np.zeros((keySize,keySize)) ):

                key =np.mod( np.dot(Cmatrix,Pmatrix_inv),26)
                keyInv = invKey(key,keySize)
                key =list(key.flat)
                PT = decrypt(keyInv.astype(int),keySize)
                ic = IdCoincidence(list(PT))
                if (ic > 0.06) and (ic < 0.07):
                    print(key)
                    print("\n")
                    print(PT)
                    opFile.write(str(key))
                    opFile.write("\n")
                    opFile.write(PT)
                    opFile.write("\n")


    opFile.close()




# In[14]:


def forTwo(topTenCipherList,Eng_topTen,keySize):
    opFile = open("analysis","w+")
    count=0
    for i in range(len(Eng_topTen)):
        for j in range(i+1,len(Eng_topTen)):
            for k in range(len(topTenCipherList)):
                for l in range(k+1,len(topTenCipherList)):
                    count+=1
                    eng1 = np.reshape(np.array(list(map(charToInt,list(Eng_topTen[i])))),(keySize,-1))
                    eng2 = np.reshape(np.array(list(map(charToInt,list(Eng_topTen[j])))),(keySize,-1))
                    ciph1 = np.reshape(np.array(list(map(charToInt,list(topTenCipherList[k])))),(keySize,-1))
                    ciph2 = np.reshape(np.array(list(map(charToInt,list(topTenCipherList[l])))),(keySize,-1))

                    Cmatrix1 = np.append(ciph1,ciph2,axis = 1)
                    Cmatrix2 = np.append(ciph2,ciph1,axis = 1)
                    Pmatrix1 = np.append(eng1,eng2,axis = 1)
#                     Pmatrix2 = np.append(eng2,eng1,axis = 1)


                    Pmatrix1_inv = invKey(Pmatrix1, keySize)
                    if not np.array_equal(Pmatrix1_inv , np.zeros((keySize,keySize)) ):
                        key1 =np.mod( np.dot(Cmatrix1,Pmatrix1_inv),26)
                        key1Inv = invKey(key1,keySize)
                        key1 =list(key1.flat)
                        if np.array_equal(key1Inv, np.zeros((keySize,keySize)) ):
                            continue
                        PT = decrypt(key1Inv.astype(int),keySize)
                        ic = IdCoincidence(list(PT))
                        if (ic > 0.06) and (ic < 0.07):
                            print(key1)
                            print("\n")
                            print(PT)
                            opFile.write(str(key1))
                            opFile.write("\n")
                            opFile.write(PT)
                            opFile.write("\n")

                        key2 = np.mod(np.dot(Cmatrix2,Pmatrix1_inv), 26)
                        key2Inv = invKey(key2,keySize)
                        key2 =list(key2.flat)
                        if np.array_equal(key2Inv, np.zeros((keySize,keySize)) ):
                            continue
                        PT = decrypt(key2Inv.astype(int),keySize)
                        ic = IdCoincidence(list(PT))
                        if (ic > 0.06) and (ic < 0.07):
                            print(key2)
                            print("\n")
                            print(PT)
                            opFile.write(str(key2))
                            opFile.write("\n")
                            opFile.write(PT)
                            opFile.write("\n")


    opFile.close()



# In[15]:


def forThree(topTenCipherList,Eng_topTen,keySize):
    opFile = open("analysis","w+")
    count=0
    for h in range(len(Eng_topTen)):
        for i in range(h+1,len(Eng_topTen)):
            for j in range(i+1,len(Eng_topTen)):
                for jk in range(len(topTenCipherList)):
                    for k in range(jk+1,len(topTenCipherList)):
                        for l in range(k+1,len(topTenCipherList)):
                            eng =[]
                            ciph=[]
                            Cmatrix=[]
                            Pmatrix =[]
                            eng.append(np.reshape(np.array(list(map(charToInt,list(Eng_topTen[h])))),(keySize,-1)))
                            eng.append(np.reshape(np.array(list(map(charToInt,list(Eng_topTen[i])))),(keySize,-1)))
                            eng.append(np.reshape(np.array(list(map(charToInt,list(Eng_topTen[j])))),(keySize,-1)))
                            ciph.append(np.reshape(np.array(list(map(charToInt,list(topTenCipherList[jk])))),(keySize,-1)))
                            ciph.append(np.reshape(np.array(list(map(charToInt,list(topTenCipherList[k])))),(keySize,-1)))
                            ciph.append(np.reshape(np.array(list(map(charToInt,list(topTenCipherList[l])))),(keySize,-1)))

                            Pmatrix.append(np.append(np.append(eng[0],eng[1],axis = 1),eng[2],axis =1))
                            # print(len(Pmatrix))
                            for i2 in range(0,3):
                                for j2 in range(0,3):
                                    for k2 in range(0,3):
                                        if i2!=j2 and j2!=k2 and i2!=k2:
                                            Cmatrix.append(np.append(np.append(ciph[i2],ciph[j2],axis = 1),ciph[k2],axis =1))



                            for i3 in range(len(Cmatrix)):
                                for j3 in range(len(Pmatrix)):

                                    Pmatrix_inv = invKey(Pmatrix[j3], keySize)
                                    if not np.array_equal(Pmatrix_inv , np.zeros((keySize,keySize)) ):
#                                         print(Pmatrix_inv)
                                        key =np.mod( np.dot(Cmatrix[i3],Pmatrix_inv),26)
                                        keyInv = invKey(key,keySize)
                                        key =list(key.flat)
                                        if np.array_equal(keyInv, np.zeros((keySize,keySize)) ):
                                            continue
                                        PT = decrypt(keyInv.astype(int),keySize)
                                        ic = IdCoincidence(list(PT))
                                        if (ic > 0.055) and (ic < 0.075):
                                            print(key)
                                            print("\n")
                                            print(PT)
                                            opFile.write(str(key))
                                            opFile.write("\n")
                                            opFile.write(PT)
                                            opFile.write("\n")


    opFile.close()




# In[16]:


def cryptAnalysis():
    startTime = time.time()
    (topTenCipherList, keySize) = topTenFreq()
    (Eng_bigram, Eng_trigram, Eng_unigram) = ngram()
    if keySize ==2:
        Eng_topTen = Eng_bigram
    elif keySize == 3:
        Eng_topTen = Eng_trigram
    else:
        Eng_topTen = Eng_unigram


    if keySize == 1:
        print(topTenCipherList)
        print(Eng_topTen)
        forOne(topTenCipherList,Eng_topTen,keySize)
    elif keySize == 2:
        print(topTenCipherList)
        print(Eng_topTen)
        forTwo(topTenCipherList,Eng_topTen,keySize)
    else:
        print(topTenCipherList)
        print(Eng_topTen)
        forThree(topTenCipherList,Eng_topTen,keySize)
    print(time.time() - startTime)





# In[17]:


cryptAnalysis()
