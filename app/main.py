import sys
import os
import subprocess
import random

# Permitir importar transmission
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from transmission.client import send_message
from transmission.server import start_server

# =========================
# Capa de Ruido
# =========================
def apply_noise(bits: str, error_prob: float) -> str:
    noisy_bits = []
    for bit in bits:
        if random.random() < error_prob:
            noisy_bits.append('1' if bit == '0' else '0')
        else:
            noisy_bits.append(bit)
    return ''.join(noisy_bits)

# =========================
# Algoritmos CRC32
# =========================
def run_crc32_sender(msg):
    result = subprocess.run([sys.executable, "crc32/sender.py"], input=msg.encode(), capture_output=True)
    return result.stdout.decode().strip()

def run_crc32_receiver(trama):
    if not os.path.exists("crc32/receiver"):
        subprocess.run(["g++", "crc32/receiver.cpp", "-o", "crc32/receiver"])
    result = subprocess.run(["./crc32/receiver"], input=trama.encode(), capture_output=True)
    return result.stdout.decode().strip()

# =========================
# Algoritmos Hamming74
# =========================
def run_hamming_sender(msg):
    if not os.path.exists("hamming74/sender"):
        subprocess.run(["g++", "hamming74/sender.cpp", "-o", "hamming74/sender"])
    result = subprocess.run(["./hamming74/sender"], input=msg.encode(), capture_output=True)
    return result.stdout.decode().strip()

def run_hamming_receiver(trama):
    result = subprocess.run([sys.executable, "hamming74/receiver.py"], input=trama.encode(), capture_output=True)
    return result.stdout.decode().strip()

# =========================
# Main principal
# =========================
def main():
    mode = input("Selecciona modo (emisor/receptor): ").strip().lower()
    algorithm = input("Selecciona algoritmo (crc/hamming): ").strip().lower()

    if mode == "emisor":
        msg = input("Mensaje a enviar: ").strip()
        error_prob = float(input("Probabilidad de error (ej. 0.01 para 1%): ").strip())

        # 1) Codificar
        if algorithm == "crc":
            trama = run_crc32_sender(msg)
        else:
            trama = run_hamming_sender(msg)

        # 2) Aplicar ruido
        print(f"[INFO] Aplicando ruido con probabilidad {error_prob*100:.2f}%...")
        noisy_trama = apply_noise(trama, error_prob)
        print(f"[INFO] Trama original: {trama[:64]}... (longitud {len(trama)})")
        print(f"[INFO] Trama con ruido: {noisy_trama[:64]}... (longitud {len(noisy_trama)})")

        # 3) Enviar al receptor
        send_message(noisy_trama)

    elif mode == "receptor":
        trama = start_server(port=5050)  # <-- puerto fijo 5050
        if algorithm == "crc":
            print(run_crc32_receiver(trama))
        else:
            print(run_hamming_receiver(trama))
    else:
        print("Modo inválido.")

if __name__ == "__main__":
    main()
