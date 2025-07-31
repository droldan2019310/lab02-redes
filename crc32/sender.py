import sys, binascii



def to_binary_ascii(text: str) -> str:
    return ''.join(format(ord(c), '08b') for c in text)

def emit(bits: str) -> str:
    binary_msg = to_binary_ascii(bits)  # Convertir mensaje a bits`      `
    # a bytes
    b = int(binary_msg, 2).to_bytes((len(binary_msg)+7)//8, 'big')
    crc = binascii.crc32(b) & 0xffffffff
    return binary_msg + format(crc, '032b')

if __name__ == "__main__":
    msg = sys.stdin.readline().strip()
    print(emit(msg))