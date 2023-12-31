import random
from copy import copy
from PIL import Image
import secrets

s_box = [
    0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
    0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
    0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
    0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
    0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
    0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
    0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
    0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
    0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
    0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
    0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
    0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
    0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
    0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
    0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
    0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16
]

s_box_inv = [
    0x52, 0x09, 0x6a, 0xd5, 0x30, 0x36, 0xa5, 0x38, 0xbf, 0x40, 0xa3, 0x9e, 0x81, 0xf3, 0xd7, 0xfb,
    0x7c, 0xe3, 0x39, 0x82, 0x9b, 0x2f, 0xff, 0x87, 0x34, 0x8e, 0x43, 0x44, 0xc4, 0xde, 0xe9, 0xcb,
    0x54, 0x7b, 0x94, 0x32, 0xa6, 0xc2, 0x23, 0x3d, 0xee, 0x4c, 0x95, 0x0b, 0x42, 0xfa, 0xc3, 0x4e,
    0x08, 0x2e, 0xa1, 0x66, 0x28, 0xd9, 0x24, 0xb2, 0x76, 0x5b, 0xa2, 0x49, 0x6d, 0x8b, 0xd1, 0x25,
    0x72, 0xf8, 0xf6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xd4, 0xa4, 0x5c, 0xcc, 0x5d, 0x65, 0xb6, 0x92,
    0x6c, 0x70, 0x48, 0x50, 0xfd, 0xed, 0xb9, 0xda, 0x5e, 0x15, 0x46, 0x57, 0xa7, 0x8d, 0x9d, 0x84,
    0x90, 0xd8, 0xab, 0x00, 0x8c, 0xbc, 0xd3, 0x0a, 0xf7, 0xe4, 0x58, 0x05, 0xb8, 0xb3, 0x45, 0x06,
    0xd0, 0x2c, 0x1e, 0x8f, 0xca, 0x3f, 0x0f, 0x02, 0xc1, 0xaf, 0xbd, 0x03, 0x01, 0x13, 0x8a, 0x6b,
    0x3a, 0x91, 0x11, 0x41, 0x4f, 0x67, 0xdc, 0xea, 0x97, 0xf2, 0xcf, 0xce, 0xf0, 0xb4, 0xe6, 0x73,
    0x96, 0xac, 0x74, 0x22, 0xe7, 0xad, 0x35, 0x85, 0xe2, 0xf9, 0x37, 0xe8, 0x1c, 0x75, 0xdf, 0x6e,
    0x47, 0xf1, 0x1a, 0x71, 0x1d, 0x29, 0xc5, 0x89, 0x6f, 0xb7, 0x62, 0x0e, 0xaa, 0x18, 0xbe, 0x1b,
    0xfc, 0x56, 0x3e, 0x4b, 0xc6, 0xd2, 0x79, 0x20, 0x9a, 0xdb, 0xc0, 0xfe, 0x78, 0xcd, 0x5a, 0xf4,
    0x1f, 0xdd, 0xa8, 0x33, 0x88, 0x07, 0xc7, 0x31, 0xb1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xec, 0x5f,
    0x60, 0x51, 0x7f, 0xa9, 0x19, 0xb5, 0x4a, 0x0d, 0x2d, 0xe5, 0x7a, 0x9f, 0x93, 0xc9, 0x9c, 0xef,
    0xa0, 0xe0, 0x3b, 0x4d, 0xae, 0x2a, 0xf5, 0xb0, 0xc8, 0xeb, 0xbb, 0x3c, 0x83, 0x53, 0x99, 0x61,
    0x17, 0x2b, 0x04, 0x7e, 0xba, 0x77, 0xd6, 0x26, 0xe1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0c, 0x7d
]

r_con = [0x00000000, 0x01000000, 0x02000000, 0x04000000, 0x08000000, 0x10000000,
         0x20000000, 0x40000000, 0x80000000, 0x1b000000, 0x36000000]


def sub_bytes(state):
    # substitui os bytes do estado de acordo com a tabela s-box
    for i in range(len(state)):
        state[i] = s_box[state[i]]
    return state


def sub_bytes_inv(state):
    # substitui os bytes do estado de acordo com a invertida de s-box
    for i in range(len(state)):
        state[i] = s_box_inv[state[i]]
    return state


def rotate(word, n):
    return word[n:] + word[:n]


def shift_row(state):
    # faz um shift circular para cada linha
    # linha 1 - nao movimenta
    # linha 2 - move 1 esp
    # linha 3 - move 2 esp
    # linha 4 - move 3 esp
    for i in range(4):
        state[i * 4:i * 4 + 4] = rotate(state[i * 4:i * 4 + 4], i)
    return state


def shift_row_inv(state):
    for i in range(4):
        state[i * 4:i * 4 + 4] = rotate(state[i * 4:i * 4 + 4], -i)
    return state


def galois_mult(a, b):
    p = 0
    hiBitSet = 0
    for i in range(8):
        if b & 1 == 1:
            p ^= a
        hiBitSet = a & 0x80
        a <<= 1
        if hiBitSet == 0x80:
            a ^= 0x1b
        b >>= 1
    return p % 256


def mix_columns(state):
    temp = copy(state)
    for i in range(0, 16, 4):
        state[i + 0] = galois_mult(temp[i + 0], 2) ^ galois_mult(temp[i + 3], 1) ^ galois_mult(temp[i + 2],
                                                                                               1) ^ galois_mult(
            temp[i + 1], 3)
        state[i + 1] = galois_mult(temp[i + 1], 2) ^ galois_mult(temp[i + 0], 1) ^ galois_mult(temp[i + 3],
                                                                                               1) ^ galois_mult(
            temp[i + 2], 3)
        state[i + 2] = galois_mult(temp[i + 2], 2) ^ galois_mult(temp[i + 1], 1) ^ galois_mult(temp[i + 0],
                                                                                               1) ^ galois_mult(
            temp[i + 3], 3)
        state[i + 3] = galois_mult(temp[i + 3], 2) ^ galois_mult(temp[i + 2], 1) ^ galois_mult(temp[i + 1],
                                                                                               1) ^ galois_mult(
            temp[i + 0], 3)
    return state


def mix_columns_inv(state):
    temp = copy(state)
    for i in range(0, 16, 4):
        state[i + 0] = galois_mult(temp[i + 0], 14) ^ galois_mult(temp[i + 3], 9) ^ galois_mult(temp[i + 2],
                                                                                                13) ^ galois_mult(
            temp[i + 1], 11)
        state[i + 1] = galois_mult(temp[i + 1], 14) ^ galois_mult(temp[i + 0], 9) ^ galois_mult(temp[i + 3],
                                                                                                13) ^ galois_mult(
            temp[i + 2], 11)
        state[i + 2] = galois_mult(temp[i + 2], 14) ^ galois_mult(temp[i + 1], 9) ^ galois_mult(temp[i + 0],
                                                                                                13) ^ galois_mult(
            temp[i + 3], 11)
        state[i + 3] = galois_mult(temp[i + 3], 14) ^ galois_mult(temp[i + 2], 9) ^ galois_mult(temp[i + 1],
                                                                                                13) ^ galois_mult(
            temp[i + 0], 11)
    return state


def dec2hex(list):
    hex_val = ''
    if isinstance(list, str):
        return list
    for x in list:
        temp = hex(x)[2:]
        if len(temp) == 1:
            temp = '0' + temp
        hex_val += temp
    return hex_val


def hex2dec(hex):
    return int(str(hex), 16)


def hexor(hex1, hex2):
    dec1 = hex2dec(hex1)
    dec2 = hex2dec(hex2)

    xord = dec1 ^ dec2
    hexed = hex(xord)[2:]

    if len(hexed) != 8:
        hexed = '0' + hexed

    return hexed


def key_expansion(key):
    w = [[]] * 44

    for i in range(4):
        w[i] = [key[4 * i], key[4 * i + 1], key[4 * i + 2], key[4 * i + 3]]

    for i in range(4, 44):
        temp = w[i - 1]
        word = w[i - 4]

        if i % 4 == 0:
            x = rotate(temp, 1)
            y = sub_bytes(x)  # vai conter uma lista de inteiros
            rcon = r_con[int(i / 4)]

            temp = hexor(dec2hex(y), hex(rcon)[2:])

        xord = hexor(dec2hex(word), dec2hex(temp))

        w[i] = [hex2dec(xord[:2]),
                hex2dec(xord[2:4]),
                hex2dec(xord[4:6]),
                hex2dec(xord[6:8])]

    exp_key = []
    for list in w:
        for val in list:
            exp_key.append(val)

    return exp_key  # retorna uma lista de inteiros


def add_round_key(key, state):
    for i in range(len(state)):
        state[i] = state[i] ^ key[i]
    return state


def generate_key():
    key_list = []

    bytes_key = bytearray(random.getrandbits(8) for _ in range(16))

    hex_key = ''.join('{:02x}'.format(byte) for byte in bytes_key)

    for i in range(0, len(hex_key), 2):
        temp = hex2dec(hex_key[i:i + 2])
        key_list.append(temp)

    return key_list


def aes_encrypt(block, key, n_round):
    exp_key = key_expansion(key)

    block = add_round_key(exp_key[:16], block)
    del exp_key[:16]

    for i in range(n_round - 1):
        state = sub_bytes(block)
        state = shift_row(state)
        state = mix_columns(state)
        state = add_round_key(exp_key[:16], state)
        del exp_key[:16]

    # ultima rodada
    state = sub_bytes(block)
    state = shift_row(state)
    state = add_round_key(exp_key[:16], state)
    del exp_key[:16]

    return state


def aes_decrypt(block, key, n_round):
    exp_key = key_expansion(key)

    state = add_round_key(exp_key[-16:], block)
    del exp_key[-16:]

    for i in range(n_round - 1):
        state = shift_row_inv(state)
        state = sub_bytes_inv(state)
        state = add_round_key(exp_key[-16:], state)
        del exp_key[-16:]
        state = mix_columns_inv(state)

    state = shift_row_inv(state)
    state = sub_bytes_inv(state)
    state = add_round_key(exp_key[:16], state)
    del exp_key[-16:]

    return state


####################################################################
# modo ctr
def aes_ctr_encrypt(plaintext, key, nonce, n_round):
    ciphertext = []

    for i in range(0, len(plaintext), 16):
        ####counter = nonce.to_bytes(16, byteorder='big') # transforma nonce em uma sequencia de 16 bytes
        counter = i
        counter = counter.to_bytes(16, byteorder='big')
        count_list = list(counter)  # cria uma lista para os 16 bytes, cada elemento equivale a 1 byte
        keystream = aes_encrypt(count_list, key, n_round)

        # XOR da keystream com o bloco de texto original
        ciphertext_block = [p ^ k for p, k in zip(plaintext[i:i + 16], keystream)]
        ciphertext.extend(ciphertext_block)
        # print(ciphertext_block, i)
        nonce = nonce + counter  # Incrementa o nonce para o próximo bloco
        ####nonce+=1

    return ciphertext


def aes_ctr_decrypt(ciphertext, key, nonce, n_round):
    plaintext = []

    for i in range(0, len(ciphertext), 16):
        ####counter = nonce.to_bytes(16, byteorder='big')
        counter = i
        counter = counter.to_bytes(16, byteorder='big')
        count_list = list(counter)
        keystream = aes_encrypt(count_list, key, n_round)

        # XOR da keystream com o bloco de texto cifrado
        plaintext_block = [c ^ k for c, k in zip(ciphertext[i:i + 16], keystream)]
        plaintext.extend(plaintext_block)
        # print(plaintext_block, i)
        nonce = nonce + counter
        ####nonce+=1

    return plaintext


###############################################################################

# Exemplo de uso:
# plaintext = [0x32, 0x88, 0x31, 0xe0, 0x43, 0x5a, 0x31, 0x37, 0xf6, 0x30, 0x98, 0x07, 0xa8, 0x8d, 0xa2, 0x34]
# key = [15, 21, 113, 201, 71, 217, 232, 89, 12, 183, 173, 214, 175, 127, 103, 152]
#nonce = 0  # Valor inicial do contador (nonce)
#key = generate_key()
#nonce = secrets.token_bytes(16)

# abre imagem
#with Image.open("chihiro.jpg") as img:
#    img_data = img.tobytes()

# gera imagem com 1 rodada
#ciphertext = aes_ctr_encrypt(img_data, key, nonce, 1)  # Cifração em modo CTR
#with Image.frombytes(img.mode, img.size, bytes(ciphertext)) as output_img:
#    output_img.save("rodada-1.jpg")

# gera imagem com 5 rodadas
#ciphertext = aes_ctr_encrypt(img_data, key, nonce, 5)  # Cifração em modo CTR
#with Image.frombytes(img.mode, img.size, bytes(ciphertext)) as output_img:
#    output_img.save("rodada-5.jpg")

# gera imagem com 9 rodadas
#ciphertext = aes_ctr_encrypt(img_data, key, nonce, 9)  # Cifração em modo CTR
#with Image.frombytes(img.mode, img.size, bytes(ciphertext)) as output_img:
#    output_img.save("rodada-9.jpg")

# gera imagem a partir da decifracao
#plaintext_decrypted = aes_ctr_decrypt(ciphertext, key, nonce, 9)  # Decifração em modo CTR
#with Image.frombytes(img.mode, img.size, bytes(plaintext_decrypted)) as output_img:
#    output_img.save("result.jpg")

#with open("teste.txt", 'r') as file:
#    text = file.read()
#    texto = text.encode()

#print("txt: ", text)
#print("\n\n")
#print("bytes: ", texto)
#print("\n\n")
#ciphertext = aes_ctr_encrypt(texto, key, nonce, 9)
#print("txt cifrado: ", ciphertext)
#print("\n\n")
#plaintext_decrypted = aes_ctr_decrypt(ciphertext, key, nonce, 9)
#string = ''.join(map(chr, plaintext_decrypted))
#print("txt decifrado: ", string)
#print("\n\n")
#y = bytes(plaintext_decrypted)
#string = y.decode()
#print("txt decifrado: ", string)
#print("\n\n")