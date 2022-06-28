.data


msg:
    .ascii "Hello World on arm64!\n" // comment with forward slash

len = . - msg


.text
   
.global _start

_start:
    mov x0, #1      // fd = 1 --> STDOUT_FILNO
    ldr x1, =msg    // buffer = message
    ldr x2, =len    // buffer = length
    mov w8, #64     // syscall 64 : write
    svc #0          // Supervisor call - the user triggers an exception. 

    mov x0, #0      // status = 0
    mov w8, #93     // syscall 93 : exit
    svc #0          // Supervisor call
    
