Action = input("""If You Want To Make QR , Type M
If You Want To Read QR Type , R

What You Want To Do ----> """).strip().lower()

if Action == "m":
    from Files import Maker
    Maker.Make_QR()
elif Action == "r":
    from Files import Reader
    print("Comming Soon Feature...")
else:
    print("Wrong Input...")