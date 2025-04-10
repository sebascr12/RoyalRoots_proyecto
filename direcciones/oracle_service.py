from royalroots.init_oracle import get_connection
import cx_Oracle

# PROVINCIAS
def listar_provincias():
    conn = get_connection()
    cur = conn.cursor()
    try:
        resultado = cur.var(cx_Oracle.CURSOR)
        cur.callproc("FIDE_PROVINCIA_TB_LISTAR_PROVINCIAS_SP", [resultado])
        provincias = []
        for row in resultado.getvalue():
            provincias.append({
                'provincia': row[0],
                'estado': row[1]
            })
        return provincias
    except Exception as e:
        print("Error al listar provincias:", e)
        return []
    finally:
        cur.close()
        conn.close()

def insertar_provincia(nombre_provincia, estado_descripcion):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.callproc('FIDE_PROVINCIA_TB_INSERTAR_PROVINCIA_SP', [
            nombre_provincia.upper(),
            estado_descripcion.upper()
        ])
        conn.commit()
        return True
    except Exception as e:
        print("Error al insertar provincia:", e)
        return False
    finally:
        cur.close()
        conn.close()

def actualizar_provincia(nombre_actual, nuevo_nombre, nuevo_estado):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.callproc("FIDE_PROVINCIA_TB_ACTUALIZAR_PROVINCIA_SP", [
            nombre_actual.upper(),
            nuevo_nombre.upper(),
            nuevo_estado.upper()
        ])
        conn.commit()
        return True
    except Exception as e:
        print("Error actualizando provincia:", e)
        return False
    finally:
        cur.close()
        conn.close()

def inactivar_provincia(nombre_provincia):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.callproc("FIDE_PROVINCIA_TB_INACTIVAR_PROVINCIA_SP", [nombre_provincia.upper()])
        conn.commit()
        return True
    except Exception as e:
        print("Error inactivando provincia:", e)
        return False
    finally:
        cur.close()
        conn.close()

# CANTONES
def insertar_canton(nombre_canton, provincia_nombre, estado_desc):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.callproc('FIDE_CANTON_TB_INSERTAR_SP', [
            nombre_canton.upper(),
            provincia_nombre.upper(),
            estado_desc.upper()
        ])
        conn.commit()
        return True
    except Exception as e:
        print("Error al insertar cantón:", e)
        return False
    finally:
        cur.close()
        conn.close()

def listar_cantones():
    conn = get_connection()
    cur = conn.cursor()
    try:
        resultado = cur.var(cx_Oracle.CURSOR)
        cur.callproc("FIDE_CANTON_TB_LISTAR_SP", [resultado])
        datos = resultado.getvalue().fetchall()
        return [{'canton': fila[0], 'provincia': fila[1], 'estado': fila[2]} for fila in datos]
    finally:
        cur.close()
        conn.close()

def actualizar_canton(nombre_actual, nuevo_nombre, provincia_nombre, estado_desc):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.callproc("FIDE_CANTON_TB_ACTUALIZAR_SP", [
            nombre_actual.upper(),
            nuevo_nombre.upper(),
            provincia_nombre.upper(),
            estado_desc.upper()
        ])
        conn.commit()
        return True
    except Exception as e:
        print("Error al actualizar cantón:", e)
        return False
    finally:
        cur.close()
        conn.close()

def inactivar_canton(nombre_canton):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.callproc("FIDE_CANTON_TB_INACTIVAR_SP", [nombre_canton.upper()])
        conn.commit()
        return True
    except Exception as e:
        print("Error al inactivar cantón:", e)
        return False
    finally:
        cur.close()
        conn.close()

# DISTRITOS
def insertar_distrito(nombre_distrito, nombre_canton, estado_desc):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.callproc('FIDE_DISTRITO_TB_INSERTAR_SP', [
            nombre_distrito.upper(),
            nombre_canton.upper(),
            estado_desc.upper()
        ])
        conn.commit()
        return True
    except Exception as e:
        print("Error al insertar distrito:", e)
        return False
    finally:
        cur.close()
        conn.close()

def listar_distritos():
    conn = get_connection()
    cur = conn.cursor()
    try:
        resultado = cur.var(cx_Oracle.CURSOR)
        cur.callproc("FIDE_DISTRITO_TB_LISTAR_SP", [resultado])
        return [{'distrito': row[0], 'canton': row[1], 'estado': row[2]} for row in resultado.getvalue()]
    except Exception as e:
        print("Error al listar distritos:", e)
        return []
    finally:
        cur.close()
        conn.close()

def actualizar_distrito(nombre_actual, nuevo_nombre, nuevo_canton, nuevo_estado):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.callproc('FIDE_DISTRITO_TB_ACTUALIZAR_SP', [
            nombre_actual.upper(),
            nuevo_nombre.upper(),
            nuevo_canton.upper(),
            nuevo_estado.upper()
        ])
        conn.commit()
        return True
    except Exception as e:
        print("Error al actualizar distrito:", e)
        return False
    finally:
        cur.close()
        conn.close()

def inactivar_distrito(nombre_distrito):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.callproc("FIDE_DISTRITO_TB_INACTIVAR_SP", [nombre_distrito.upper()])
        conn.commit()
        return True
    except Exception as e:
        print("Error al inactivar distrito:", e)
        return False
    finally:
        cur.close()
        conn.close()

# FUNCIONES AUXILIARES
def obtener_id_provincia(nombre):
    return ejecutar_funcion_id("FIDE_PROVINCIA_TB_OBTENER_ID_PROVINCIA_FN", nombre)

def obtener_id_canton(nombre):
    return ejecutar_funcion_id("FIDE_CANTON_TB_OBTENER_ID_CANTON_FN", nombre)

def obtener_id_distrito(nombre):
    return ejecutar_funcion_id("FIDE_DISTRITO_TB_OBTENER_ID_DISTRITO_FN", nombre)

def obtener_id_estado(descripcion):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT ID_ESTADO FROM FIDE_ESTADO_TB WHERE UPPER(DESCRIPCION) = :1", [descripcion.upper()])
        return cur.fetchone()[0]
    except Exception as e:
        print("Error al obtener ID de estado:", e)
        return None
    finally:
        cur.close()
        conn.close()

def ejecutar_funcion_id(nombre_funcion, valor):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(f"SELECT {nombre_funcion}(:1) FROM DUAL", [valor.upper()])
        return cur.fetchone()[0]
    except Exception as e:
        print(f"Error ejecutando {nombre_funcion}:", e)
        return None
    finally:
        cur.close()
        conn.close()

# DIRECCIONES
def insertar_direccion(provincia, canton, distrito, estado):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.callproc("FIDE_DIRECCION_TB_INSERTAR_SP", [
            provincia.upper(),
            canton.upper(),
            distrito.upper(),
            estado.upper()
        ])
        conn.commit()
        return True
    except Exception as e:
        print("Error al insertar dirección:", e)
        return False
    finally:
        cur.close()
        conn.close()

def listar_direcciones():
    conn = get_connection()
    cur = conn.cursor()
    try:
        resultado = cur.var(cx_Oracle.CURSOR)
        cur.callproc("FIDE_DIRECCION_TB_LISTAR_SP", [resultado])
        direcciones = []
        for row in resultado.getvalue():
            direcciones.append({
                'id_direccion': row[0],  
                'provincia': row[1],
                'canton': row[2],
                'distrito': row[3],
                'estado': row[4]
            })
        return direcciones
    except Exception as e:
        print("Error al listar direcciones:", e)
        return []
    finally:
        cur.close()
        conn.close()
def actualizar_direccion(id_direccion, nueva_provincia, nuevo_canton, nuevo_distrito, nuevo_estado):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.callproc("FIDE_DIRECCION_TB_ACTUALIZAR_SP", [
            id_direccion,
            nueva_provincia.upper(),
            nuevo_canton.upper(),
            nuevo_distrito.upper(),
            nuevo_estado.upper()
        ])
        conn.commit()
        return True
    except Exception as e:
        print("Error al actualizar dirección:", e)
        return False
    finally:
        cur.close()
        conn.close()

def inactivar_direccion(id_direccion):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.callproc("FIDE_DIRECCION_TB_INACTIVAR_SP", [id_direccion])
        conn.commit()
        return True
    except Exception as e:
        print("Error al inactivar dirección:", e)
        return False
    finally:
        cur.close()
        conn.close()

# LISTAR OPCIONES DISPONIBLES
def obtener_provincias_disponibles():
    return obtener_lista_cursor("FIDE_PROVINCIA_TB_LISTAR_ACTIVAS_FN")

def obtener_cantones_disponibles():
    return obtener_lista_cursor("FIDE_CANTON_TB_LISTAR_ACTIVOS_FN")

def obtener_distritos_disponibles():
    return obtener_lista_cursor("FIDE_DISTRITO_TB_LISTAR_ACTIVOS_FN")

def obtener_lista_cursor(nombre_funcion):
    conn = get_connection()
    cur = conn.cursor()
    try:
        resultado = cur.var(cx_Oracle.CURSOR)
        cur.execute(f"BEGIN :1 := {nombre_funcion}(); END;", [resultado])
        return [row[0] for row in resultado.getvalue()]
    except Exception as e:
        print(f"Error al obtener lista de {nombre_funcion}:", e)
        return []
    finally:
        cur.close()
        conn.close()

        
def obtener_estados_disponibles():
    conn = get_connection()
    cur = conn.cursor()
    try:
        resultado = cur.var(cx_Oracle.CURSOR)
        cur.callproc("FIDE_ESTADO_TB_LISTAR_ESTADOS_SP", [resultado])
        return [row[0] for row in resultado.getvalue()]
    except Exception as e:
        print("Error al obtener estados disponibles:", e)
        return []
    finally:
        cur.close()
        conn.close()

