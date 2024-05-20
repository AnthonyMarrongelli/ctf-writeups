# Austen Supremacy

Lydia loves Jane Austen. In fact, her favorite book is Pride and Prejudice. Her and her friends like to talk about the book together, but recently Lydia has started encoding her messages. Unfortunately Lydia's friends don't understand her secret code -- could you help them out and identify the secret message?

Flag format - byuctf{secretmessage}

1.1.1 8.9.8 10.2.11 4.14.28 61.2.4 47.10.3 23.7.37 41.12.4 17.6.10 1.1.21

## Challenge

So other from the description we aren't given anything else. Off first thought I predicted the numbers to be in this format:
```
Chapter.Paragraph.Word/Letter
```
After trying to do it by word and it wasn't making sense I ended up going with letter. And after a few trials and errors I noticed the word `darcy` at the end of my plaintext and thats when I knew I had the right idea.

From there I went back and made sure my plaintext was correct and made sense and I got `ilovedarcy`.

I used this link: https://giove.isti.cnr.it/demo/eread/Libri/joy/Pride.pdf

## Flag

`byuctf{ilovedarcy}`