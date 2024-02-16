#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import statements
import random
import sys
from urllib.request import urlopen
from urllib.error import URLError

def lfsr(seed, taps):
    shift_register = seed
    while True:
        xor = 0
        for t in taps:
            xor ^= (shift_register >> (16-t)) & 1
        shift_register = (shift_register >> 1) | (xor << 15)
        shift_register &= 0xffff  # Since we want a 16-bit lfsr, this is needed.
        yield shift_register

def seed_generator():
    try:
        online_file = "https://www.mit.edu/~ecprice/wordlist.10000"
        wordlist = urlopen(online_file)

        wordlist_text = wordlist.read().decode('utf-8')  # On import, the text needs to be readable.
        dictionary = wordlist_text.splitlines()

        selected = random.choice(dictionary)
        seed = sum(ord(char) for char in selected) & 0xffff  # Further assurance that our lfsr works within the bounds of 16-bits as the seed word needs to be numerical and cannot be just sent in (throws errors).
        
        print(f"Generated using this word: {selected}\n")

        return seed
    
    except URLError as error:
        print(f"Failed to download word list: {error}")
        return None

if __name__ == "__main__":
    seed = seed_generator()
    taps = [16, 14, 13, 11]

    if seed is not None:
        lfsr_output = lfsr(seed, taps)
        for _ in range(10):  # Generate 10 lines of output
            print(format(next(lfsr_output), '016b'))
        print(f"\nGenerated using this seed: {seed}")
    else:
        print("Exiting, seed not generated.")
        sys.exit()