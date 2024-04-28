import math 

def normalized_hamming(a, b):
  dist = bin(a ^ b).count('1')
  return dist

def create_sublists(num_lists):
  dict_of_sublists = {}
  for i in range(0, num_lists):
    dict_of_sublists['l'+str(i)] = hex_list[max_key_length*i:max_key_length*i+max_key_length]
  return dict_of_sublists 

with open("ciphertext2.txt", 'r') as file:
  data = file.read()
  hex_list = []
  for x in range(len(data)//2):
    current_byte = int(data[2*x:2*x+2], 16)
    hex_list.append(current_byte)
  
keys_lengths_hamming = []
for max_key_length in range(2, 30):
  num_lists = math.ceil(len(hex_list)/max_key_length)
  dict_of_sublists = create_sublists(num_lists)
  dict_length = len(dict_of_sublists)
  if (dict_length%2 == 0):
    dict_length = dict_length-2
  else:
    dict_length = dict_length-1

  # Pair up dictionary objects and compute hamming distance
  summation = 0
  for i in range(dict_length//2):
    list1 = dict_of_sublists['l'+str(i*2)]
    list2 = dict_of_sublists['l'+str(i*2+1)]
    diff = 0
    for x in range(len(list1)):
      diff = diff + normalized_hamming(list1[x], list2[x])
    summation = summation + (diff/max_key_length)
  average = summation/(dict_length//2)
  keys_lengths_hamming.append((max_key_length, average))

keys_lengths_hamming.sort(key=lambda s: s[1])
print("Best key lengths:")
for i in range (5):
  print("key length: {0} average hamming distance: {1}".format(keys_lengths_hamming[i][0], keys_lengths_hamming[i][1]))









 
