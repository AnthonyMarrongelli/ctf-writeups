def second_value(a):
    return a[1]

text = input('Enter Ciphertext: ').upper()
#'rbk dlcsqrpdzi pktmisrdml zlc drq amlqkosklakq bztk hkkl z cdqzqrkp ump rbk bsjzl pzak rbkx bztk fpkzrix dlapkzqkc rbk iduk kwnkarzlax mu rbmqk mu sq vbm idtk dl zctzlakc amslrpdkq hsr rbkx bztk ckqrzhdidykc qmadkrx bztk jzck iduk slusiudiidlf bztk qshekarkc bsjzl hkdlfq rm dlcdfldrdkq bztk ikc rm vdckqnpkzc nqxabmimfdazi qsuukpdlf dl rbk rbdpc vmpic rm nbxqdazi qsuukpdlf zq vkii zlc bztk dluidarkc qktkpk czjzfk ml rbk lzrspzi vmpic rbk amlrdlskc cktkimnjklr mu rkablmimfx vdii vmpqkl rbk qdrszrdml dr vdii akprzdlix qshekar bsjzl hkdlfq rm fpkzrkp dlcdfldrdkq zlc dluidar fpkzrkp czjzfk ml rbk lzrspzi vmpic dr vdii npmhzhix ikzc rm fpkzrkp qmadzi cdqpsnrdml zlc nqxabmimfdazi qsuukpdlf zlc dr jzx ikzc rm dlapkzqkc nbxqdazi qsuukpdlf ktkl dl zctzlakc amslrpdkq rbk dlcsqrpdzi rkablmimfdazi qxqrkj jzx qsptdtk mp dr jzx hpkzg cmvl du dr qsptdtkq dr jzx ktklrsziix zabdktk z imv iktki mu nbxqdazi zlc nqxabmimfdazi qsuukpdlf hsr mlix zurkp nzqqdlf rbpmsfb z imlf zlc tkpx nzdlusi nkpdmc mu zcesqrjklr zlc mlix zr rbk amqr mu nkpjzlklrix pkcsadlf bsjzl hkdlfq zlc jzlx mrbkp idtdlf mpfzldqjq rm klfdlkkpkc npmcsarq zlc jkpk amfq dl rbk qmadzi jzabdlk usprbkpjmpk du rbk qxqrkj qsptdtkq rbk amlqkosklakq vdii hk dlktdrzhik rbkpk dq lm vzx mu pkumpjdlf mp jmcduxdlf rbk qxqrkj qm zq rm npktklr dr upmj cknpdtdlf nkmnik mu cdfldrx zlc zsrmlmjx'.upper()
alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ_{}'
length = len(alphabet)
alphabet_count = [['',0]]*length
starts_with_count = [['',0]]*length

replacements = {}

def replaceFromDict(cipher, replacements):
    res = cipher
    for (rep, val) in replacements.items():
        res = res.replace(rep, val)
    
    return res


for i in range(length):
    alphabet_count[i] = [alphabet[i],0]
    starts_with_count[i] = [alphabet[i],0]


for i in text:
    for j in range(length):
        if i==alphabet[j]:
            alphabet_count[j][1]+=1
            break

sorted_alphabet = alphabet_count
cipher_length = len(text)
sorted_alphabet.sort(reverse=1,key=second_value)

#sorting them
for i in range(length):
    sorted_alphabet[i][1]=round(sorted_alphabet[i][1]/cipher_length*100,2)

x=''
print("Current Ciphertext:")
print(text)

while(x!='X'):
    x= input("\nPress A to display current alphabet, F to display frequencies, C to display current ciphertext, R to replace a letter, U to reset the alphabet, or X to exit: ").upper()
    if x=='A':
        print(alphabet)
        print(replaceFromDict(alphabet, replacements))
    elif x=='F':
        print(sorted_alphabet)
    elif x=='C':
        print(replaceFromDict(text, replacements))
    elif x=='R':
        old_letter = input("Old letter: ").upper()
        new_letter = input("New letter: ").lower()
        if len(old_letter) != len(new_letter):
            print("Length of old and new do not match!")
        else:
            for l in range(len(old_letter)):
                replacements[old_letter[l]] = new_letter[l]
            print("\nUpdated Ciphertext:")
            print(replaceFromDict(text, replacements))        
            print("\nUpdated Alphabet:")
            print(alphabet+" ->")
            print(replaceFromDict(alphabet, replacements))
    elif x=='U':
        replacements = {}
        print("Alphabet reset!")    
    elif x!='X':
        print("Erm what the deuce")