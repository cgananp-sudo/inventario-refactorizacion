import pytest
import inventario_legacy


class ConexionFalsa:
    def __init__(self, filas):
        self.filas = filas

    def query(self, sql):
        return self.filas

    def close(self):
        pass


CASOS = [
    ([], []),                                                    # lista vacía
    ([{"id": 1, "nombre": "A", "cantidad": 4}], "Bajo stock"),   # justo bajo el límite
    ([{"id": 2, "nombre": "B", "cantidad": 5}], "OK"),           # límite exacto
    ([{"id": 3, "nombre": "C", "cantidad": 0}], "Bajo stock"),   # cero
    ([{"id": 4, "nombre": "D", "cantidad": 50}], "OK"),          # stock alto
]


@pytest.mark.parametrize("filas,esperado", CASOS)
def test_caja_negra_legacy(monkeypatch, filas, esperado):
    monkeypatch.setattr(inventario_legacy, "conectar_db", lambda: ConexionFalsa(filas))
    resultado = inventario_legacy.obtener_inventario()
    if not filas:
        assert resultado == []
    else:
        assert resultado[0]["estado"] == esperado