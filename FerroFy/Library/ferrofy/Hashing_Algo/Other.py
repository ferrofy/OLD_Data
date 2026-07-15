import hashlib

def MD5(Text):
    Hash = hashlib.md5(Text.encode()).hexdigest()
    return Hash