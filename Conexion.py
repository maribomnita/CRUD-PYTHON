import sqlite3

def conectar():
    MiConexion = sqlite3.connect("crud.db")
    cursor = MiConexion.cursor()
    try:
        sql = """
        CREATE TABLE IF NOT EXISTS personas(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dni TEXT NOT NULL UNIQUE,
            edad INTEGER NOT NULL,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            direccion TEXT DEFAULT "NO TIENE",
            correo TEXT NOT NULL UNIQUE
        )
        """
        cursor.execute(sql)
    except Exception as ex:
        print("ERROR DE CONEXION: ", ex)
    finally:
        cursor.close()
    
    return MiConexion


conexion = conectar()
conexion.close()
