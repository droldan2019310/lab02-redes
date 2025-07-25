#!/usr/bin/env python3
import subprocess
import random

def app_layer():
    text = input(">> [APP] Mensaje a enviar: ")
    return text

def pres_layer(text):
    bits = ''.join(f"{ord(c):08b}" for c in text)
    print(f">> [PRES] ASCII bits:\n{bits}\n")
    return bits

def enlace_layer(bits):
    # Llama al emisor Hamming 7,4 compilado en hamming74/sender
    out = subprocess.check_output(
        ["../hamming74/sender"],    # ruta corregida
        input=bits.encode()
    ).decode().strip()
    print(f">> [ENLACE] Código Hamming (7,4):\n{out}\n")
    return out

def ruido_layer(frame, p):
    out=[]; flips=[]
    for i,bit in enumerate(frame):
        if random.random() < p:
            bit = '1' if bit=='0' else '0'
            flips.append(i)
        out.append(bit)
    noisy = ''.join(out)
    print(f">> [RUIDO] Bits volteados en pos: {flips}")
    print(f">> [RUIDO] Trama ruidosa:\n{noisy}\n")
    return noisy

if __name__=="__main__":
    text      = app_layer()
    bits      = pres_layer(text)
    frame     = enlace_layer(bits)
    p = float(input(">> [NOISE] Tasa de error [0–1]: "))
    _ = ruido_layer(frame, p)  