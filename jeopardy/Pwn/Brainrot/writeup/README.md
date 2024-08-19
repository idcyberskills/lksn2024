- It will execute whatever user input as assembly code
- Binary has strict protection that only allows a few syscalls, i.e. open, read, write
- This program reveals the flag position and prompt you to input shellcode
- The only viable shellcode technique involves using open, read, and write called ORW

## How to solve
- open("/flagdottieksti.txt") > it will open flag file, and return it's file descriptor (fd)
- read("rax", "rsp", 0x100) > read fd from rax register, and place the data to rsp (stack pointer) 0x100 bytes
- write(1, "rsp", 0x100) > write stack pointer to stdout (1), then flag will appear

For full exploit solve.py

## Referrences
https://tripoloski1337.github.io/experience/2019/09/09/writting-open-read-write-shellcode.html
https://kazma.tw/2024/02/07/Pwnable-tw-orw-Writeup/
