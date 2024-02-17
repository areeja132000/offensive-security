from pwn import *

for num1 in range (256):
  print("{0}".format(num1))
  p = remote("offsec-chalbroker.osiris.cyber.nyu.edu", 1250)

  p.recvuntil(b"What's the key?\n")
  p.send(bytes("{0}".format(num1) + "\n", 'utf-8'))
  result = p.recvall(timeout=5).decode('utf-8')
  print(result)
  if (result != ""):
    print("RESULT    num1: {0}".format(num1))
    break
  p.close()