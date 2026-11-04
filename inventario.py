from inventario_legacy import conectar_db  # simulación de la base de datos

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


class ProductoRepositorio:
    def __init__(self, conexion):
        self.conexion = conexion

    def listar(self):
        return self.conexion.query("SELECT id, nombre, cantidad FROM productos")


class InventarioService:
    def __init__(self, repositorio):
        self.repositorio = repositorio

    def obtener_inventario(self):
        return [construir_item(p) for p in self.repositorio.listar()]
