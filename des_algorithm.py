### DES Implmentation ###
# Author: Ayman Wael 
# ID: CU2500054
# Course: KH4015CMD Foundations of Computer Science
from permutations import *
from sboxes import *
from key_schedule import *


### Utiltiy Functions ###

def xor(bits1, bits2):
    return [b1 ^ b2 for b1, b2 in zip(bits1, bits2)]

def split_half(bit_array):
    mid = len(bit_array) // 2
    return bit_array[:mid], bit_array[mid:]

def bit_array_to_string(bit_array):
    result = []
    for i in range(0, len(bit_array), 8):
        byte = bit_array[i:i+8]
        value=0
        for bit in byte:
            value = (value << 1) | bit
        result.append(chr(value))
    return ''.join(result)

### Feistel Function ###
def feistel_function(right_half, round_key):
    expanded = apply_permutation(right_half, Expansion_Permutation)
    xored = xor(expanded, round_key)
    substituted = sbox_substitution(xored)
    permuted = apply_permutation(substituted, P_Box)
    return permuted

### Core DES ###
def des_block(block_bits, round_keys):
    permuted = apply_permutation(block_bits, Intial_Permutation)
    left, right = split_half(permuted)
    for round_num in range(16):
        old_left = left
        left = right
        f_output = feistel_function(right, round_keys[round_num])
        right = xor(old_left, f_output)
    combined = right + left

    final = apply_permutation(combined, Final_Permutation)
    return final

### Padding Functions ###
def add_padding(text):
  padding_length = 8 - (len(text) % 8)
  return text + chr(padding_length) * padding_length

def remove_padding(text):
  padding_length = ord(text[-1])
  return text[:-padding_length]

### DES Encryption/Decryption ###
def des_encrypt(plaintext, key):
    if len(key) != 8:
        raise ValueError("Key must be 8 characters (64 bits) long")
    
    needs_padding = (len(plaintext) % 8 != 0)
    if needs_padding:
        plaintext = add_padding(plaintext)

    round_keys = generate_round_keys(key)
    ciphertext_bits = []
    for i in range(0, len(plaintext), 8):
        block = plaintext[i:i+8]
        block_bits = string_to_bit_array(block)
        encrypted_bits = des_block(block_bits, round_keys)
        ciphertext_bits.extend(encrypted_bits)
    ciphertext= bit_array_to_string(ciphertext_bits)
    return ciphertext.encode('latin-1').hex().upper()

def des_decrypt(ciphertext_hex, key):
    if len(key) != 8:
        raise ValueError("Key must be 8 characters (64 bits) long")
    
    try:
        ciphertext_bytes= bytes.fromhex(ciphertext_hex)
        ciphertext = ciphertext_bytes.decode('latin-1')
    except:
        raise ValueError("Invalid ciphertext format. Must be a valid hex string.")

    round_keys = generate_decryption_keys(key)
    plaintext_bits = []
    for i in range(0, len(ciphertext), 8):
        block = ciphertext[i:i+8]
        block_bits = string_to_bit_array(block)
        decrypted_bits = des_block(block_bits, round_keys)
        plaintext_bits.extend(decrypted_bits)
    plaintext= bit_array_to_string(plaintext_bits)
    plaintext = remove_padding(plaintext)
    return plaintext

### User Interface ###
def get_valid_input(prompt, min_length=1, max_length= None):
    while True:
        user_input = input(prompt)
        if not user_input:
            print("Input cannot be empty. Please try again.")
            continue
        if max_length and len(user_input) > max_length:
            print(f"Input cannot exceed {max_length} characters. Please try again.")
            continue
        return user_input
if __name__=="__main__":
    print("Welcome to the DES Encryption/Decryption Tool")
    print("Enter 'quit' to exit\n")
    
    while True:
        print("\nChoose operation:")
        print("1. Encrypt")
        print("2. Decrypt")
        choice = input("Enter 1 or 2 (or 'quit'): ").strip().lower()

        if choice == 'quit':
            print("Goodbye!")
            break
        
        if choice not in ['1', '2']:
            print("Invalid choice. Enter 1, 2, or 'quit'.")
            continue

        while True:
            key = get_valid_input("Enter 8-character key: ")
            if len(key) == 8:
                break
            print("Key must be exactly 8 characters!")

        if choice == '1':
            prompt = "Enter message to encrypt: "
        else:
            prompt = "Enter ciphertext to decrypt: "
        
        text = get_valid_input(prompt)
        
        # Process
        try:
            if choice == '1':
                result = des_encrypt(text, key)
                print(f"\n Encrypted: '{result}'")
                print(f"   Hex: {result.encode('latin-1').hex().upper()}")
            else:
                result = des_decrypt(text, key)
                print(f"\n Decrypted: '{result}'")
                
        except ValueError as e:
            print(f"\n Error: {e}")
        except Exception as e:
            print(f"\n Unexpected error: {e}")