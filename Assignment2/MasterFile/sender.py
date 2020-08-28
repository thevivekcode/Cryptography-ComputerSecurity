
# coding: utf-8

# In[19]:


import RSA
import vignere
import CertificationAuthority

def getCApublicKey():
   with open("CA_public_key",'r') as f:
       CA = f.read()

   CA = CA.split()
   e_CA = CA[2]
   n_CA = CA[3]
   return e_CA,n_CA

def getPrivateKey():
   with open("sender_private_key",'r') as f:
       s2 = f.read()
   s2 = s2.split()
   d_S2 = s2[2]
   n_S2 = s2[3]
   return d_S2,n_S2

def get_S1_PublicKey(e_CA,n_CA):
   with open("public_directory",'r') as f:
       sender_public_keys = f.read().split()
       e_S1 = RSA.RSA_decryption(sender_public_keys[2],int(e_CA),int(n_CA)).replace('{',"")
       n_S1 = RSA.RSA_decryption(sender_public_keys[3],int(e_CA),int(n_CA)).replace('{',"")
       return e_S1,n_S1


# In[21]:


if __name__ == "__main__":
    (d_S2,n_S2) = getPrivateKey()
    (e_CA,n_CA) = getCApublicKey()
    (e_S1,n_S1) = get_S1_PublicKey(e_CA,n_CA)
    with open('plainText','r') as f:
        pt = f.read().lower()
    pt = list(pt)
    text = "".join([i for i in pt if (i>='a' and i<='{') or i >='0' and i<= '9' ])
    with open('vignereKey','r') as f:
        Vkey = f.read()


    CT = vignere.VigenereEncryption(Vkey,text)
    if len(Vkey) <=9:
        cipherText = '0'+str(len(Vkey))+Vkey+CT

    else:
        cipherText = str(len(Vkey))+Vkey+CT


    DS = RSA.RSA_encryption(cipherText,int(d_S2),int(n_S2))


    finalCipherText = RSA.RSA_encryption(DS,int(e_S1),int(n_S1))


    with open("sender_TO_receiver",'w') as f:
        f.write(finalCipherText)
