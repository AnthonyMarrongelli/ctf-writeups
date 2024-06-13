# I Want to Believe

We've received a GIFt from what appears to be a signal coming from extraterrestrial life! Although, it appears they've used steganography to hide it inside of this .gif file. All we know is that it's in the form of a text file named 'iwanttobelieve.txt'. Can you recover it?

## Challenge

In this challenge we are given a `gift.gif`:

![Gift](./gift.gif)

And given the challenge description we can assume we are working with steganography. There was also a hint that went along with the challenge that was said something about a `GIFt tool`. After trying all of the normal steganography tricks and coming up with nothing. Searching around online for a `gift tool` I came across [this](https://github.com/dtmsecurity/gift).

Quickly glancing over the repo and reading through some of its functionality I saw this line:
```
python3 gift-cli.py --source output.gif recover recovered_hello.txt recovered_meme.jpg
```

And from there I figured this is probably exactly what we needed, given that we were given the file name.

Utilizing this tool we got this:

```
└─$ python gift/gift-cli.py --source gift.gif recover iwanttobelieve.txt
Recovering files from gift.gif
Recovering iwanttobelieve.txt
```

Taking a look at what was recovered:

```
HELLO HUMANS. WE COME IN PEACE.

MY NAME IS J0K3 AND I AM BROADCASTING THIS MESSAGE FROM SIGMA CENTAVRI.

WE FORMALLY APOLOGIZE FOR ABDUCTING SO MANY OF YOUR KIND. AND ALSO THE COWS.

WE HOPE YOU ACCEPT THIS TOKEN OF ATONEMENT.

OUR RESEARCH SHOWS IT IS HIGHLY PRIZED BY YOUR KIND.

 ___________________________
< SIVBGR{y0ur_g1ft_1s_h3r3} >
 ---------------------------
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||


PS: THE HUMANS WERE DROPPED OFF IN BORNEO.
ALSO, WE ARE KEEPING THE COWS. I NAMED THIS ONE "ANTHONY". 
```

Hello fellow Anthony.

## Flag

`SIVBGR{y0ur_g1ft_1s_h3r3}`
