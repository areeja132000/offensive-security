'''
CBC oracle padding attack
'''
import math
from pwn import *

def read_input(filename):
  with open(filename) as file:
    data = file.read()
  iv = data[data.index("IV: ")+4:data.index("Ciphertext: ")-1]
  ct = data[data.index("Ciphertext: ")+12:-1]
  return (iv, ct)

def hex_to_hex_list(m):
  output=[]
  for i in range(len(m)//2):
    output.append(int("0x"+m[2*i:2*i+2], 16))
  return output

def hex_list_to_message(sublist):
  output = ''
  for item in sublist:
    temp = hex(item)[2:]
    if (len(temp)<2):
      temp = '0'+temp
    output = output + temp
  return output

bytes_per_block = 16
iv, ct = read_input("cbc.txt")

iv_list = hex_to_hex_list(iv)

num_lists = math.ceil(len(ct)/2/bytes_per_block)
dict_of_sublists = {}
for i in range(0, num_lists):
  dict_of_sublists['l'+str(i)] = hex_to_hex_list(ct[bytes_per_block*2*i:bytes_per_block*2*i+bytes_per_block*2])

intermediate = {}
x = num_lists-1
while len(dict_of_sublists)>0 :
  print("x: {0}".format(x))
  previous_text = []
  temp = []
  if (x-1 < 0):
    previous_text = iv_list
    temp = iv_list.copy()
  else:
    previous_text = dict_of_sublists['l'+str(x-1)]
    temp = dict_of_sublists['l'+str(x-1)].copy()
    
  p=remote("offsec-chalbroker.osiris.cyber.nyu.edu", 1478)
  recieved = p.recvuntil(b"abc123): ").decode('utf-8')
  p.send(b"aga8870" + b"\n")
  intermediate_text = []
  i = bytes_per_block-1
  while i > -1:
    #print("i: {0}".format(i))
    #previous_text[i] is being changed 
    ti = 0
    response = False
    padding = bytes_per_block-i
    #print("padding")
    #print(padding)
    s = len(intermediate_text)-1
    for l in range(bytes_per_block-1,i,-1):
      previous_text[l] = intermediate_text[s]^padding
      #print(intermediate_text[s]^padding)
      s-=1
    #print(previous_text)
    
    while not response:
      #print("while")
      #print(previous_text)
      #print("i: {0}".format(i))
      #print("ti: {0}".format(ti))
      
      previous_text[i] = ti
      #print(previous_text)
      
      if (x-1 < 0):
        iv_list = previous_text
      else:
        dict_of_sublists['l'+str(x-1)] = previous_text
      message = hex_list_to_message(iv_list)
      for m in range(len(dict_of_sublists)):
        message = message + hex_list_to_message(dict_of_sublists['l'+str(m)])
      #print("MESSAGE")
      #print(message)

      
      recieved = p.recvuntil(b"message: \n").decode('utf-8')
      p.send(message.encode() + b"\n")
      recieved = p.recvline().decode('utf-8')
      
      if "oh no bad pad so sad" not in recieved:
        #print("success")
        #print("i: {0}".format(i))
        #print("ti: {0}".format(ti))
        intermediate_byte = ti^(padding)
        #print("intermediate_byte: {0}".format(intermediate_byte))
        intermediate_text.insert(0, intermediate_byte)
        print(intermediate_text)
        response = True    
      ti+=1
    if (x-1<0):
      iv_list = temp
    else:
      dict_of_sublists['l'+str(x-1)] = temp
    i-=1
  popped = dict_of_sublists.pop('l'+str(x))
  intermediate['l'+str(x)] = intermediate_text
  x-=1
  p.close()
  
output = ''
print("intermediate")
for i in range(num_lists):
  output = output + hex_list_to_message(intermediate['l'+str(i)])
print(output)
  










 
