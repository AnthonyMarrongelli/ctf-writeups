# Lost Some Magic

## Overview:

Category: Miscellaneous

## Description

I had a flag but I can no longer open it up. I think I compressed it beforehand but I can't remember how many times! And I may have lost some magic along the way....

## Approach

Okay so reading the challenge description the file we are given has been compressed a few times and "lost some magic along the way". First thing that comes to mind is that some bytes were changed/lost, which i've seen before in other challenges. Specifically header bytes are a target.


## Attack

Lets through the file in cyberchef and examine the hex:

```c
42 00 00 39 ...
```

Seeing the 42 as the first byte here and 39 as the last, I discovered that `bzip2` headers are as follows:
- 42 Followed by 5A 68
- Fourth byte is in the range 31-39

So the file definitely fits that criteria right now, lets change thats null bytes to `5A 68`.

Doing so and then running bzip2 decompress we can see some keywords like `data`, `flag`, and `kali`. Lets download the file and check it out:
```
└─$ file bzip2decompressed 
bzip2decompressed: tar archive (old), file data, mode 0000644, uid 0001750, gid 0001750, size 00000000115, seconds 14561034515, comment: ust
```

Cool a tar archive, lets use untar on cyberchef. We get another data file, lets analyze the hex:
```
00 8b 08 08 6e 37 c4 65 00 03 66 6c 61 67 00 0b c9 48 55 48 cb 49 4c 57 c8 2c b6 52 28 2e 4f cc 2d 70 0e 71 ab 76 36 30 34 34 4e 2e 31 cc 4b 8f 2f c9 30 8e cf 4d 4c 37 4c 8e cf 2b cd 4d 4a 2d 32 ad e5 02 00 a8 d6 98 73 34 00 00 00
```

Looking at the first few bytes, it looks like a gunzip header, which is `1F 8B`. Lets change it and then try to gunzip it:
```
The flag is: swampCTF{C0113ct1ng_th3_mag1c_number5}
```


## Flag

swampCTF{C0113ct1ng_th3_mag1c_number5}

# References
1. https://gchq.github.io/CyberChef/
