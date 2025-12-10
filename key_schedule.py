### DES key schedule ###

# Generates the 16 round keys from intial 64 bit key
# starts with 64 bit key as input then apply PC-1 permutation to get 56 bit key after removing parity
# then split into two 28 bit halves c and d then for each of the 16 rounds left shift c and d based on round number 
# then combine c and d then apply PC-2 permutatuion to get 48 bit round key
# this results in 16 round keys K1-K16 each 48 bits. and when we decrypt we use same keys but in reverse k16-->k1

from permutations import Permuted_Choice_1, Permuted_Choice_2, Shift_Schedule

def string_to_bit_array(text):
    # converts a string into a list of bits
    bit_array =[]
    for char in text:
        ascii_val = ord(char)
        for i in range (7, -1, -1):
            bit_array.append((ascii_val >> i) & 1)
    return bit_array


def apply_permutation(bit_array, permutation_table):
    # applies permutation to a bit array
    return [bit_array[position - 1] for position in permutation_table]


def left_shift(bit_array, shifts):
    # left shifts a bit array by the number of shifts
    return bit_array[shifts:] + bit_array[:shifts]

def generate_round_keys(key):
    # generate all 16 round keys from the intial 64 bit key
    if isinstance(key, str):
        if len(key) != 8:
            raise ValueError("Key must be 8 characters (64 bits) long")
        key_bits = string_to_bit_array(key)
    elif len (key) == 64:
        key_bits = key
    else:
        raise ValueError("Key must be 64 bits long")

    key_56 = apply_permutation(key_bits, Permuted_Choice_1)

    c = key_56[:28] # left half
    d = key_56[28:] # right half

    round_keys = []

    for round_num in range (16):
        shift_amount = Shift_Schedule[round_num]
        c= left_shift(c, shift_amount)
        d= left_shift(d, shift_amount)

        CD= c+d

        round_key = apply_permutation(CD, Permuted_Choice_2)
        round_keys.append(round_key)
    return round_keys


def generate_decryption_keys(key):
    encryption_keys = generate_round_keys(key)
    decryption_keys = encryption_keys[::-1]
    return decryption_keys