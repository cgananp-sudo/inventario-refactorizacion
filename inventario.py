UMBRAL_BAJO_STOCK = 5


def calcular_estado(cantidad, umbral=UMBRAL_BAJO_STOCK):
    return "Bajo stock" if cantidad < umbral else "OK"


def construir_item(producto):
    return {
        "id": producto["id"],
        "nombre": producto["nombre"],
        "cantidad": producto["cantidad"],
        "estado": calcular_estado(producto["cantidad"]),
    }
