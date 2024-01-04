import pyfiglet
import sys
import socket
import os
import dirhunt
import requests
from datetime import datetime

#Menamppilkan menu awal
ascii_banner = pyfiglet.figlet_format("ReWS")
print(ascii_banner)
print("="*50)
print("Port Scanner & Directory Scanner & Subdomain Scanner")
print("="*50)

#Mengambil argumen ke 1 yang berisikan domain target lalu dimasukan kedalam variable t
t = sys.argv[1]

if len(sys.argv) == 2:
	# translate domain menjadi IPv4
	target = socket.gethostbyname(sys.argv[1])
else:
	print("Invalid Argument!")

# Menampilkan terget domain dan waktu mulai scanning port
print("-" * 50)
print("Scanning Port Target: " + target)
print("Scanning started at:" + str(datetime.now()))
print("-" * 50)

# Scanning dengan try agar dapat mengelola program jika ada error
try:
	
	# scan port mulai port 1 sampai 65535
	for port in range(1,65535):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		socket.setdefaulttimeout(1)
		
		# menampilkan port yang ditemukan
		result = s.connect_ex((target,port))
		if result ==0:
			print("Port {} is open".format(port))
		s.close()
		
#Handling error program berhenti, hostname tidak ditemukan dan server tidak merespon
except KeyboardInterrupt:
		print("\n Anda menghentikan program!")
		sys.exit()
except socket.gaierror:
		print("\n Hostname tidak ditemukan!")
		sys.exit()
except socket.error:
		print("\n Server tidak merespon!")
		sys.exit()

# Menampilkan terget domain dan waktu mulai scanning directory
print("-" * 50)
print("Scanning Directory Target: " + t)
print("Scanning started at:" + str(datetime.now()))
print("-" * 50)
#Menjalankan scanning directory dengan menggunakan dirhunt
os.system('dirhunt '+t)


# mendefinisikan function scanning subdomain
def domain_scanner(dom,sub_dom):
    print("-" * 50)
    print("Scanning Subdomain Target: " + t)
    print("Scanning started at:" + str(datetime.now()))
    print("-" * 50)

    # looping scan subdomain
    for subdomain in sub_dom:

        # menyusun variable untuk dijadikan url yang akan di scan dimasukan ke variable url
        url = f"https://{subdomain}.{t}"

        # handling menggunakan try dan except
        try:
            # mengirim request dengan method get berisikan url 
            requests.get(url)

            # jika domain valid maka akan ditampilkan
            print(f'Domain ditemukan [+] {url}')

        # jika domain tidak valid akan melanjutkan looping
        except requests.ConnectionError:
            pass

# membuka file berisikan list subdomain
with open('subdo.txt','r') as file:

    # Membaca isi file
    name = file.read()

    # menggunakan function splitline() untuk memisah perbaris setiap subdomain pada file subdo.txt
    sub_dom = name.splitlines()

# menjalankan function scaning subdomain
domain_scanner(t,sub_dom)
