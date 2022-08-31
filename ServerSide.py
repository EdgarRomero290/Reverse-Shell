import sys
import socket



# Crear Socket para conectar dos PC

def createSocket():
    try:
        global host     # IP en este caso la ip del server
        global port     # Puerto de comunicacion 
        global s        # Socket
        host=''
        port= 9999      #puerto muy poco utilizado
        s= socket.socket()
    except socket.error as msg:
        print('Socket Creation Error' + str(msg) )

######

# Binding Socket and Connections

def bindSocket():
    try:
        global host     # IP en este caso la ip del server
        global port     # Puerto de comunicacion 
        global s        # Socket
        print('Bindind the port '+ str(port))

        s.bind((host,port)) #el metodo bind recibe los parametros en forma de tupla
        s.listen(5) 


    except socket.error as msg:
        print('Socket Binding Error' + str(msg))
        bindSocket()  ##es caso de un error aplicamos recursividad

########        

# Accepting Connections

def socketAccept():
    global conn
    conn,address=s.accept()
    print('Connection has been established '+' IP '+ address[0]+ ' | '+'Port ' + str(address[1]))
    sendCommands()
    conn.close()

#########

# Sending Commands

def sendCommands():
    while True:   #Loop infinito
        cmd= input()
        if cmd =='quit':
            conn.close()
            s.close()
            sys.exit()
        if len(str.encode(cmd))> 0:
            conn.send(str.encode(cmd))
            clienteResponse= str(conn.recv(1024),'utf-8')
            print(clienteResponse, end='')

def main():
    createSocket()
    bindSocket()
    socketAccept()

main()

