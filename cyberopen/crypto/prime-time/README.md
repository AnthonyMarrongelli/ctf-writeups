# Prime Time

N/A

## Challenge

We are given a `challenge.txt`:
```
Your encrypted flag: 67901295092999403377812474031753022640207373798290839976120254385637043193411358791915464230611073615341268787302565972547452757697916207952702288626173819641234095639259743277146365018265212857092237457393449677065307951821155969047439248276581778411840300731922481525641974287306159852931109413442675622573
Public Key:
n: 98813858186636016061828413291587334532178109240417756890955763078740391019450718373743031325554048662069578591495075978203742992839688516726192682096525494907367614705518833413598767554267177141399324414271413882430512533175133684772034149758259287505147508079731874384109521277000217376431320424120947279649
e: 65537
```

So just another standard RSA challenge. First things first as always, throw the key into [RsaCtfTool](https://github.com/RsaCtfTool/RsaCtfTool) and see if it cracks it.

```
└─$ RsaCtfTool -n 98813858186636016061828413291587334532178109240417756890955763078740391019450718373743031325554048662069578591495075978203742992839688516726192682096525494907367614705518833413598767554267177141399324414271413882430512533175133684772034149758259287505147508079731874384109521277000217376431320424120947279649 -e 65537 --private --dumpkey
['/tmp/tmp6e1oizbw']

[*] Testing key /tmp/tmp6e1oizbw.
attack initialized...
attack initialized...
[*] Performing factordb attack on /tmp/tmp6e1oizbw.
[*] Attack success with factordb method !

Results for /tmp/tmp6e1oizbw:

Private key :
-----BEGIN RSA PRIVATE KEY-----
MIICWwIBAAKBgQCMtzHijD1Om6YYrOLNLPbjZtpkoSvoBrsuDSiDPSmLcP3kSOJ6
dv4ARbrKQ5r+hBhUfvq9U3oF/xIb0NrxolJHowYx9lDEt7DijUns1EN0aN01GjjD
siSMUguGo+na+23+YgEWASEPlyMp/v/JEAGxD85zfaA7ek51d2Au1+OHIQIDAQAB
AoGAVeQgc/tMFKZXTSqCSeDPVmDan5/tT/SD3okzmGAF8tJmdyix7TSiuAHYEUwQ
2JhCzZiwbk385poaMJZcfi+pbp3NiW/UnVlYHlJWRQlrPgx6q8woSEe7FwF3ljA/
XCEfafMth0jei7H/xdBTA9gmt3EzaF23gNc4m1iaFLAFU80CQQCrybx5nby530J4
YWFQWYkIFwXLxSnSPvvMIKwouZ7TryNcK3UTyA33VVUlwzis/6zAXJkBUKBQ5HZU
nVWfpas/AkEA0bIS/V/I/QxEKZZ86eAhr6ZozqcTdYCZ20BO9b37YFBV25g3Qxoy
pcCplK+esexU2u+gQWxk23IiGFPB5I4VnwJAYAS/Yx6meSHwDkcn1HhnHm134OCQ
MqLfrMXqVE0EGH/A/OiRZQAhxkgc8qF+kTvLPC3Fm7WMFgrMlRjn3fcEkwJAJPcw
U8wr4TflWDN4J75kEdPTDAL18jPOa5Elmjp4ct0WlZR6wXB/1ypkepqO7iyMNOAj
LwVNrkWrbwBs4L6PXwJALsQQw3eCvgAnJ/bDzVk6KHhUqdawJMuG8wMXU8cMdWU3
i0hnoRtc+AIBYo0D7HQVrvhzFzQp/xWGQgzMDVKVlA==
-----END RSA PRIVATE KEY-----

Private key details:
n: 98813858186636016061828413291587334532178109240417756890955763078740391019450718373743031325554048662069578591495075978203742992839688516726192682096525494907367614705518833413598767554267177141399324414271413882430512533175133684772034149758259287505147508079731874384109521277000217376431320424120947279649
e: 65537
d: 60314795749576583464627950881233015598680453849648771364403365891616214687139891772660367153152243902356979300175130450830589299824008723844513570378676298480594496636317099777285383497240568035910455508230818305121082655515124487369107805340663425383618272955753040389852233989883859613176439629282548208589
p: 8997269295884843284681982750060377872478356391734956728242353212469576051387114547220167685859751845030095832125183195971175109609583065893432498097335103
q: 10982649839305281359093240091231892576733401067753111072429500083504978610994787471724765658823614458122443035638808449338442889570184467486237572144698783
```

And what do you know, we got the private key.

Decryption script:
```python
from Crypto.Util.number import *

c = 67901295092999403377812474031753022640207373798290839976120254385637043193411358791915464230611073615341268787302565972547452757697916207952702288626173819641234095639259743277146365018265212857092237457393449677065307951821155969047439248276581778411840300731922481525641974287306159852931109413442675622573
p = 8997269295884843284681982750060377872478356391734956728242353212469576051387114547220167685859751845030095832125183195971175109609583065893432498097335103
q = 10982649839305281359093240091231892576733401067753111072429500083504978610994787471724765658823614458122443035638808449338442889570184467486237572144698783
n = p*q
e = 65537
phi = (p-1)*(q-1)
d = inverse(e, phi)
print(long_to_bytes(pow(c, d, n)))
```

## Flag

`SIVBGR{h1dd3n_f4c70r5}`