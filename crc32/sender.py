import sys, binascii

def emit(bits: str) -> str:
    # a bytes
    b = int(bits, 2).to_bytes((len(bits)+7)//8, 'big')
    crc = binascii.crc32(b) & 0xffffffff
    return bits + format(crc, '032b')

if __name__ == "__main__":
    msg = sys.stdin.readline().strip()
    print(emit(msg))