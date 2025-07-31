#!/usr/bin/env python3
import os
import sys
import subprocess
import random

# Para poder importar transmission/ desde el padre
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from transmission.client import send_message
from transmission.server import start_server

def pres_encode(text: str) -> str:
    bits = ''.join(f"{ord(c):08b}" for c in text)
    print(f">> [PRESENTACIÓN] Bits ASCII:\n{bits}\n")
    return bits

def pres_decode(bits: str) -> str:
    text = ''.join(chr(int(bits[i:i+8], 2)) for i in range(0, len(bits), 8))
    print(f">> [PRESENTACIÓN] Texto: {text}\n")
    return text

def enlace_hamming_encode(bits: str) -> str:
    code = subprocess.check_output(
        ["../hamming74/sender"],
        input=bits.encode()
    ).decode().strip()
    print(f">> [ENLACE] Hamming (7,4) code:\n{code}\n")
    return code

def enlace_hamming_decode(frame: str) -> (str, bool):
    out = subprocess.check_output(
        ["python3", "../hamming74/receiver.py"],
        input=frame.encode()
    ).decode().strip()
    print(f">> [ENLACE] {out}\n")
    if "Datos:" in out:
        data_bits = out.split("Datos:")[1].strip()
        return data_bits, True
    return "", False

def enlace_crc_encode(bits: str) -> str:
    frame = subprocess.check_output(
        ["python3", "../crc32/sender.py"],
        input=bits.encode()
    ).decode().strip()
    print(f">> [ENLACE] Frame + CRC32:\n{frame}\n")
    return frame

def enlace_crc_decode(frame: str) -> (str, bool):
    # Lanza el receptor de CRC y captura stdout completo
    proc = subprocess.run(
        ["../crc32/receiver"],
        input=frame.encode(),
        capture_output=True,
        check=True
    )
    out = proc.stdout.decode()
    print(f">> [ENLACE] {out}")

    # Si la comprobación pasó, buscamos la línea con los bits
    if "Sin errores" in out:
        for line in out.splitlines():
            # Aquí capturamos justo la línea que empieza con "Mensaje decodificado:"
            if line.lower().startswith("mensaje decodificado"):
                data_bits = line.split(":", 1)[1].strip()
                # DEBUG opcional:
                print(f"DEBUG datos extraídos: {data_bits}")
                return data_bits, True

        # Fallback: si no encontramos esa línea, recortamos el CRC
        print("DEBUG: no hallé 'Mensaje decodificado', recorto CRC manualmente")
        return frame[:-32], True

    # Si falla la comprobación de CRC
    print(">> [ENLACE] ERROR: CRC inválido, trama descartada")
    return "", False


def ruido_layer(frame: str, p: float) -> str:
    flips = []
    lst = list(frame)
    for i, b in enumerate(lst):
        if random.random() < p:
            lst[i] = '1' if b == '0' else '0'
            flips.append(i)
    noisy = ''.join(lst)
    print(f">> [RUIDO] Bits volteados en posiciones: {flips}")
    print(f">> [RUIDO] Trama ruidosa:\n{noisy}\n")
    return noisy

def main():
    mode = input("Modo (emisor/receptor): ").strip().lower()
    alg  = input("Algoritmo (hamming/crc): ").strip().lower()

    if mode == "emisor":
        # Aplicación
        text = input(">> [APLICACIÓN] Mensaje a enviar: ")
        # Presentación
        bits = pres_encode(text)
        # Enlace (encode)
        if alg == "hamming":
            frame = enlace_hamming_encode(bits)
        else:
            frame = enlace_crc_encode(bits)
        # Ruido
        p = float(input(">> [RUIDO] Tasa de error [0–1]: "))
        noisy = ruido_layer(frame, p)
        # Transmisión
        send_message(noisy)
        print(">> [TRANSMISIÓN] Trama enviada.\n")

    elif mode == "receptor":
        # Transmisión (recv)
        frame = start_server()
        # Enlace (decode)
        if alg == "hamming":
            data_bits, ok = enlace_hamming_decode(frame)
        else:
            data_bits, ok = enlace_crc_decode(frame)
        if not ok:
            print(">> [APLICACIÓN] ERROR: trama irrecuperable. Mensaje descartado.\n")
            return
        # Presentación (decode)
        pres_decode(data_bits)
        # Aplicación
        print(">> [APLICACIÓN] Mensaje recibido correctamente.\n")

    else:
        print("Modo inválido. Usa 'emisor' o 'receptor'.")

if __name__ == "__main__":
    main()