import os 
import threading
import socket
def search(ip_adress):
    comando="ping -c 1 "+ip_adress
    
    response=os.popen (comando).read() # string

    if "bytes=" in response:
        print("Respuesta desde : ", ip_adress)
        #print(comando)
for ip in range(1,254):
    current_ip="192.168.1."+str(ip)
    #print("analizando la ip", current_ip)

    run=threading. Thread (target=search, args = (current_ip,))
    run.start()

