# Time

I tick but never tock, I age but never grow old, I'm always moving, never still, What am I that time can't hold?

nc time.chal.cyberjousting.com 1355

## Challenge

When running the binary it gives us this output

```
└─$ ./time
XOR Result:     99 73 184 205 187 87 67 65 122 245 170 121 70 58 207 53 136 59 137 154 137 247 165 251 245 187 196 149 121 166 210 127 86 37 160 167 212 88 73 213
```

Just from looking at it i'm guessing that is our flag after being xored. But lets disassemble and look at some code.

```c++
  local_20 = *(long *)(in_FS_OFFSET + 0x28);
  std::basic_ifstream<>::basic_ifstream((char *)local_228,0x102004);
                    /* try { // try from 001013d0 to 00101406 has its CatchHandler @ 001015b9 */
  cVar1 = std::basic_ifstream<>::is_open();
  if (cVar1 == '\x01') {
    std::__cxx11::basic_string<>::basic_string();
                    /* try { // try from 00101434 to 0010156a has its CatchHandler @ 001015a1 */
    std::getline<>(local_228,local_248);
    std::basic_ifstream<>::close();
    tVar5 = time((time_t *)0x0);
    srand((uint)tVar5);
    std::operator<<((basic_ostream *)std::cout,"XOR Result:     ");
    local_258 = local_248;
    local_268 = std::__cxx11::basic_string<>::begin();
    local_260 = std::__cxx11::basic_string<>::end();
    while( true ) {
      bVar2 = __gnu_cxx::operator!=((__normal_iterator *)&local_268,(__normal_iterator *)&local_260)
      ;
      if (!bVar2) break;
      local_250 = (char *)__gnu_cxx::__normal_iterator<>::operator*
                                    ((__normal_iterator<> *)&local_268);
      iVar3 = rand();
      pbVar4 = (basic_ostream *)
               std::basic_ostream<>::operator<<
                         ((basic_ostream<> *)std::cout,(int)*local_250 ^ iVar3 % 0x100);
      std::operator<<(pbVar4," ");
      __gnu_cxx::__normal_iterator<>::operator++((__normal_iterator<> *)&local_268);
    }
    std::basic_ostream<>::operator<<((basic_ostream<> *)std::cout,std::endl<>);
    uVar6 = 0;
    std::__cxx11::basic_string<>::~basic_string((basic_string<> *)local_248);
  }
  else {
    pbVar4 = std::operator<<((basic_ostream *)std::cerr,"Error opening file \'flag.txt\'");
    std::basic_ostream<>::operator<<((basic_ostream<> *)pbVar4,std::endl<>);
    uVar6 = 1;
  }
  std::basic_ifstream<>::~basic_ifstream((basic_ifstream<> *)local_228);
  if (local_20 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return uVar6;
```

So just pulling this segment out of ghidra, theres a few things that we can recognize here. The first thing the program is doing here is trying to open `flag.txt`, if successful continue, else print an error. After it does that we can see that it reads a line from the file 
```c++ 
std::getline<>(local_228,local_248);
```
which would be the flag, and then it seeds the random number generator with the current time: 
```c++
tVar5 = time((time_t *)0x0);
srand((uint)tVar5);
```

After this we see this segment:
```c++
local_250 = (char *)__gnu_cxx::__normal_iterator<>::operator*
                                    ((__normal_iterator<> *)&local_268);
      iVar3 = rand();
      pbVar4 = (basic_ostream *)
               std::basic_ostream<>::operator<<
                         ((basic_ostream<> *)std::cout,(int)*local_250 ^ iVar3 % 0x100);
      std::operator<<(pbVar4," ");
```

Couple of things to pick out here, an iterator is being created to iterate through the flag, a random value is being generated, and then that value is being xored with the current index of the flag. We also see the modulus by `0x100` but thats just keeping the random value within 1 byte so we keep our result in one byte.

So how can we retrieve the flag? We'll the output being spit out to us from the server uses the time that we connect to the server. So if we can retrieve the correct time, we can just xor the plaintext again with the same sequence of random numbers to retrieve our plaintext.

To grab the correct time, I wrote a little python script that just connects and prints the time as well as the ciphertext.
```python
from pwn import *
import time

p = remote('time.chal.cyberjousting.com', 1355)
log.info(int(time.time()))
log.info(p.recvuntil(b'\n').decode())
p.close()
```
```
└─$ python solve.py
[+] Opening connection to time.chal.cyberjousting.com on port 1355: Done
[*] 1716168252
[*] XOR Result:     98 222 123 236 220 185 246 157 139 204 53 17 120 62 218 141 241 67 202 18 201 8 253 160 240 3 15 250 15 52 4 5 93 21 150 133 118 25 243 104 
[*] Closed connection to time.chal.cyberjousting.com port 1355
```
Now that we have a time and corresponding ciphertext, we can rewrite the program to re-encrypt the ciphertext and give us plaintext.

```c++
#include <iostream>
#include <string>
#include <vector>

int main() {
    std::vector<int> xorResults = {
        98, 222, 123, 236, 220, 185, 246, 157, 139, 204, 53, 17, 120, 62, 218,
        141, 241, 67, 202, 18, 201, 8, 253, 160, 240, 3, 15, 250, 15, 52, 4, 5,
        93, 21, 150, 133, 118, 25, 243, 104
    };
    std::string originalText;
    unsigned int seed = 1716168252;  
    srand(seed);

    for (int xorValue : xorResults) {
        int randByte = rand() % 256; 
        char originalChar = static_cast<char>(xorValue ^ randByte); 
        originalText += originalChar;
    }

    std::cout << "Original text: " << originalText << std::endl;
    return 0;
}
```

Running this c++ program we recieve the flag:
```
└─$ ./solve               
Original text: byuctf{ooooooooh_a_seeded_PRNGGGGGGGGGG}
```

## Flag

`byuctf{ooooooooh_a_seeded_PRNGGGGGGGGGG}`