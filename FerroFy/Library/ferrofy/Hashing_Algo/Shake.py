import hashlib

def SHAKE_128(Text, Length=32):
    Hash = hashlib.shake_128(Text.encode()).hexdigest(Length)
    return Hash

def SHAKE_256(Text, Length=64):
    Hash = hashlib.shake_256(Text.encode()).hexdigest(Length)
    return Hash