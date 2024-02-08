# Lettice

## Overview:

Category: Reverse Engineering

Difficulty: Easy

## What We Have:

```challenge.c```
```c
#0x696E636C756465 0x3C737464696F2E683E void 0x6F6266757363617465645072696E74() { char 0x737472[] = {104, 97, 99, 107, 117, 99, 102, 123, 54, 101, 48, 98, 102, 117, 115, 99, 52, 116, 105, 48, 110, 95, 49, 115, 95, 55, 117, 110, 33, 125, 0};  0x666F72 (int 0x69 = 0; 0x737472[0x69] != 0; ++0x69) { 0x70757463686172(0x737472[0x69]); }} int 0x6D61696E() { 0x6F6266757363617465645072696E74(); 0x72657475726E 0; }
```

## Approach

From what we can see it looks to resemble a c program. Lets start trying to make it more readable.


```c
#0x696E636C756465 0x3C737464696F2E683E

void 0x6F6266757363617465645072696E74() { 
    char 0x737472[] = {104, 97, 99, 107, 117, 99, 102, 123, 54, 101, 48, 98, 102, 117, 115, 99, 52, 116, 105, 48, 110, 95, 49, 115, 95, 55, 117, 110, 33, 125, 0};
    0x666F72 (int 0x69 = 0; 0x737472[0x69] != 0; ++0x69) {
        0x70757463686172(0x737472[0x69]); 
    }
} 

int 0x6D61696E() { 
    0x6F6266757363617465645072696E74();
    0x72657475726E 0; 
}
```

And just like that we have something that is structured like a normal program. Now anyone that has ever seen hex before can recognize that some of these values being displayed are hex.

Lets take the first hex value we see and convert it to ascii: `0x696E636C756465` converts to `include`.

Here is an example of a hex to ascii converter: https://www.rapidtables.com/convert/number/hex-to-ascii.html.



## Attack

So now that we have an idea that the hex values convert to ascii code, lets go and convert them all back to ascii.


```c
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
```
Now lets run the reversed program.


```text
$ gcc -o solve solve.c 
$ ./solve 
  hackucf{6e0bfusc4ti0n_1s_7un!} 
```

It's also worth noting that if you recognize that the array of decimal numbers may be an important string of text, you can plug them into something like https://www.rapidtables.com/convert/number/ascii-hex-bin-dec-converter.html to convert from decimal to ascii.

## Flag

hackucf{6e0bfusc4ti0n_1s_7un!}
