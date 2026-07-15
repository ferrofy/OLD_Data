import hashlib

def SHA1(Text):
    Hash = hashlib.sha1(Text.encode()).hexdigest()
    return Hash

def SHA224(Text):
    Hash = hashlib.sha224(Text.encode()).hexdigest()
    return Hash

def SHA256(Text):
    Hash = hashlib.sha256(Text.encode()).hexdigest()
    return Hash

def SHA384(Text):
    Hash = hashlib.sha384(Text.encode()).hexdigest()
    return Hash

def SHA512(Text):
    Hash = hashlib.sha512(Text.encode()).hexdigest()
    return Hash

def SHA3_224(Text):
    Hash = hashlib.sha3_224(Text.encode()).hexdigest()
    return Hash

def SHA3_256(Text):
    Hash = hashlib.sha3_256(Text.encode()).hexdigest()
    return Hash

def SHA3_384(Text):
    Hash = hashlib.sha3_384(Text.encode()).hexdigest()
    return Hash

def SHA3_512(Text):
    Hash = hashlib.sha3_512(Text.encode()).hexdigest()
    return Hash