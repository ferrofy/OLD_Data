import qrcode

def Make_QR():
    No_Of_QR = int(input("How Many QR Code You Want To Make ---> "))

    for i in range(0 , No_Of_QR):
        Name = input(f"Enter Name Of {i+1} QR ---> ")
        Text = input("Enter The Text Inside The QR ---> ").strip()

        QR_Location = f"{Name}.png"

        QR = qrcode.QRCode()
        QR.add_data(Text)

        Img = QR.make_image()

        Img.save(QR_Location)
        print(f"Done.... Made {Name} as {i} QR")