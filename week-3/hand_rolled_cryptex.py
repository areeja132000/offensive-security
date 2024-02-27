from pwn import *

p = remote("offsec-chalbroker.osiris.cyber.nyu.edu", 7332)

print(p.recvuntil(b"The first round requires two inputs...\n > "))
p.send(bytes("flag.txt" + "\n", 'utf-8'))
print(p.recvuntil(b"\n > "))
p.send(bytes("0" + "\n", 'utf-8'))
print(p.recvuntil(b"*The first chamber opened! Ok, the second phase requires a single input...\n > "))
p.send(bytes("5" + "\n", 'utf-8'))
print(p.recvuntil(b"Nice, the second chamber opened! Ok, the final level requires another single input...\n > "))
p.send(b'\x02\x00\x0A')
print(p.recvline().decode('utf-8'))
print(p.recvline().decode('utf-8'))
print(p.recvline().decode('utf-8'))
print(p.recvline().decode('utf-8'))
print(p.recvline().decode('utf-8'))
print(p.recvline().decode('utf-8'))
p.close()