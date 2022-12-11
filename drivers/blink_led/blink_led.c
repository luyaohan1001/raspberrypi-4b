#include <stdio.h>
#include <string.h>
#include <unistd.h>


#define DEFAULT_BUFFER_SIZE 256
static char write_content[DEFAULT_BUFFER_SIZE];

int main() {
    FILE *filp;

    filp = fopen("/sys/class/gpio/export", "w");
    strcpy(write_content, "26");
    fwrite(write_content, sizeof(char), strlen(write_content), filp);
    fclose(filp);


    filp = fopen("/sys/class/gpio/gpio26/direction", "w");
    strcpy(write_content, "out");
    fwrite(write_content, sizeof(char), strlen(write_content), filp);
    fclose(filp);


    filp = fopen("/sys/class/gpio/gpio26/value", "w");
    strcpy(write_content, "1");
    fwrite(write_content, sizeof(char), strlen(write_content), filp);
    fclose(filp);


    while (1) {
    filp = fopen("/sys/class/gpio/gpio26/value", "w");
    strcpy(write_content, "1");
    fwrite(write_content, sizeof(char), strlen(write_content), filp);
    fclose(filp);
    sleep(1);
    filp = fopen("/sys/class/gpio/gpio26/value", "w");
    strcpy(write_content, "0");
    fwrite(write_content, sizeof(char), strlen(write_content), filp);
    fclose(filp);
    sleep(1);
    }


    return 0;
}
