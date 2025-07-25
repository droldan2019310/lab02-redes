import sys

def decode_block(code7: str):
    b = [0] + [int(x) for x in code7]          # 1-index
    s1 = b[1]^b[3]^b[5]^b[7]
    s2 = b[2]^b[3]^b[6]^b[7]
    s4 = b[4]^b[5]^b[6]^b[7]
    pos = s4*4 + s2*2 + s1                     # 0 = sin error
    if pos!=0:
        b[pos] ^= 1
    data_bits = ''.join(str(b[i]) for i in (3,5,6,7))
    fixed = ''.join(str(b[i]) for i in range(1,8))
    return pos, fixed, data_bits

if __name__ == "__main__":
    # Entrada: "codigo_grande PAD"
    line = sys.stdin.readline().strip()
    parts = line.split()
    code_big = ''.join(ch for ch in parts[0] if ch in '01')
    pad = int(parts[1]) if len(parts)>1 else 0

    if len(code_big)%7 != 0:
        raise ValueError("La longitud del código no es múltiplo de 7.")

    n_blocks = len(code_big)//7
    data_all = []
    fixed_all = []
    errors = []

    for blk in range(n_blocks):
        c = code_big[blk*7:(blk+1)*7]
        pos, fixed, data = decode_block(c)
        fixed_all.append(fixed)
        data_all.append(data)
        if pos!=0:
            errors.append((blk, pos))  # bloque, bit

    # unir y quitar padding
    data_join = ''.join(data_all)
    if pad>0:
        data_join = data_join[:-pad]

    # Salida
    if not errors:
        print(f"Sin errores. Datos: {data_join}")
    else:
        # posiciones globales: bloque*7 + pos
        corr_list = [f"(blk {b+1}, bit {p})" for b,p in errors]
        print(f"Se corrigieron errores en {len(errors)} bloque(s): " + ', '.join(corr_list))
        print("Código corregido:", ''.join(fixed_all))
        print("Datos:", data_join)