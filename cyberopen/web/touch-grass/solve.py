import requests
import time

url = "http://uscybercombine-touch-grass.chals.io/api/click"
headers = {
    "Cookie": "session=yAQcu4t3ZcREvZCCtpLjrfgc6p_ouzpNO_xqBzwmsaY",
    "Sec-Ch-Ua": "",
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '""',
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.5790.171 Safari/537.36",
    "Content-Type": "application/json",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-User": "?1",
    "Sec-Fetch-Dest": "document",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "close",
    "Content-Length": "29"
}
data = {
    "username": "anthony"
}

while True:
    response = requests.post(url, json=data, headers=headers)
    print(response.status_code, response.text)
    time.sleep(0.1)  # Sleep for 1 second to avoid sending requests too quickly