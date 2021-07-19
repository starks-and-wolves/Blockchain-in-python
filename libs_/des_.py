"""
this .py file contains the code for encrypting and decrypting strings with DES algorithm.
"""

IP_Inverse = [40, 8, 48, 16, 56, 24, 64, 32,
              39, 7, 47, 15, 55, 23, 63, 31,
              38, 6, 46, 14, 54, 22, 62, 30,
              37, 5, 45, 13, 53, 21, 61, 29,
              36, 4, 44, 12, 52, 20, 60, 28,
              35, 3, 43, 11, 51, 19, 59, 27,
              34, 2, 42, 10, 50, 18, 58, 26,
              33, 1, 41, 9, 49, 17, 57, 25]

IP = [58, 50, 42, 34, 26, 18, 10, 2,
      60, 52, 44, 36, 28, 20, 12, 4,
      62, 54, 46, 38, 30, 22, 14, 6,
      64, 56, 48, 40, 32, 24, 16, 8,
      57, 49, 41, 33, 25, 17, 9, 1,
      59, 51, 43, 35, 27, 19, 11, 3,
      61, 53, 45, 37, 29, 21, 13, 5,
      63, 55, 47, 39, 31, 23, 15, 7]

S_Box = [[[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
          [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
          [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
          [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],

         [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
          [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
          [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
          [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],

         [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
          [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
          [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
          [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],

         [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
          [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
          [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
          [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],

         [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
          [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
          [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
          [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]],

         [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
          [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
          [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
          [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]],

         [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
          [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
          [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
          [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],

         [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
          [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
          [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
          [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]]

Exp_Table = [32, 1, 2, 3, 4, 5, 4, 5,
             6, 7, 8, 9, 8, 9, 10, 11,
             12, 13, 12, 13, 14, 15, 16, 17,
             16, 17, 18, 19, 20, 21, 20, 21,
             22, 23, 24, 25, 24, 25, 26, 27,
             28, 29, 28, 29, 30, 31, 32, 1]

P_Table = [16, 7, 20, 21,
           29, 12, 28, 17,
           1, 15, 23, 26,
           5, 18, 31, 10,
           2, 8, 24, 14,
           32, 27, 3, 9,
           19, 13, 30, 6,
           22, 11, 4, 25]

PC_1_Table = [57, 49, 41, 33, 25, 17, 9,
              1, 58, 50, 42, 34, 26, 18,
              10, 2, 59, 51, 43, 35, 27,
              19, 11, 3, 60, 52, 44, 36,
              63, 55, 47, 39, 31, 23, 15,
              7, 62, 54, 46, 38, 30, 22,
              14, 6, 61, 53, 45, 37, 29,
              21, 13, 5, 28, 20, 12, 4]

PC_2_Table = [14, 17, 11, 24, 1, 5,
              3, 28, 15, 6, 21, 10,
              23, 19, 12, 4, 26, 8,
              16, 7, 27, 20, 13, 2,
              41, 52, 31, 37, 47, 55,
              30, 40, 51, 45, 33, 48,
              44, 49, 39, 56, 34, 53,
              46, 42, 50, 36, 29, 32]

Shift_Table = [1, 1, 2, 2,
               2, 2, 2, 2,
               1, 2, 2, 2,
               2, 2, 2, 1]


# def hex_to_bin(text_hex):
#     text_bin = ""
#     for i in text_hex:
#         bi = bin(int(i, 16))[2:]
#         k = 4 - len(bi)
#         s = ""
#         for g in range(k):
#             s = s + "0"
#         bi = s + bi
#         text_bin = text_bin + bi
#     return text_bin
#
#
# def bin_to_hex(text_bin):
#     l = len(text_bin)
#     text_hex_ = ""
#     for i in range(4, l + 1, 4):
#         text_hex_ = text_hex_ + hex(int(text_bin[i - 4:i], 2))[2:]
#     return text_hex_
#
#
# def encrypt(plaintext, key="133457799BBCDFF1"):
#     ciphertext = plaintext
#     return ciphertext
#
#
# def decrypt(ciphertext_, key="133457799BBCDFF1"):
#     """
# 	ciphertext is bitstring of length 64
# 	key is also bitstring of length 64
# 	plaintext is also bit string of length 64
# 	"""
#     # ciphertext = hex_to_bin(ciphertext_)
#     # K = hex_to_bin(key)
#
#     plaintext = ciphertext_
#     return plaintext


def hex_to_bin(text_hex):
    text_bin = ""
    for i in text_hex:
        bi = bin(int(i, 16))[2:]
        k = 4 - len(bi)
        s = ""
        for g in range(k):
            s = s + "0"
        bi = s + bi
        text_bin = text_bin + bi
    return text_bin


def bin_to_hex(text_bin):
    l = len(text_bin)
    text_hex_ = ""
    for i in range(4, l + 1, 4):
        text_hex_ = text_hex_ + hex(int(text_bin[i - 4:i], 2))[2:]
    return text_hex_


def xor(x, y):
    b = bin(int(x, 2) ^ int(y, 2))[2:]
    return '0' * (len(y) - len(b)) + b


def shift_left(x, i):
    return x[i:] + x[0:i]


def create_subkeys(key, for_decryption=False):
    Kb = []  # Kb for RoundKeys in binary
    Kh = []  # Kh for RoundKeys in hexadecimal

    key = hex_to_bin(key)

    key = "".join(key[i - 1] for i in PC_1_Table)

    kleft = key[0:28]
    kright = key[28:56]

    for i in range(0, 16):
        kleft = shift_left(kleft, Shift_Table[i])
        kright = shift_left(kright, Shift_Table[i])

        combine_result = kleft + kright

        roundKey = "".join(combine_result[i - 1] for i in PC_2_Table)

        Kb.append(roundKey)
        Kh.append(bin_to_hex(roundKey))
    return (Kb, Kh) if not for_decryption else (Kb[::-1], Kh[::-1])


def encrypt1(plaintext, key):
    (Kb, Kh) = create_subkeys(key)

    plaintext = hex_to_bin(plaintext)
    plaintext = "".join(plaintext[i - 1] for i in IP)

    left_ = plaintext[0:32]
    right_ = plaintext[32:64]
    for i in range(0, 16):

        right_expansion = "".join(right_[pos - 1] for pos in Exp_Table)  # Expansion table 32 to 48 bits

        xor_result = xor(right_expansion, Kb[i])

        sbox_result = ""
        for j in range(0, 8):
            r = int(xor_result[j * 6] + xor_result[j * 6 + 5], 2)
            c = int(xor_result[j * 6 + 1] + xor_result[j * 6 + 2] + xor_result[j * 6 + 3] + xor_result[j * 6 + 4], 2)
            value = S_Box[j][r][c]
            sbox_result = sbox_result + ('0' * (4 - len(bin(value)[2:]))) + bin(value)[2:]

        sbox_result = "".join(sbox_result[pos - 1] for pos in P_Table)
        result = xor(left_, sbox_result)
        left_ = result

        if i != 15:
            left_, right_ = right_, left_

    combine = left_ + right_

    cipher_text = "".join(combine[pos - 1] for pos in IP_Inverse)
    return bin_to_hex(cipher_text)


def decrypt1(ciphertext, key):
    (Kb, Kh) = create_subkeys(key, for_decryption=True)

    ciphertext = hex_to_bin(ciphertext)

    ciphertext = "".join(ciphertext[i - 1] for i in IP)

    left_ = ciphertext[0:32]
    right_ = ciphertext[32:64]
    for i in range(0, 16):
        right_expansion = "".join(right_[pos - 1] for pos in Exp_Table)

        xor_result = xor(right_expansion, Kb[i])

        sbox_result = ""
        for j in range(0, 8):
            r = int(xor_result[j * 6] + xor_result[j * 6 + 5], 2)
            c = int(xor_result[j * 6 + 1] + xor_result[j * 6 + 2] + xor_result[j * 6 + 3] + xor_result[j * 6 + 4], 2)

            value = S_Box[j][r][c]
            sbox_result = sbox_result + ('0' * (4 - len(bin(value)[2:]))) + bin(value)[2:]

        sbox_result = "".join(sbox_result[pos - 1] for pos in P_Table)

        result = xor(left_, sbox_result)
        left_ = result

        if i != 15:
            left_, right_ = right_, left_

    combine = left_ + right_

    plain_text = "".join(combine[pos - 1] for pos in IP_Inverse)
    return bin_to_hex(plain_text)


def encrypt(plaintext, key="133457799bbcdff1", plaintext_is_hex=True, key_is_hex=True):
    if not plaintext_is_hex:
        plaintext = str(plaintext)
        plaintext = ''.join(hex(ord(i))[2:] for i in plaintext)

    if not key_is_hex:
        key = "".join(hex(ord(i))[2:] for i in key[:8])

    while len(plaintext) % 16 != 0:
        plaintext += hex(ord('$'))[2:]

    ciphertext = "".join(encrypt1(plaintext[i - 16:i], key) for i in range(16, len(plaintext) + 1, 16))
    return ciphertext


def decrypt(ciphertext, key="133457799bbcdff1", return_hex=True, key_is_hex=True):
    if not key_is_hex:
        key = "".join(hex(ord(i))[2:] for i in key[:8])

    plaintext = "".join(decrypt1(ciphertext[i - 16:i], key) for i in range(16, len(ciphertext) + 1, 16))
    if return_hex:
        return plaintext
    else:
        text = "".join(chr(int(plaintext[i - 2:i], 16)) if plaintext[i - 2:i] != '24' else "" for i in
                       range(2, len(plaintext) + 1, 2))
        return text
