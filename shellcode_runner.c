// gcc shellcode_runner.c -z execstack -o shellcode_runner
#include <stdio.h>

int main() {
  char buf[1024];
  fgets(buf, 1024, stdin);

  (*(int (*)())buf)();
}
