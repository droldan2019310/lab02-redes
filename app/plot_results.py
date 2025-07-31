import pandas as pd
import matplotlib.pyplot as plt

# lee los datos
df = pd.read_csv("app/results.csv")

# grafica
for alg in df['algoritmo'].unique():
    sub = df[df['algoritmo']==alg]
    plt.plot(sub['error_rate'], sub['success_rate'], marker='o', label=alg)

plt.title("Tasa de entrega correcta vs. tasa de error")
plt.xlabel("Tasa de error (p)")
plt.ylabel("Tasa de éxito")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()