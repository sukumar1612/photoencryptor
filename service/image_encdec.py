import cv2
import binascii
from service.aes import AESCipher


class Imgencdec:
    image_name = "image.png"

    def __init__(self, password):
        self.aes = AESCipher(password)

    @staticmethod
    def add_zeros(n, text):
        zeros = ['0' for i in range(0, n - len(text))]
        return ''.join(zeros) + text

    @staticmethod
    def convert_hexstring_to_bitstring_list(text):
        binary_list = []
        text = list(text)
        text = [bin(int(hex_val, 16)) for hex_val in text]
        for i in range(0, len(text), 2):
            nibble1 = Imgencdec.add_zeros(4, text[i].split('0b')[1])
            nibble2 = Imgencdec.add_zeros(4, text[i + 1].split('0b')[1])
            byte = nibble1 + nibble2
            binary_list.append(byte)

        return binary_list

    @staticmethod
    def convert_bitstring_list_to_hexstring(bit_list):
        hex_string = ''
        for i in bit_list:
            nibble1 = hex(int(i[:4], 2)).split("0x")[1]
            nibble2 = hex(int(i[4:], 2)).split("0x")[1]
            hex_string += nibble1 + nibble2

        return hex_string

    def encode(self, text):
        cipher = self.aes.encrypt(text)
        byte_list = Imgencdec.convert_hexstring_to_bitstring_list(cipher)
        return byte_list

    def decode(self, bit_list):
        text = Imgencdec.convert_bitstring_list_to_hexstring(bit_list)
        #print(text)
        decrypt = self.aes.decrypt(text)
        return decrypt

    def img_encode(self, text, img_name):
        img = cv2.imread(self.image_name, cv2.IMREAD_COLOR)
        data = self.encode(text)
        #print(data)
        data = ''.join(data)
        if len(data) % 3 != 0:
            zeros = ['0' for i in range(3 - len(data) % 3)]
            data += ''.join(zeros)
            #print("inside")
        n = 3
        data = [data[i:i + n] for i in range(0, len(data), n)]
        cnt = 0

        for i in range(0, len(img)):
            for j in range(0, len(img)):
               # print(img[i][j], end="-----")
                if cnt >= len(data):
                    img[i][j][0] = img[i][j][0] + 1
                    img[i][j][1] = img[i][j][1] + 1
                    img[i][j][2] = img[i][j][2] + 1
                   # print(img[i][j])
                   # print(cnt)
                else:
                    img[i][j][0] = img[i][j][0] + int(data[cnt][0])
                    img[i][j][1] = img[i][j][1] + int(data[cnt][1])
                    img[i][j][2] = img[i][j][2] + int(data[cnt][2])

                   # print(img[i][j])
                    #print(int(data[cnt][0]), int(data[cnt][1]), int(data[cnt][2]))
                    #print(len(data), cnt)

                cnt = cnt + 1

                if cnt + 1 >= len(data) + 10:
                    cv2.imwrite(img_name, img)
                    #print("----out----")
                    return True
        return True

    def img_read(self, img_name):
        img = cv2.imread(self.image_name, cv2.IMREAD_COLOR)
        enc_img = cv2.imread(img_name, cv2.IMREAD_COLOR)
        if enc_img is None:
            return False

        data = ''
        zero_cnt = 0

        for i in range(0, len(img)):
            for j in range(0, len(img)):
               # print(enc_img[i][j], "------", img[i][j])
                b1 = enc_img[i][j][0] - img[i][j][0]
                b2 = enc_img[i][j][1] - img[i][j][1]
                b3 = enc_img[i][j][2] - img[i][j][2]

                if (b1 == 1 and b2 == 1 and b3 == 1):
                    zero_cnt = zero_cnt + 1
                else:
                    zero_cnt = 0

                if (zero_cnt >= 9):
                    return data

                b1 = str(b1)
                b2 = str(b2)
                b3 = str(b3)

                data += b1 + b2 + b3
                #print(b1, " ", b2, " ", b3)
        return data

    def img_decode(self, img_name):
        data = self.img_read(img_name)
        n = 3
        data = [data[i:i + n] for i in range(0, len(data), n)]
        data = [data[i] for i in range(0, len(data) - 8)]

        data = ''.join(data)
        n = 8
        data = [data[i:i + n] for i in range(0, len(data), n)]
        data = [i for i in data if(len(i)==8)]

        return self.decode(data)

'''
txt = """LUCKNOW: After sweeping the Zila Panchayat chairman elections, the BJP-supported candidates had registered win in over 630 out of 825 block pramukh seats on Saturday, till now. The development potentially armed the saffron party with the proof to claim its large-scale political presence in the rural swathes ahead of the high stake UP assembly elections due next year.
Immediately after the results were announced, chief minister Yogi Adityanath told reporters that it was a mandate for the policy of ‘Sabka Saath Sabka Vikas Sabka Vishwas'.
READ ALSO
349 of 825 block chairman candidates in UP elected unopposed: State Election Commission
The State Election Commission (SEC) announced the election of 349 candidates for block chairman seats as unopposed after 187 candidates took back their nomination papers on Friday.

349 of 825 block chairman candidates in UP elected unopposed: State Election Commission
According to reports, the BJP-supported candidates contested on 735 seats, while 14 seats were given to its ally Apna Dal (S). The party also gave an unannounced support to 76 candidates while agreeing not to field its officially supported candidates. As results trickled in, BJP and its ally AD (S) supported candidates were poised for a win on 635 seats. The Samajwadi Party-backed candidates, according to reports, won in over 70 seats, while Congress supported candidates managed a win on just two seats. The independents won around 95 seats.
A day ago, as many as 349 candidates were elected unopposed after 187 candidates took back their nomination papers on Friday. Polling for the remaining 476 seats were conducted on Saturday. The BJP had claimed that its supported candidates won unopposed on 334 seats.
"""


txt = txt.encode("utf-8")
x = Imgencdec(password="password123")
x.img_encode(txt, "bt.png")
print(x.img_decode("bt.png"))

a2=xx2[1]

a2 = ''.join(a2)
n = 3
a2 = [a2[i:i + n] for i in range(0, len(a2), n)]

for i in range(len(a2)):
    if a1[i] == a2[i]:
        print(a1[i], "----", a2[i], "ok")
        print(i)
    else:
        print(a1[i], "!----!", a2[i], "-----!", i)


print(xx2[0])
print(len(a1), len(a2))

'''