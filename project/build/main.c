#include<stdio.h>

#define DEBUG 1

int main() {
    #ifdef DEBUG
        printf("hello debug\n");
    #else
        printf("hello world\n");
    #endif
    return 0;
}
