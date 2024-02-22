#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import statements
import random
import sys
import os
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
        seed = int.from_bytes(os.urandom(2), 'big')  # Generates a 16-bit seed from system entropy

        return seed
    
    except URLError as error:
        print(f"Failed to download word list: {error}")
        return None

if __name__ == "__main__":
    seed = seed_generator()
    taps = [16, 14, 13, 11]

    if seed is not None:
        lfsr_output = lfsr(seed, taps)
        for _ in range(8):  # Generate 8 lines of output
            print(format(next(lfsr_output), '016b'))
        print(f"\nGenerated using this seed: {seed}")
    else:
        print("Exiting, seed not generated.")
        sys.exit()