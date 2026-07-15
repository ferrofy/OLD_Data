import qrcode

def Make_QR(Data, File_Name , Location):
    QR = qrcode.make(Data)
    QR.save(fr"{Location}\{File_Name}")