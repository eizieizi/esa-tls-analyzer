import re,os,collections
from functions import *



tlsversion=[]
ciphers=[]
zaehler=0
logs=[]


if not os.path.exists("./logs"):
    print("./logs folder not existing, creating")
    os.makedirs("./logs")
    print("Downloading Logs from ESA")
    logs=download_logs()

if os.path.exists("./logs"):
    x=input("\n Would you like to re-use existing Logs? If answering no, the script will fetch logs via FTP from ESA yes/no: ")
    
    if  (x=="yes" or x=="YES" or x=="Yes"):
        
        #Returns all Filenames as List in folder ./logs
        for files in os.walk("./logs", topdown=True):
            file_list=(files[2])
        
        #Reads all files into "logs" list. 
        for x in file_list:
            with open(f"./logs/{x}") as f:
                logs += f.read().splitlines()

    
    if  (x=="no" or x=="NO" or x=="No"):
        print("Downloading Logs from ESA")
        logs=download_logs()


#Iterates over every line in list and scans for TLS-Version and used ciphers to store in list. 
for x in logs:
    try:
        #Regex with lookahead and lookbehind for TLS Version and used Ciphers
        tlsversion.append(re.search(r"(?<=TLS success protocol ).*(?= cipher)",x).group())
        ciphers.append(re.search(r"(?<=cipher ).*",x).group())

        #counter+=1
        #For troublehooting, to prevent long regex scanning time. 
        # if counter >=100000:
        #     break
    except:
        pass

#Count duplicate TLS-Version in list "tlsversion" and store the used tls-versions and how often the tls-version was used in a dictionary. .mostcommon() sorts the dictionary.
tlsversion_count=dict((collections.Counter(tlsversion).most_common()))
#Count duplicate events in lists and store TLS-cipher and how often the tls-cipher was used. .mostcommon() sorts the dictionary.
ciphers_count=dict((collections.Counter(ciphers).most_common()))

#Create two lists for mathplotlib from dict and create plot from function
tls_version_list=list(tlsversion_count.keys())
tls_version_count_list=list(tlsversion_count.values())

create_plot(tls_version_list,tls_version_count_list,"Used TLS Versions")

#Create two lists for mathplotlib from dict and create plot from function
cipher_list=list(ciphers_count.keys())
ciphercount_list=list(ciphers_count.values())

create_plot(cipher_list,ciphercount_list,"Used TLS Ciphers")