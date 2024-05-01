'''
RSA - common modulus attack (same m, n, different e)
Modulus arithmetic rules: 
1. (A * B) mod C = (A mod C * B mod C) mod C
2. (A ^ B) mod C = ((A mod C) ^ B) mod C

Consider:
((c1^u mod n)*(c2^v mod n)) mod n 
= (((m^e1 mod n)^u mod n)*((m^e2 mod n)^v mod n)) mod n.   
= ((m^(e1*u) mod n)*(m^(e2*v) mod n)) mod n.   by 2. 
= m^(e1*u+e2*v) mod n.                         by 1.
If we make e1*u+e2*v = 1, we will get m^1 = m,
which will give us the flag
'''
from gmpy2 import *

def read_input(filename):
  with open(filename) as file:
    data = file.read()
  n = int(data[data.index("n = ")+4:data.index("e = ")])
  e = int(data[data.index("e = ")+4:data.index("c = ")])
  c = int(data[data.index("c = ")+4:])
  return (n, e, c)

def int_to_ascii(m):
  m = hex(int(m))[2:]
  output=''
  for i in range(len(m)//2):
    output = output + chr(int("0x"+m[2*i:2*i+2], 16))
  return output

data1 = read_input("rsa2_1.txt")
data2 = read_input("rsa2_2.txt")

'''
Consider Bézout's identity: ax + by = gcd(a,b) 
When a and b are coprime (gcd(a,b) = 1), x is the modular multiplicative inverse of a modulo b.
This can be caluclated with gmpy.invert(a,b)
'''
u = gmpy2.invert(data1[1], data2[1])

'''
From (e1*u)+(e2*v) = 1, we can rearrange to solve for v: 
v = (1 - (e1*u))/e2
'''
v = (1 - data1[1]*u)//data2[1]

m = (pow(data1[2], u, data1[0])*pow(data2[2], v, data1[0]))%data1[0]
print(m)
flag = int_to_ascii(m)
print(flag)












 
