"""Módulo de inventario refactorizado: consulta productos y calcula su estado de stock."""
from inventario_legacy import conectar_db  # simulación de la base de datos

UMBRAL_BAJO_STOCK = 5


def calcular_estado(cantidad, umbral=UMBRAL_BAJO_STOCK):
    """Devuelve 'Bajo stock' si la cantidad es menor al umbral, o 'OK' en caso contrario."""
    return "Bajo stock" if cantidad < umbral else "OK"


def construir_item(producto):
    """Arma el diccionario de respuesta de un producto, incluyendo su estado."""
    return {
        "id": producto["id"],
        "nombre": producto["nombre"],
        "cantidad": producto["cantidad"],
        "estado": calcular_estado(producto["cantidad"]),
    }


class ProductoRepositorio:
    """Acceso a datos: consulta solo las columnas necesarias de productos."""

    def __init__(self, conexion):
        self.conexion = conexion

    def listar(self):
        """Devuelve los productos (id, nombre, cantidad)."""
        return self.conexion.query("SELECT id, nombre, cantidad FROM productos")


class InventarioService:
    """Capa de servicio: aplica la regla de negocio sobre los datos del repositorio."""

    def __init__(self, repositorio):
        self.repositorio = repositorio

    def obtener_inventario(self):
        """Devuelve la lista de productos con su estado de stock."""
        return [construir_item(p) for p in self.repositorio.listar()]


def obtener_inventario():
    """Misma firma que la versión legada (compatibilidad). Cierra la conexión al terminar."""
    conexion = conectar_db()
    try:
        return InventarioService(ProductoRepositorio(conexion)).obtener_inventario()
    finally:
        conexion.close()