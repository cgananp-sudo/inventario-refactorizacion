UMBRAL_BAJO_STOCK = 5


def calcular_estado(cantidad, umbral=UMBRAL_BAJO_STOCK):
    return "Bajo stock" if cantidad < umbral else "OK"
