from PIL import Image


def text_to_binary(message):
    # Formatting the input text to binary
    return [format(ord(c), '08b') for c in message]


def encode_message(image, message):
    w = image.size[0]  # getting the width which is the first index of the image.size method

    list_of_bin = text_to_binary(message)
    len_of_bin = len(list_of_bin)

    # extract image data
    imdata = iter(image.getdata())

    new_pixel = []

    for i in range(len_of_bin):
        # making a list of three pixels per index
        pix = [value for value in imdata.__next__()[:3] +
               imdata.__next__()[:3] +
               imdata.__next__()[:3]]

        for j in range(0, 8):
            if list_of_bin[i][j] == '0' and pix[j] % 2 != 0:
                pix[j] -= 1

            elif list_of_bin[i][j] == '1' and pix[j] % 2 == 0:
                if pix[j] != 0:
                    pix[j] -= 1
                else:
                    pix[j] += 1

        if i == len_of_bin - 1:
            if pix[-1] % 2 == 0:
                pix[-1] += 1
        else:
            if pix[-1] % 2 != 0:
                pix[-1] -= 1

        pix = tuple(pix)
        new_pixel.append(pix[0:3])
        new_pixel.append(pix[3:6])
        new_pixel.append(pix[6:9])
    (x, y) = (0, 0)
    for pixel in new_pixel:

        # inserting the pixel back into the image
        image.putpixel((x, y), pixel)
        if x == w - 1:
            x = 0
            y += 1
        else:
            x += 1

    save_as = input("Enter a new name for the image (without file type): ")
    image.save(save_as, "PNG")


# Decoding the message in the image file
def decode_message(img_name):
    image_received = Image.open(img_name, 'r')

    message = ''
    imgdata = iter(image_received.getdata())

    while True:
        pixels = [value for value in imgdata.__next__()[:3] +
                  imgdata.__next__()[:3] +
                  imgdata.__next__()[:3]]

        binstr = ''

        for i in pixels[:8]:
            if i % 2 == 0:
                binstr += '0'
            else:
                binstr += '1'

        message += chr(int(binstr, 2))
        if pixels[-1] % 2 != 0:
            return message


def main():
    global choice, image
    choice = input("Please enter mode (E)ncode or (D)ecode: ")
    if choice.lower() == "e":
        file_name = input("Enter the image name to encode with the extension type: ")
        try:
            image = Image.open(file_name)
        except:
            print("Image does not exist in folder")
        else:
            message = input("Enter the message to encode: ")
            encode_message(image, message)
            print("File saved, enter q to make it show in the project folder")

    elif choice.lower() == "d":
        file_name = input("Enter image name to decode: ")
        try:
            image = Image.open(file_name)

        except:
            print("Image does not exist in folder")
        else:
            print("Found: " + decode_message(file_name))
    elif choice.lower() == "q":
        print("Response: Program quited")
        choice = "q"
    else:
        print("Invalid choice!!!")


if __name__ == '__main__':
    choice = ""
    image = None
    while choice.lower() != "q":
        main()

