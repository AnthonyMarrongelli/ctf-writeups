# Spreading Out

ARIA is going out and touching files it shouldn't, can you track down where all it has gone?

https://uscybercombine-s4-spreading-out.chals.io/

Note: Fuzzing web directories is allowed.

## Challenge

Now the whole premise of this challenge was to use directory discovery tools to find the different endpoints for the flag.

When visiting the url, there isn't anything special to be found on the page. 

Using a tool like dirbuster we can try and bruteforce these endpoints. I spent an unbelievable amount of time letting my computer run hundreds of thousands of endpoints. I ended up getting 4/5 and not getting the fifth.

1. /robots.txt
2. /.env
3. /readme
4. /sitemap.xml

I could've pretty easily guessed that the last part of the flag was some variation of `_stopped}`, which it ended up being. 

Not a fan of this challenge as I don't believe it really teaches you something besides utilizing a automation tool.

## Partial Flag

`SIVBGR{ARIA_1s_spreading_3v3rywh3r3_4lw4ys_4nd_c4nnot_b3`
