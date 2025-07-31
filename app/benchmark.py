#!/usr/bin/env python3
import subprocess
import random
import csv
import os
import sys
from time import sleep

# Parámetros
ERROR_RATES = [0.0, 0.01, 0.02, 0.05, 0.1, 0.2]
N_RUNS      = 30
MESSAGE     = "BenchmarkTest"

# Asegurarnos de estar en app/
os.chdir(os.path.dirname(__file__))

def run_pair(alg, p):
    """
    Ejecuta receptor y emisor secuencialmente, devuelve True si el receptor
    finalmente imprime 'Mensaje recibido correctamente'.
    """
    # 1) Levantar receptor en background
    server = subprocess.Popen(
        ["./main.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True
    )
    # enviarle al receptor el modo y el algoritmo por stdin
    server.stdin.write(f"receptor\n{alg}\n")
    server.stdin.flush()

    # brevemente esperamos a que el servidor esté escuchando
    sleep(0.1)

    # 2) Ejecutar emisor
    client = subprocess.run(
        ["./main.py"],
        input=f"emisor\n{alg}\n{MESSAGE}\n{p}\n",
        capture_output=True,
        text=True
    )

    # 3) Esperar a que el servidor termine
    try:
        out, _ = server.communicate(timeout=2)
    except subprocess.TimeoutExpired:
        server.kill()
        out = ""

    # 4) Interpretar salida
    return "Mensaje recibido correctamente" in out

# fichero de resultados
with open("results.csv", "w", newline="") as csvf:
    writer = csv.writer(csvf)
    writer.writerow(["algoritmo","error_rate","runs","successes","success_rate"])

    for alg in ("hamming","crc"):
        for p in ERROR_RATES:
            succ = 0
            for _ in range(N_RUNS):
                if run_pair(alg, p):
                    succ += 1
            rate = succ / N_RUNS
            writer.writerow([alg, p, N_RUNS, succ, f"{rate:.2f}"])
            print(f"{alg} @ p={p:.3f}: {succ}/{N_RUNS} → {rate:.2f}")