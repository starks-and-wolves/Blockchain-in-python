"""
13-4-2021
implementation of RSA algorithm.
written by S Sai Dharma Srinidhi
"""


def pos_of_elem_just_less_than_b(exponents_of_2, b):
    for pos in range(len(exponents_of_2) - 1, -1, -1):
        if exponents_of_2[pos] <= b:
            return pos, int(b / exponents_of_2[pos])
    raise Exception("error")


def split_b(exponents_of_2, b):
    b_split = [[], []]
    while b > 0:
        pos, count = pos_of_elem_just_less_than_b(exponents_of_2, b)
        b_split[0].append(pos)
        b_split[1].append(count)

        b = b - exponents_of_2[pos] * count

    return b_split


def mod_(a, b, c):
    exponents_of_2 = [1, 2]
    mod_c = []
    mod_c.append(a % c)
    mod_c.append((mod_c[-1] * mod_c[-1]) % c)
    while exponents_of_2[-1] * 2 <= b:
        exponents_of_2.append(exponents_of_2[-1] * 2)
        mod_c.append((mod_c[-1] * mod_c[-1]) % c)

        exponents_of_2.append(exponents_of_2[-1] * 2)
        mod_c.append((mod_c[-1] * mod_c[-1]) % c)

    # print(exponents_of_2)
    b_split = split_b(exponents_of_2, b)

    # print(mod_c)
    # print(b_split)
    soln = 1
    for i in range(0, len(b_split[0])):
        if b_split[1][i] != 1:
            soln = (soln * mod_(mod_c[b_split[0][i]], b_split[1][i], c)) % c
        else:
            soln = (soln * mod_c[b_split[0][i]]) % c
    return soln


def rsa_encrypt(a, b, c):
    # """
    # a = '12a3 e4ac def2 3434'
    # """
    # encrypted = ""
    # for i in a:
    #     x = hex(mod_(int(i, 16), b, c))[2:]
    #     encrypted += '0'*(2-len(x)) + x
    # return encrypted
    encr = hex(mod_(int(a, 16), b, c))[2:]
    return encr


def rsa_decrypt(a, b, c):
    # decrypted = ""
    # for i in range(2, len(a)+1, 2):
    #     x = hex(mod_(int(a[i-2:i], 16), b, c))[2:]
    #     decrypted += '0'*(1-len(x)) + x
    # return decrypted

    decr = hex(mod_(int(a, 16), b, c))[2:]
    decr = '0'*(64-len(decr)) + decr

    return decr

