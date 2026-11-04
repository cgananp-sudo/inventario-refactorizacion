import pytest
import inventario_legacy
import inventario


class ConexionFalsa:
    def __init__(self, filas):
        self.filas = filas
        self.cerrada = False
        self.sql = None

    def query(self, sql):
        self.sql = sql
        return self.filas

    def close(self):
        self.cerrada = True


CASOS = [
    ([], []),                                                    # lista vacía
    ([{"id": 1, "nombre": "A", "cantidad": 4}], "Bajo stock"),   # justo bajo el límite
    ([{"id": 2, "nombre": "B", "cantidad": 5}], "OK"),           # límite exacto
    ([{"id": 3, "nombre": "C", "cantidad": 0}], "Bajo stock"),   # cero
    ([{"id": 4, "nombre": "D", "cantidad": 50}], "OK"),          # stock alto
]


@pytest.mark.parametrize("modulo", [inventario_legacy, inventario])
@pytest.mark.parametrize("filas,esperado", CASOS)
def test_caja_negra_regresion(monkeypatch, modulo, filas, esperado):
    monkeypatch.setattr(modulo, "conectar_db", lambda: ConexionFalsa(filas))
    resultado = modulo.obtener_inventario()
    if not filas:
        assert resultado == []
    else:
        assert resultado[0]["estado"] == esperado


def test_regresion_misma_salida(monkeypatch):
    filas = [d[0][0] for d in CASOS if d[0]]
    monkeypatch.setattr(inventario_legacy, "conectar_db", lambda: ConexionFalsa(filas))
    monkeypatch.setattr(inventario, "conectar_db", lambda: ConexionFalsa(filas))
    assert inventario_legacy.obtener_inventario() == inventario.obtener_inventario()


def test_caja_blanca_ambas_ramas():
    assert inventario.calcular_estado(4) == "Bajo stock"
    assert inventario.calcular_estado(5) == "OK"


def test_cierra_conexion_y_no_usa_select_estrella(monkeypatch):
    conexion = ConexionFalsa([])
    monkeypatch.setattr(inventario, "conectar_db", lambda: conexion)
    inventario.obtener_inventario()
    assert conexion.cerrada is True
    assert "*" not in conexion.sql
