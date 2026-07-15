import hashlib

def Blake2b(Text):
    Hash = hashlib.blake2b(Text.encode()).hexdigest()
    return Hash

def Blake2s(Text):
    Hash = hashlib.blake2s(Text.encode()).hexdigest()
    return Hash