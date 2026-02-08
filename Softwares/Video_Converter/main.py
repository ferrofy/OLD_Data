from Files import MKV_To_MP4

Current_Format = input("Which File Format You Have ----> ").lower()
Convert_Format = input("In Which Format You Want To Convert ----> ").lower()

if Current_Format == "mkv":
    if Convert_Format == "mp4":
        print("Opening Converter....")
        MKV_To_MP4.Convert() # Fix This Error
        print("Done Conversion...")
else:
    print("This File Format Is Not Avaliable")