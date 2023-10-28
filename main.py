import secrets
import aes
import os
from PIL import Image


continua = True
key = aes.generate_key() #gera a chave aleatória que será utilizada durante toda a execução do programa

#se quiser que a chave mude, bote a instrução acima dentro de um if(escolha == 1 ou 2)

nonce = secrets.token_bytes(16) #nonce aleatório, será somado com o contador nas funções encrypt e decrypt do AES

while continua:
    print("Escolha:")
    print("[1] Cifrar e decifrar um arquivo de texto")
    print("[2] Cifrar uma imagem")
    print("[3] Decifrar a imagem") #opção para testar se você consegue obter a imagem que foi cifrada
    print("[4] Fechar o programa")
    escolha = int(input())
    if(escolha == 4): #encerra o programa
        continua = False
        continue
    if(escolha != 3):
        rodadas = int(input("Digite o número de rodadas (entre 1 e 9): "))

    if(rodadas < 1 or rodadas > 9):
        os.system('cls' if os.name == 'nt' else 'clear')  # limpa o terminal no windows e no linux
        print("Digite uma quantidade de rodadas válida!")
        continue

    if(escolha == 1):
        arquivo = input("Digite o nome do arquivo com a extensão dele: ")
        with open(arquivo, 'r') as file:
            text = file.read()
            str_file = text.encode()
        print("Chave utilizada: ", key, "\n")
        ciphertext = aes.aes_ctr_encrypt(str_file, key, nonce, rodadas)
        print("Texto cifrado: ", ciphertext, "\n")
        plaintext_decrypted = aes.aes_ctr_decrypt(ciphertext, key, nonce, rodadas)
        my_bytes = bytes(plaintext_decrypted) #transforma a saída do aes em bytes, para que o python consiga decodificar a string
        print("Texto decifrado:\n", my_bytes.decode())
        print("\n\nDeseja continuar? [s, n]: ")
        repetir = input()
        if(repetir == "s"):
            continua = True
            os.system('cls' if os.name == 'nt' else 'clear') #limpa o terminal no windows e no linux
        else:
            continua = False
    elif(escolha == 2):
        arquivo = input("Digite o nome do arquivo com a extensão dele: ")
        with Image.open(arquivo) as img:
            img_data = img.tobytes()
        print("Chave utilizada: ", key, "\n")
        ciphertext = aes.aes_ctr_encrypt(img_data, key, nonce, rodadas)
        with Image.frombytes(img.mode, img.size, bytes(ciphertext)) as output_img:
            output_img.save("result.jpg")
        print("Deseja continuar? [s, n]: ")
        repetir = input()
        if (repetir == "s"):
            continua = True
            os.system('cls' if os.name == 'nt' else 'clear')  # limpa o terminal no windows e no linux
        else:
            continua = False
    # o motivo para exigir a imagem original, é que precisa do ciphertext para para decifrar
    # daí é necessário cifrar a imagem de novo para recuperar o ciphertext e só então decifrar
    # o if abaixo não funciona se a key mudar a cada rodada do while!
    elif(escolha == 3):
        print("Chave utilizada: ", key, "\n")
        arquivo2 = input("Digite o nome da imagem que GEROU a imagem cifrada junto com a extensão dele: ")
        arquivo = input("Digite o nome da imagem a ser DECIFRADA com a extensão dela: ")
        rodadas = int(input("Digite o número de rodadas que a imagem passou: "))
        if (rodadas < 1 or rodadas > 9):
            os.system('cls' if os.name == 'nt' else 'clear')  # limpa o terminal no windows e no linux
            print("Número de rodadas para decifrar inválido!")
            continue
        with Image.open(arquivo2) as img2:
            img2_data = img2.tobytes()
        ciphertext = aes.aes_ctr_encrypt(img2_data, key, nonce, rodadas) #cifra imagem original para obter o ciphertext
        plaintext_decrypted = aes.aes_ctr_decrypt(ciphertext, key, nonce, rodadas)
        with Image.open(arquivo) as img:
            img_data = img.tobytes()
        with Image.frombytes(img.mode, img.size, bytes(plaintext_decrypted)) as output_img:
            output_img.save("result.jpg")
        print("Deseja continuar? [s, n]: ")
        repetir = input()
        if (repetir == "s"):
            continua = True
            os.system('cls' if os.name == 'nt' else 'clear')  # limpa o terminal no windows e no linux
        else:
            continua = False
    else:
        os.system('cls' if os.name == 'nt' else 'clear')  # limpa o terminal no windows e no linux
        print("Digite uma opção válida!")
