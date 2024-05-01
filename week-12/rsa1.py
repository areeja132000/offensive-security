
'''
RSA - small modulus attack
We can see that m^e is probably < N, which means m^e mod n is just m^e. 
We can reverse m^e to find the plaintext.
m^e = c
c^(1/e) = m
'''

def int_to_ascii(m):
  m = hex(int(m))[2:]
  output=''
  for i in range(len(m)//2):
    output = output + chr(int("0x"+m[2*i:2*i+2], 16))
  return output

from gmpy2 import *

with open("rsa1.txt") as file:
  data = file.read()

n = int(data[data.index("n = ")+4:data.index("e = ")])
e = int(data[data.index("e = ")+4:data.index("c = ")])
c = int(data[data.index("c = ")+4:])

gmpy2.get_context().precision=300
m = gmpy2.root(c,e)
print(int_to_ascii(m))








 
