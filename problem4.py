"""
problem4.py

Author: chen7790@umn.edu
Date: 09-23-2025

This script recovers two plaintexts encrypted with a reused one-time padby using scoring from ftable2.csv to identify best English plaintext
"""

import numpy as np
import csv
import os

# XOR two byte sequence, needs to be equal length
def xor_bytes(c1, c2):
  return bytes([b1 ^ b2 for b1, b2 in zip(c1, c2)])

# load bigram table
def load_bigrams(filename):
  bigrams = {}
  with open(filename, newline='') as csvfile:
      reader = csv.reader(csvfile)
      rows = list(reader)
      
  header = rows[0][1:]  # skip first row because it displays the character
  for row in rows[1:]:
      first_char = row[0]
      for i, freq_str in enumerate(row[1:]):
          second_char = header[i]
          freq = float(freq_str) if freq_str else 0.0
          bigrams[(first_char, second_char)] = freq
          
  # Find smallest positive frequency
  min_freq = min(v for v in bigrams.values() if v > 0)
  
  # Convert frequencies to log probabilities
  for k in bigrams:
      freq = bigrams[k]
      bigrams[k] = np.log(max(freq, min_freq / 100))
  return bigrams

# Scores a byte sequence for english letters using the probabilities from the bigram
# Scores for letters, penalties for unknown characters
def score_english(candidate, bigrams):
  def byte_to_char(b):
      if b == 32:       # ASCII space
          return ' '
      if 65 <= b <= 90: # uppercase letters
          return chr(b)
      if 97 <= b <= 122: # lowercase letters converted to uppercase
          return chr(b - 32)
      return None
    
  score = 0
  for i in range(len(candidate) - 1):
      a = byte_to_char(candidate[i])
      b = byte_to_char(candidate[i + 1])
      if a is None or b is None:
          score += -10  # penalty for invalid characters
      else:
          score += bigrams.get((a, b), -10)  # penalty if bigram not found
  return score

# Recover plaintexts by XORing to cancel out the key, return the best scoring English plaintext
def recover_plaintext(c1_bytes, c2_bytes, db_files, bigram_file):
  xor_result = xor_bytes(c1_bytes, c2_bytes)
  bigrams = load_bigrams(bigram_file)
  best_score = -float('inf')
  best_db_file = None
  best_english = None
  
  # Try each candidate DB file as possible
  for db_file in db_files:
      with open(db_file, 'rb') as f:
          db_bytes = f.read()
          # Skip files not matching ciphertext length
          if len(db_bytes) != len(xor_result):
              continue
            
          # Compute candidate English plaintext2
          candidate_english = xor_bytes(db_bytes, xor_result)
          score = score_english(candidate_english, bigrams)
          if score > best_score:
              best_score = score
              best_db_file = db_file
              best_english = candidate_english
              
  # Return best db plaintext
  with open(best_db_file, 'rb') as f:
      db_plaintext = f.read()
  return db_plaintext, best_english


if __name__ == "__main__":
  # Split ciphertext file into two halves
  with open('ciphertexts.bin', 'rb') as f:
      data = f.read()
  assert len(data) == 2048, "Ciphertext file length mismatch"
  with open('file1.bin', 'wb') as f1:
      f1.write(data[:1024])  # first half
  with open('file2.bin', 'wb') as f2:
      f2.write(data[1024:]) # second half
      
  # Load ciphertext halves as bytes
  c1_bytes = open('file1.bin', 'rb').read()
  c2_bytes = open('file2.bin', 'rb').read()
  
  # List candidate plaintext files from database directory
  db_dir = '/project/web-classes/Fall-2025/csci5471/hw1/db/'
  db_files = [os.path.join(db_dir, f) for f in os.listdir(db_dir) if f.endswith('.txt')]
  
  bigram_file = 'ftable2.csv'
  db_plaintext, english_plaintext = recover_plaintext(c1_bytes, c2_bytes, db_files, bigram_file)
  
  with open('recovered_db_plaintext.txt', 'wb') as f:
      f.write(db_plaintext)
  with open('recovered_english_plaintext.txt', 'wb') as f:
      f.write(english_plaintext)
      
  print("Recovered plaintexts saved to 'recovered_db_plaintext.txt' and 'recovered_english_plaintext.txt'")
  print("\nEnglish plaintext preview:\n", english_plaintext.decode('latin1', errors='ignore')[:500])
  