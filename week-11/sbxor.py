with open("sbxor_ciphertext.txt", 'r') as file:
  data = file.read()

for i in range(256):
  decrypted = ''
  for x in range(len(data)//2):
    current_byte = int(data[2*x:2*x+2], 16)
    decrypted = decrypted + chr(current_byte ^ i)
  print(decrypted)