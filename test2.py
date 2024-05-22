import bcchapi
import numpy as np
# Incluyendo credenciales explícitamente
import matplotlib.pyplot as plt
siete = bcchapi.Siete(file="credentials.txt")

df=siete.cuadro(
  series="F034.VVNN.FLU.CCHC.Z.0.T",
  nombres = ["imacec"]
)

df.plot()
plt.show()
print(df)
