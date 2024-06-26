# You Have Mail

This challenge is composed of an email, more specifically a .eml file. The email introduces the theme for the forensics group, which is a whistleblower announcing that alien life exists on Earth, and the government knows about it.

## Challenge

We're given this file `URGENT_Proof_of_UFO_Read_in_a_secure_location.eml`:
```
MIME-Version: 1.0
Date: Tue, 7 May 2024 22:12:36 -0500
Message-ID: <CAL1VkQ5JtBMJGOg+yuq6m51ETGDMj5nOHZswruxkD=yVRR9thQ@mail.gmail.com>
Subject: URGENT: Proof of UFO!!! Read in a secure location
From: Edward Silverfish <e.silverfish@uscg_ctf1.org>
To: media@uscgnews11.com
Content-Type: multipart/mixed; boundary="000000000000cd98100617e8acef"

--000000000000cd98100617e8acef
Content-Type: text/plain; charset="UTF-8"

Hello USGC News Channel media member,

My name is Dr. Edward Silverfish, and I am contacting you today to
provide you with information into what will be the next major news
story that will rock the headlines. I have evidence that the
government is actively hiding verifiable proof that alien life exists.
The government has a series of ongoing projects with the goal of
concealing this information from the public. I work within a lab in
Area 007, and I have seen with my own eyes what can only be described
as intelligent life that is not from this planet. I have worked on
unknown technology that can do things we have never seen before.
Things like Gen-AI that draws hands properly, bug spray that actually
stops all the bugs, and comms that deliver whale sounds straight from
the ocean to your bedroom! Just incredible stuff that our scientists
have never been able to replicate. This technology might be used to
develop breakthroughs, it if is just released to the public.

With your help, we can let the public know what is actually going on,
what type of life exists beyond Earth, and how to master Gen-AI art
once and for all.

Please see the attachment for my first piece of evidence. I am not
very good at understanding encryption details, but I did password
protect the file. The password is 53 65 63 75 72 65 5f 43 6f 64 65 3a
4f 72 64 65 72 5f 36 36.

Utilize a common number system to decrypt that password.

--000000000000cd98100617e8acef
Content-Type: application/zip; name="evidence.zip"
Content-Disposition: attachment; filename="evidence.zip"
Content-Transfer-Encoding: base64
X-Attachment-Id: f_lvx8qxe70
Content-ID: <f_lvx8qxe70>

UEsDBAoACQAAADewp1gfngtKRAAAADgAAAAMABwAZXZpZGVuY2UudHh0VVQJAAMZ6zpm6Oo6ZnV4
CwABBOgDAAAEAAAAADeIlKHufvfLJvJ/Ed32cRwF755eiG+bw1NAIL3UPKn+4WIMkSPXJInVFxLM
CrGuacbTdG6AcqrqzDiXWVhqKv6WuHlKUEsHCB+eC0pEAAAAOAAAAFBLAQIeAwoACQAAADewp1gf
ngtKRAAAADgAAAAMABgAAAAAAAEAAACkgQAAAABldmlkZW5jZS50eHRVVAUAAxnrOmZ1eAsAAQTo
AwAABAAAAABQSwUGAAAAAAEAAQBSAAAAmgAAAAAA
--000000000000cd98100617e8acef--
```

Just reading through it we notice two important things:
```
The password is 53 65 63 75 72 65 5f 43 6f 64 65 3a
4f 72 64 65 72 5f 36 36.
```
and
```
--000000000000cd98100617e8acef
Content-Type: application/zip; name="evidence.zip"
Content-Disposition: attachment; filename="evidence.zip"
Content-Transfer-Encoding: base64
X-Attachment-Id: f_lvx8qxe70
Content-ID: <f_lvx8qxe70>

UEsDBAoACQAAADewp1gfngtKRAAAADgAAAAMABwAZXZpZGVuY2UudHh0VVQJAAMZ6zpm6Oo6ZnV4
CwABBOgDAAAEAAAAADeIlKHufvfLJvJ/Ed32cRwF755eiG+bw1NAIL3UPKn+4WIMkSPXJInVFxLM
CrGuacbTdG6AcqrqzDiXWVhqKv6WuHlKUEsHCB+eC0pEAAAAOAAAAFBLAQIeAwoACQAAADewp1gf
ngtKRAAAADgAAAAMABgAAAAAAAEAAACkgQAAAABldmlkZW5jZS50eHRVVAUAAxnrOmZ1eAsAAQTo
AwAABAAAAABQSwUGAAAAAAEAAQBSAAAAmgAAAAAA
--000000000000cd98100617e8acef--
```

First thing we can do here is convert the password from what looks to be hex. Doing that we get this: `Secure_Code:Order_66`.

Then we can extract this `evidence.zip` which has the flag `Content-Transfer-Encoding: base64`.

```
└─$ echo "UEsDBAoACQAAADewp1gfngtKRAAAADgAAAAMABwAZXZpZGVuY2UudHh0VVQJAAMZ6zpm6Oo6ZnV4
CwABBOgDAAAEAAAAADeIlKHufvfLJvJ/Ed32cRwF755eiG+bw1NAIL3UPKn+4WIMkSPXJInVFxLM
CrGuacbTdG6AcqrqzDiXWVhqKv6WuHlKUEsHCB+eC0pEAAAAOAAAAFBLAQIeAwoACQAAADewp1gf
ngtKRAAAADgAAAAMABgAAAAAAAEAAACkgQAAAABldmlkZW5jZS50eHRVVAUAAxnrOmZ1eAsAAQTo
AwAABAAAAABQSwUGAAAAAAEAAQBSAAAAmgAAAAAA" | base64 -d > file.zip
```

When unzipping we are prompted for a password (which we already recovered):
```
└─$ unzip file.zip                  
Archive:  file.zip
[file.zip] evidence.txt password: 
 extracting: evidence.txt 
```

And inside that text file:
```
└─$ cat evidence.txt 
You found the evidence! 

 SIVBGR{th3_ev1d3nc3_1s_h3r3}
```


## Flag

`SIVBGR{th3_ev1d3nc3_1s_h3r3}`
