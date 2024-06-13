# The Email Where It Happens

Howdy Truth Seekers! It seems that some malware that was strategically shared has begun to phone back home! We believe that this might have some very important information that could help lead us to finally getting to the bottom of this conspiracy regarding extraterrestrial life. Unfortunately the original developer of this tool was recently promoted to customer status and is no longer on good terms with the orginization. This means that we don't have any information on how to decode this traffic. Unfortunately all I have is a PCAP. Can you help us out here?

## Challenge

For this challenge we are just given a pcap.

Opening it up we can just see a list of udp packets.

![UDP Packets](./pictures/udp.png)

From here we can right click one of the packets and click Follow->UDP Stream:

```
............,FIQSUIJKEEVCCKRBFIQSUIJKEEVAUSKOKRCVEQ2FKBKE.0.meowcorp.cloud.................,KRBAIVGEKQ2UKJHU4SKDEBGUCSKMEBBU6TKNKVHESQ2B.1.meowcorp.cloud.................,KREU6TQKFIQSUIJKEEVCCKRBFIQSUIJKEEVAUVCPHIQG.2.meowcorp.cloud.................,E4TJMFXC44TJM5TXGQDBOJSWCNJRFZRWY33VMQFEMUSP.3.meowcorp.cloud.................,JU5CA2LMNR2W22LOMF2GSQDTMVRXEZLUOMXHK4YKIRAV.4.meowcorp.cloud.................,IRJ2EA2S6MJUF4ZDAMRUIAYTMORTGMFFGVKCJI5CAUSF.5.meowcorp.cloud.................,HIQEGT2OIZEVETKFIQQEKWCUKJAVIRKSKJCVGVCSJFAU.6.meowcorp.cloud.................,YICMJFDEKCSCJ5CFSOQKJBSWY3DPEBBHE2LBNYWAUCSX.7.meowcorp.cloud.................,MUQGC4DQOJSWG2LBORSSA5DIMUQGS3TGN5ZG2YLUNFXW.8.meowcorp.cloud.................,4IDZN52SA2DBOZSSA4DSN53GSZDFMQQHK4ZAOJSWOYLS.9.meowcorp.cloud.................,MRUW4ZZAPFXXK4RAMRUXGY3POZSXE6JAMFXGIIDQOJXW.10.meowcorp.cloud.................,24DUEBSGK5DFNZ2GS33OEBXWMIDFPB2HEYLUMVZHEZLT.11.meowcorp.cloud.................,ORZGSYLMEBWGSZTFEBXW4ICFMFZHI2BOEBKGQ2LTEBUX.12.meowcorp.cloud.................,GIDGMFXHIYLTORUWGIDOMV3XGIDBNZSCA4DVORZSA5LT.13.meowcorp.cloud.................,EBUW4IDQN5ZWS5DJN5XCAZTPOIQHK4ZAORXSAYTFM5UW.14.meowcorp.cloud.................,4IDQNBQXGZJAOR3W6IDPMYQG65LSEBYGYYLOEBTG64RA.15.meowcorp.cloud.................,O5XXE3DEEBSG63LJNZQXI2LPNYXCAV3FEB2W4ZDFOJZX.16.meowcorp.cloud.................,IYLOMQQHS33VEBUGC5TFEBZXI33SMVSCA5DIMUQGY2LG.17.meowcorp.cloud.................,MVTG64TNEBUW4IDUNBSSAYLHOJSWKZBAOVYG63RANRXW.18.meowcorp.cloud.................,GYLUNFXW4IDBNZSCA43FOQQHI2DFEBWG6Y3LEB2G6IDV.19.meowcorp.cloud.................,ORUWY2L2MUQHI2DFEBYGC43TO5XXEZBAORXSAISTJFLE.20.meowcorp.cloud.................,ER2SPN3WQMC7NYZTGZDTL4ZTEX3CGRZTG435EIXCAV3F.21.meowcorp.cloud.................,EB3WS3DMEBTG63DMN53SA5LQEBQWM5DFOIQGS3TWMVZX.22.meowcorp.cloud.................,I2LHMF2GS3THEB2GQZJAOBZG65TJMRSWIIDMNFTGKZTP.23.meowcorp.cloud.................,OJWSA53JORUCAZTVOJ2GQZLSEBUW443UOJ2WG5DJN5XH.24.meowcorp.cloud.................,GLQKBJJWC3DVORQXI2LPNZZSYCSUOJUWC3THNRSSAQTP.25.meowcorp.cloud.................,NFZQUKRBFIQSUIJKEEVCCKRBFIQSUIJKBJCU4RBAKRJE.26.meowcorp.cloud.................,CTSTJVEVGU2JJ5HAUKRBFIQSUIJKEEVCCKRBFIQSUIJK.27.meowcorp.cloud.....
```

So here we can see abunch of dns queries formatted as `*.(number in order).meowcorp.cloud`. They key here was to extract the `*` in at the beginning of each query and piece them together into a blob of base32. Then from there decoding it to retrieve the flag.

Automation Script:
```python
import re
import base64

with open('udp-stream', 'r') as file:
    contents = file.readline()

pattern = r'\.\d+\.meowcorp\.cloud'
contents = re.sub(pattern, '', contents)
base32_blob = contents.replace('.*.meowcorp.cloud', '').replace(',', '').replace('.', '')

print(base64.b32decode(base32_blob).decode())
```

Running it gives this:
```
*!*!*!*!*!*!*!*!*
INTERCEPTED ELECTRONIC MAIL COMMUNICATION
*!*!*!*!*!*!*!*!*
TO: brian.riggs@area51.cloud
FROM: illuminati@secrets.us
DATE: 5/14/2024@16:33
SUBJ: RE: CONFIRMED EXTRATERRESTRIAL LIFE
BODY:
Hello Brian,

We appreciate the information you have provided us regarding your discovery and prompt detention of extraterrestrial life on Earth. This is fantastic news and puts us in position for us to begin phase two of our plan for world domination. We understand you have stored the lifeform in the agreed upon location and set the lock to utilize the password to "SIVBGR{wh0_n33ds_32_b4s3s}". We will follow up after investigating the provided lifeform with further instructions.

Salutations,
Triangle Bois
*!*!*!*!*!*!*!*!*
END TRANSMISSION
*!*!*!*!*!*!*!*!*
```
## Flag

`SIVBGR{wh0_n33ds_32_b4s3s}`
