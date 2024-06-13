# Let Em Cook

Someone cooked up some weird text

## Challenge

We are given one file containing ciphertext:
```
QnV0IGlz IHRoYXQg dGhlIG9u bHkgYmFz
ZSB0aGF0 IENURnMg d2lsbCB0 cnkgYW5k
IHVzZSB0 byB0cmlj ayB5b3U/ DQoNCjpN
WEJhK0Yu bUorRDVW NytFVjoq RjxHJThGFrom Base64
PEdJPkc5 QkkiR0Iu VkRBS1lR LUFURSc8
QlBEP3Mr REdeOTst LTFhPCo6 Z18kNFI+
REdeOktV QmxTR0FC bFJnIkZD bz4zRGc8
SUtGPEdP SUNqSTQ+ QjZuUURG PEdtREY8
R1s7SD5k U0ArRCM4 LENOM3Az RkRFIjhG
RiQubyUx M09PMihM WDMuNVk8 YUJLOHBP
QksmZDcr dHVrP0JQ OHRwQ0w3
```

Throwing it into cyberchef and messing around I was able to see that it was base64 encoded, decoding yields this:
```
But is that the only base that CTFs will try and use to trick you?

:MXBa+F.mJ+D5V7+EV:*F<G%8F<GI>G9BI"GB.VDAKYQ-ATE'<BPD?s+DG^9;--1a<*:g_$4R>DG^:KUBlSGABlRg"FCo>3Dg<IKF<GOICjI4>B6nQDF<GmDF<G[;H>dS@+D#8,CN3p3FDE"8FF$.o%13OO2(LX3.5Y<aBK8pOBK&d7+tuk?BP8tpCL7
```

From here its kind of hinted at that the next encoding type of some sort of baseXX encoding. So playing around again in cyberchef we can determine that its base85, decoding that yields:
```
Okay you got that but now I wrote everything in QWERTY.

Wxz viqz iqhhtfl oy vt pxlz kgzqzt zit tfzokt eiqkqeztk ltz? 

5+8$)4]0h9Q;h7Q%"0Q%hh-Qk_
```

Then from there, I played around with [dcode cipher identifier](https://www.dcode.fr/cipher-identifier) to try and identify what exactly they meant by they "wrote everything in QWERTY". I was able to conclude that a Mono-alphabetic Substitution was used, switching the alphabet to qwerty, meaning the order of keys from left to right on a normal keyboard from the top row down.

Changing the alphabet from `ABCDEFGHIJKLMNOPQRSTUVWXYZ` to `QWERTYUIOPASDFGHJKLZXCVBNM`. Decoding:
```
But what happens if we just rotate the entire character set?

5+8$)4]0p9A;p7A%"0A%pp-Ar_
```

From that hint we can kinda figure that its a rot cipher. Bruteforcing it using dcode again, we get this:
```
ASCII[!-~]+64	SIVBGR{N0W_Y0U_C@N_C00K_2}
```

I know a lot of people, especially myself, got caught on the qwerty step and that led to incorrect plaintext in certain bytes. I think a common mistake was letting decode decide the alphabet, which for the most part it got right but for the letters that weren't used, they weren't mapped correctly and were different from `QWERTYUIOPASDFGHJKLZXCVBNM` but looked extremely similar.



## Flag

`SIVBGR{N0W_Y0U_C@N_C00K_2}`