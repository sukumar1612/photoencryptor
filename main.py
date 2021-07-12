import cv2
import numpy
from service.image_encdec import Imgencdec
import sys
import os
from time import sleep
import warnings

warnings.filterwarnings("ignore")

def menu():
    print("enter password")
    password = input()
    user = Imgencdec(password=password)
    while True:
        print("----------------------------------------photoencryptor----------------------------------------")
        print("--------enter option number--------")
        print("1)encrypt and store data")
        print("2)decrypt and retrieve data")
        print("any other key to exit")
        option = int(input("     :"))

        if (option == 1):
            file_name = input("enter new generated photo name without extension : ")
            file_name += '.png'
            os.system('cls')
            print("------- continue typing and press enter twice to exit -------")
            msg = []
            while True:
                line = input()
                if line:
                    msg.append(line)
                else:
                    break

            msg = '\n'.join(msg)
            msg = msg.encode("utf-8")
            user.img_encode(msg, file_name)
            print("successful")
            sleep(1)
            os.system('cls')

        elif (option == 2):
            file_name = input("enter new generated photo name without extension : ")
            file_name += '.png'
            os.system('cls')
            print("------available data------")
            print(user.img_decode(file_name))
            x = input("\n\n press any key to exit")
        else:
            os.system('cls')
            print("-------------------good bye-------------------")
            sleep(1)
            break


if __name__ == '__main__':
    menu()
