#include <stdio.h>

void obfuscatedPrint() { 
    char str[] = {104, 97, 99, 107, 117, 99, 102, 123, 54, 101, 48, 98, 102, 117, 115, 99, 52, 116, 105, 48, 110, 95, 49, 115, 95, 55, 117, 110, 33, 125, 0};
    for (int i = 0; str[i] != 0; ++i) {
        putchar(str[i]); 
    }
} 

int main() { 
    obfuscatedPrint();
    return 0; 
}