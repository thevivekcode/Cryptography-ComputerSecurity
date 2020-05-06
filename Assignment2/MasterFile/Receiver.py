
# coding: utf-8

# In[56]:


import RSA
import vignere
import CertificationAuthority


# In[57]:


def getCApublicKey():
   with open("CA_public_key",'r') as f:
       CA = f.read()

   CA = CA.split()
   e_CA = CA[2]
   n_CA = CA[3]
   return e_CA,n_CA

def getPrivateKey():
   with open("receiver_private_key",'r') as f:
       s1 = f.read()
   s1 = s1.split()
   d_S1 = s1[2]
   n_S1 = s1[3]
   return d_S1,n_S1

def get_S2_PublicKey(e_CA,n_CA):
   with open("public_directory",'r') as f:
       sender_public_keys = f.read().split()
       e_S2 = RSA.RSA_decryption(sender_public_keys[6],int(e_CA),int(n_CA)).replace('{',"")
       n_S2 = RSA.RSA_decryption(sender_public_keys[7],int(e_CA),int(n_CA)).replace('{',"")
       return e_S2,n_S2


# In[58]:


if __name__ == "__main__":
    (d_S1,n_S1) = getPrivateKey()
    (e_CA,n_CA) = getCApublicKey()
    (e_S2,n_S2) = get_S2_PublicKey(e_CA,n_CA)

    #-------------------RECEIVING MESSAGE---------------------

    with open("sender_TO_receiver",'r') as f:
        cipherText = f.read()

    CT1 = RSA.RSA_decryption(cipherText,int(d_S1),int(n_S1))
    CT1 = list(CT1)

    for i in range(len(CT1)-1,-1,-1):
        if CT1[i]!='{':
            break
        else:
            del CT1[i]

    CT1 = "".join(CT1)
    CT2 = RSA.RSA_decryption(CT1,int(e_S2),int(n_S2))

    CT2 = CT2.replace("{","")

    CT3 = list(CT2)
    Vkey_len = int("".join(CT3[:2]))
    Vkey = "".join(CT3[2:2+Vkey_len])
    finalCT = "".join(CT3[2+Vkey_len:])
    PT  = vignere.VigenereDecryption(Vkey,finalCT)

    print(PT)
    #----------------------------------------------------------
