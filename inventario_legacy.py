class ConexionFalsa:
    def query(self, sql):
        return [
            {"id": 1, "nombre": "Tornillos", "cantidad": 3},
            {"id": 2, "nombre": "Tuercas", "cantidad": 20},
        ]

    def close(self):
        pass


def conectar_db():
    return ConexionFalsa()


def obtener_inventario():
    conexion = conectar_db()
    datos = conexion.query("SELECT * FROM productos")
    lista = []
    for d in datos:
        if d['cantidad'] < 5:
            alerta = "Bajo stock"
        else:
            alerta = "OK"
        lista.append({
            "id": d['id'],
            "nombre": d['nombre'],
            "cantidad": d['cantidad'],
            "estado": alerta
        })
    return lista


if __name__ == "__main__":
    print(obtener_inventario())
    