import re
import base64

with open('udp-stream', 'r') as file:
    contents = file.readline()

pattern = r'\.\d+\.meowcorp\.cloud'
contents = re.sub(pattern, '', contents)
base32_blob = contents.replace('.*.meowcorp.cloud', '').replace(',', '').replace('.', '')

print(base64.b32decode(base32_blob).decode())