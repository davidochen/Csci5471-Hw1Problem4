# Csci5471-Hw1Problem4

#Description
A one-time pad used twice unlocks its secrecy, and we are given a list of candidate plaintext files to help decrypt a given ciphertext.

This algorithm uses a database of candidate plaintexts and uses statistical English bigram frequencies from ftable2.csv to score and identify the most likely English plaintext. The approach is XORs the two ciphertexts to remove the key, then uses each candidate database plaintext to get a potential English plaintext, scoring each to find the best fit.

The implementation reads two halves of the ciphertext from ciphertexts.bin, loads a set of candidate plaintext files from a known directory, and outputs the most probable database plaintext and corresponding English plaintext to separate files.

Must be in this directory:
- ciphertexts.bin
- ftable2.csv

Must have access to:
- /project/web-classes/Fall-2025/csci5471/hw1/db/

Output files:
- recovered_db_plaintext.txt
- recovered_english_plaintext.txt

Command Line Command:
python3 problem4.py
