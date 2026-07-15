import time
import random

Speed = 0.01
Text = "0123456789aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxXyYzZ"

Colors = [
"\033[91m",
"\033[92m",
"\033[93m",
"\033[94m",
"\033[95m",
"\033[96m"
]

Reset = "\033[0m"

def Typewriter_Effect():
    for Letter in Text:
        print(Letter,end="",flush=True)
        time.sleep(Speed)
    print("\n")

def Hacker_Decode():

    Characters="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%&"

    Result=""

    for Real in Text:

        for i in range(3):
            Fake=random.choice(Characters)
            print("\r"+Result+Fake,end="",flush=True)
            time.sleep(Speed)

        Result+=Real
        print("\r"+Result,end="",flush=True)

    print("\n")

def Glitch_Text():

    Characters="!@#$%^&*()_+=-[]{}<>?/"

    for i in range(12):

        Glitched=""

        for Letter in Text:

            if random.random()<0.25:
                Glitched+=random.choice(Characters)
            else:
                Glitched+=Letter

        print("\r"+Glitched,end="",flush=True)
        time.sleep(Speed*5)

    print("\r"+Text+"\n")

def Rainbow_Text():

    for Letter in Text:

        Color=random.choice(Colors)
        print(Color+Letter+Reset,end="",flush=True)
        time.sleep(Speed)

    print("\n")

def Progress_Reveal():

    Result=""

    for Letter in Text:

        Result+=Letter
        print("\r"+Result,end="",flush=True)
        time.sleep(Speed)

    print("\n")

def Random_Scramble():

    Characters="ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    Display=list(Text)

    for i in range(len(Display)):

        for j in range(4):

            Display[i]=random.choice(Characters)
            print("\r"+"".join(Display),end="",flush=True)
            time.sleep(Speed)

        Display[i]=Text[i]

    print("\r"+Text+"\n")

def Flash_Text():

    for i in range(6):

        print("\r"+Text,end="",flush=True)
        time.sleep(Speed*20)

        print("\r"+" "*len(Text),end="",flush=True)
        time.sleep(Speed*20)

    print("\r"+Text+"\n")

def Reverse_Reveal():

    for i in range(len(Text)):

        Part=Text[len(Text)-i-1:]
        print("\r"+Part,end="",flush=True)
        time.sleep(Speed)

    print("\n")

def Binary_Decode():

    Binary=" ".join(format(ord(c),"08b") for c in Text)

    print(Binary)
    time.sleep(1)

    print(Text+"\n")

def Scatter_Fix():

    Letters=list(Text)

    random.shuffle(Letters)

    for i in range(15):

        random.shuffle(Letters)
        print("\r"+"".join(Letters),end="",flush=True)
        time.sleep(Speed*10)

    print("\r"+Text+"\n")

def Fade_Reveal():

    Result=[" "]*len(Text)

    for i in range(len(Text)):

        Result[i]=Text[i]
        print("\r"+"".join(Result),end="",flush=True)
        time.sleep(Speed)

    print("\n")

def Case_Flicker():

    for i in range(10):

        Temp=""

        for c in Text:

            if random.random()<0.5:
                Temp+=c.lower()
            else:
                Temp+=c.upper()

        print("\r"+Temp,end="",flush=True)
        time.sleep(Speed*8)

    print("\r"+Text+"\n")

# Typewriter_Effect()
Hacker_Decode()
Glitch_Text()
Rainbow_Text()
Progress_Reveal()
Random_Scramble()
Flash_Text()
Reverse_Reveal()
Binary_Decode()
Scatter_Fix()
Fade_Reveal()
Case_Flicker()