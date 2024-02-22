# selamat-pagi

## Overview:

Category: Cryptography

## Description

If you talk in another language, nobody can understand what you say! Check out this message I sent in Indonesian. To add some extra security, I also applied a monoalphabetic substitution cipher on it!

## What We Have:

```message.txt```
```c
Efe kqkbkx czwkf akfs kdkf qzfskf wzdcjtfk Ieqku kqk akfs ikxj kck akfs wkak ukikukf :Q Lzfqztk ukdj kqk qe wefe: bkvim{wzbkdki_ckse_kckukx_ukdj_wjuk_kfkbewew_mtzujzfwe}
```

## Approach

First thing that comes to mind with a monoalphabetic substitution cipher is frequency analysis.

Lets open up a handy frequency analysis tool like [this one](joshcrates.py).

## Attack

So we can guess the flag format is going to be lactf{}.

Therefore we can already start off by making these mappings:
```text
b -> l
k -> a
v -> c
i -> t
m -> f
```

After doing so we get this:
```c
Updated Ciphertext:
EFE aQalaX CZWaF AaFS aDaF QZFSaF WZDCJTFa tEQaU aQa AaFS taXJ aCa AaFS WaAa UataUaF :Q LZFQZTa UaDJ aQa QE WEFE: lactf{WZlaDat_CaSE_aCaUaX_UaDJ_WJUa_aFalEWEW_fTZUJZFWE}

Updated Alphabet:
ABCDEFGHIJKLMNOPQRSTUVWXYZ_{} ->
AlCDEFGHtJaLfNOPQRSTUcWXYZ_{}
```

So now you could either choose to see if you can guess what some of the words will be, or begin to analyze the frequencies of letters and plug and play.

Out of intuition during the competition, I noticed this string inside the flag `aFalEWEW_fTZUJZFWE`.

In this string, `a_al____` is a part of our plaintext. 

First thing I thought of was "analysis". Knowing our plaintext was in Indonesian, I translated frequency anaylsis to indonesian to get:  `analisis frekuensi`.

After seeing that, I thought, let's try these mappings out.

```c
Updated Ciphertext:
ini aQalaX Cesan AanS aDan QenSan seDCurna tiQak aQa AanS taXu aCa AanS saAa katakan :Q LenQera kaDu aQa Qi sini: lactf{selaDat_CaSi_aCakaX_kaDu_suka_analisis_frekuensi}

Updated Alphabet:
ABCDEFGHIJKLMNOPQRSTUVWXYZ_{} ->
AlCDinGHtuaLfNOPQRSrkcsXYe_{}
```

So now this is where we are sitting at. 

Looking at the flag again, I noticed that `selaDat_CaSi` looks awfully close to the challenge title `selamat pagi`. 

So let's try that out as well.

```c
Updated Ciphertext:
ini aQalaX pesan Aang aman Qengan sempurna tiQak aQa Aang taXu apa Aang saAa katakan :Q LenQera kamu aQa Qi sini: lactf{selamat_pagi_apakaX_kamu_suka_analisis_frekuensi}

Updated Alphabet:
ABCDEFGHIJKLMNOPQRSTUVWXYZ_{} ->
AlpminGHtuaLfNOPQRgrkcsXYe_{}
```

Now that leaves us with a singular letter to determine what it is.

A simple google search `indonesian apaka...` lead me to the word `apakah`.

Plugging that in we got:

```c
Updated Ciphertext:
ini aQalah pesan Aang aman Qengan sempurna tiQak aQa Aang tahu apa Aang saAa katakan :Q LenQera kamu aQa Qi sini: lactf{selamat_pagi_apakah_kamu_suka_analisis_frekuensi}

Updated Alphabet:
ABCDEFGHIJKLMNOPQRSTUVWXYZ_{} ->
AlpminGHtuaLfNOPQRgrkcshYe_{}
```

I submitted the flag in Indonesian and it was accepted. I am unsure if the english translated version was accepted.

You can continue to decipher the rest of the message even though you have the flag. Doing so, gave me the entire plaintext which I converted to English:

```c
this is a perfectly safe message no one is afraid of what I say :d your flag is here: lactf{good_morning_what_you_like_frequency_analysis}
```

## Flag

lactf{selamat_pagi_apakah_kamu_suka_analisis_frekuensi}
