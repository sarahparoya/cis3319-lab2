from des import DesKey
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #create a socket
port = 3000
s.bind(('', port)) #bind the socket to address
s.listen(1) #start listening
keystr = "imthekey" #key string must be multiple of 8
key = DesKey(keystr.encode('utf-8')) #create key
print("Server is running...")
conn, addr = s.accept() #accept connection request
print("Accept new connection from %s"%(str(addr)))
conn.send(str("Connection established").encode())
while True:
    rcv = conn.recv(1024)
    print("*"*18)
    print("Recieved ciphertext is: %s"%rcv.decode('utf-8', 'ignore'))
    pt = key.decrypt(rcv, padding=True).decode() #decrypt the key
    print("Recieved plaintext is: %s"%pt)
    print("*"*18)
    if pt == "bye": #if recieved msg is bye then break and close the connection
        break
    msg = input("Type message: ")
    ct = key.encrypt(msg.encode('utf-8'), padding=True)
    print("*"*18)
    print("key is ", keystr)
    print("Sent plaintext is: %s"%msg)
    print("Sent ciphertext is: %s"%ct.decode('utf-8', 'ignore'))
    print("*"*18)
    conn.send(ct) #send ciphertext
conn.close()