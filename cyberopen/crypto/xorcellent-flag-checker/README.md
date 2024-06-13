# xorcellent flag checker

Can you successfully figure out the flag to correctly pass this checker?

## Challenge

Not entirely sure whats up with this challenge. During the competition it was a .cpp file like I have in this repo, but on the github its now a compiled binary. It was also worth more than any other crypto challenge in the beginners room.

Anyways, during competition I opened up the cpp and saw this chunk of code:
```cpp

using namespace std;
    unsigned char hexArray1[] = {
        0xad, 0x75, 0xff, 0x83, 0xd5, 0xc0, 0x73, 0x16,
        0x2c, 0x2a, 0xf7, 0x2e, 0x7b, 0x45, 0xb4, 0x96,
        0xfb, 0x81, 0xa9, 0x7b, 0x69, 0x69
    };
        unsigned char hexArray2[] = {
        0xfe, 0x3c, 0xa9, 0xc1, 0x92, 0x92, 0x08, 0x6e, 
        0x1c, 0x58, 0xa8, 0x6c, 0x3b, 0x36, 0x85, 0xf5, 
        0x88, 0xde, 0xfb, 0x48, 0x1f, 0x14
    };
// Function to check if the input string is correct
bool checkString(const string& input) {
    if(input.size()==22) {
        for(int i=0;i<=22;i++) {
            char test = hexArray1[i]^hexArray2[i];
            if(input[i] != test) {
                return 0;
        }
        }
    } else {
        return 0;
    }
    return 1;

}
```

We can pretty easily tell here that the flag is gonna be the xor of these two hex arrays:
```cpp
char test = hexArray1[i]^hexArray2[i];
```

Calculating that and printing it out we get the flag.

Script:
```python
hexArray1 = [0xad, 0x75, 0xff, 0x83, 0xd5, 0xc0, 0x73, 0x16, 0x2c, 0x2a, 0xf7, 0x2e, 0x7b, 0x45, 0xb4, 0x96, 0xfb, 0x81, 0xa9, 0x7b, 0x69, 0x69]
hexArray2 = [0xfe, 0x3c, 0xa9, 0xc1, 0x92, 0x92, 0x08, 0x6e, 0x1c, 0x58, 0xa8, 0x6c, 0x3b, 0x36, 0x85, 0xf5, 0x88, 0xde, 0xfb, 0x48, 0x1f, 0x14]

result = [x ^ y for x, y in zip(hexArray1, hexArray2)]

for item in result:
    print(chr(item), end="")
```

## Flag

`SIVBGR{x0r_B@s1cs_R3v}`