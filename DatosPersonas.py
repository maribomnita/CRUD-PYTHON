import Conexion as con

def save(persona):
    persona = dict(persona)
    try:
        db = con.conectar()
        cursor = db.cursor()
        columnas = tuple(persona.keys())
        valores = tuple(persona.values())
        campos = ", ".join(columnas)
        placeholders = ", ".join("?" for _ in columnas)
        sql = f"INSERT INTO personas ({campos}) VALUES ({placeholders})"
        cursor.execute(sql, valores)
        creada = cursor.rowcount > 0
        db.commit()
        if creada:
            return {"respuesta": creada, "mensaje": "Persona Registrada"}
        else:
            return {"respuesta": creada, "mensaje": "No se logró registrar a la persona"}
    except Exception as ex:
        if "UNIQUE" in str(ex) and "correo" in str(ex):
            mensaje = "ya existe una persona con ese correo"
        elif "UNIQUE" in str(ex) and "dni" in str(ex):
            mensaje = "ya existe una persona con ese dni"
        else:
            mensaje = str(ex)
        return {"respuesta": False, "mensaje": mensaje}
    finally:
        cursor.close()
        db.close()

def findAll():
    try:
        db = con.conectar()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM personas")
        personas = cursor.fetchall()
        if personas:
            return {"respuesta": True, "personas": personas, "mensaje": "LISTADO OK"}
        else:
            return {"respuesta": False, "mensaje": "NO HAY PERSONAS REGISTRADAS AUN"}
    except Exception as ex:
        return {"respuesta": False, "mensaje": str(ex)}
    finally:
        cursor.close()
        db.close()

def findByDni(dni):
    try:
        db = con.conectar()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM personas WHERE dni = ?", (dni,))
        res = cursor.fetchone()
        if res:
            persona = {
                "id": res[0],
                "dni": res[1],
                "edad": res[2],
                "nombre": res[3],
                "apellido": res[4],
                "direccion": res[5],
                "correo": res[6]
            }
            return {"respuesta": True, "persona": persona, "mensaje": "PERSONA ENCONTRADA"}
        else:
            return {"respuesta": False, "mensaje": "NO EXISTE ESA PERSONA"}
    except Exception as ex:
        return {"respuesta": False, "mensaje": str(ex)}
    finally:
        cursor.close()
        db.close()

def update(persona):
    try:
        db = con.conectar()
        cursor = db.cursor()
        persona = dict(persona)
        dniPersona = persona.get("dni")
        if not dniPersona:
            return {"respuesta": False, "mensaje": "DNI es requerido para actualizar la persona"}
        
        persona.pop("dni")
        valores = tuple(persona.values())
        set_clause = ", ".join([f"{key} = ?" for key in persona.keys()])
        sql = f"""
        UPDATE personas
        SET {set_clause}
        WHERE dni = ?
        """
        cursor.execute(sql, valores + (dniPersona,))
        modificada = cursor.rowcount > 0
        db.commit()
        if modificada:
            return {"respuesta": modificada, "mensaje": "Persona actualizada"}
        else:
            return {"respuesta": modificada, "mensaje": "No existe la persona con ese dni"}
    except Exception as ex:
        if "UNIQUE" in str(ex) and "correo" in str(ex):
            mensaje = "ya existe una persona con ese correo"
        elif "UNIQUE" in str(ex) and "dni" in str(ex):
            mensaje = "ya existe una persona con ese dni"
        else:
            mensaje = str(ex)
        return {"respuesta": False, "mensaje": mensaje}
    finally:
        cursor.close()
        db.close()

def delete(idPersona):
    try:
        db = con.conectar()
        cursor = db.cursor()
        sql = "DELETE FROM personas WHERE id = ?"
        cursor.execute(sql, (idPersona,))
        eliminada = cursor.rowcount > 0
        db.commit()
        if eliminada:
            return {"respuesta": eliminada, "mensaje": "Persona eliminada"}
        else:
            return {"respuesta": eliminada, "mensaje": "No existe la persona con ese id"}
    except Exception as ex:
        return {"respuesta": False, "mensaje": str(ex)}
    finally:
        cursor.close()
        db.close()