from royalroots.init_oracle import get_connection
import cx_Oracle

def insertar_servicio(nombre, descripcion, precio, estado):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.callproc("FIDE_SERVICIOS_TB_INSERTAR_SP", [
            nombre,
            descripcion,
            precio,
            estado
        ])
        conn.commit()
        return True
    except Exception as e:
        print("Error al insertar servicio:", e)
        return False
    finally:
        cur.close()
        conn.close()

def listar_servicios():
    conn = get_connection()
    cur = conn.cursor()
    try:
        resultado = cur.var(cx_Oracle.CURSOR)
        cur.callproc("FIDE_SERVICIOS_TB_LISTAR_SP", [resultado])
        cursor = resultado.getvalue()
        servicios = []
        for row in cursor:
            servicios.append({
                'nombre': row[0],
                'descripcion': row[1],
                'precio': row[2],
                'estado': row[3],
            })
        return servicios
    except Exception as e:
        print("Error al listar servicios:", e)
        return []
    finally:
        cur.close()
        conn.close()

def actualizar_servicio(nombre_actual, nuevo_nombre, descripcion, precio, estado):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.callproc("FIDE_SERVICIOS_TB_ACTUALIZAR_SP", [
            nombre_actual,
            nuevo_nombre,
            descripcion,
            precio,
            estado
        ])
        conn.commit()
        return True
    except Exception as e:
        print("Error al actualizar servicio:", e)
        return False
    finally:
        cur.close()
        conn.close()

def inactivar_servicio(nombre_servicio):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.callproc("FIDE_SERVICIOS_TB_INACTIVAR_SP", [nombre_servicio])
        conn.commit()
        return True
    except Exception as e:
        print("Error al inactivar servicio:", e)
        return False
    finally:
        cur.close()
        conn.close()


##beneficios del cliente
def insertar_beneficio(detalle_beneficio, nombre_servicio, estado_desc):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.callproc("FIDE_BENEFICIO_TB_INSERTAR_SP", [
            detalle_beneficio,
            nombre_servicio,
            estado_desc
        ])
        conn.commit()
        return True
    except Exception as e:
        print("Error al insertar beneficio:", e)
        return False
    finally:
        cur.close()
        conn.close()

def listar_beneficios():
    conn = get_connection()
    cur = conn.cursor()
    try:
        resultado = cur.var(cx_Oracle.CURSOR)
        cur.callproc("FIDE_BENEFICIO_TB_LISTAR_SP", [resultado])
        cursor = resultado.getvalue()
        beneficios = []
        for row in cursor:
            beneficios.append({
                'detalle': row[0],
                'servicio': row[1],
                'estado': row[2]
            })
        return beneficios
    except Exception as e:
        print("Error al listar beneficios:", e)
        return []
    finally:
        cur.close()
        conn.close()

def actualizar_beneficio(detalle_actual, nuevo_detalle, nuevo_servicio, nuevo_estado):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.callproc("FIDE_BENEFICIO_TB_ACTUALIZAR_SP", [
            detalle_actual,
            nuevo_detalle,
            nuevo_servicio,
            nuevo_estado
        ])
        conn.commit()
        return True
    except Exception as e:
        print("Error al actualizar beneficio:", e)
        return False
    finally:
        cur.close()
        conn.close()

def inactivar_beneficio(detalle_beneficio):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.callproc("FIDE_BENEFICIO_TB_INACTIVAR_SP", [detalle_beneficio])
        conn.commit()
        return True
    except Exception as e:
        print("Error al inactivar beneficio:", e)
        return False
    finally:
        cur.close()
        conn.close()

def obtener_servicios_disponibles():
    conn = get_connection()
    cur = conn.cursor()
    try:
        resultado = cur.var(cx_Oracle.CURSOR)
        cur.callproc("FIDE_SERVICIOS_TB_LISTAR_SP", [resultado])
        return [row[0] for row in resultado.getvalue()]
    except Exception as e:
        print("Error al obtener servicios disponibles:", e)
        return []
    finally:
        cur.close()
        conn.close()

def obtener_estados_disponibles():
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT DESCRIPCION FROM FIDE_ESTADO_TB WHERE DESCRIPCION IN ('ACTIVO', 'INACTIVO')")
        return [row[0] for row in cur.fetchall()]
    except Exception as e:
        print("Error al obtener estados disponibles:", e)
        return []
    finally:
        cur.close()
        conn.close()

##clientes

# UTILIDAD: obtener lista desde función SYS_REFCURSOR
def obtener_lista_cursor(funcion_sql):
    conn = get_connection()
    cur = conn.cursor()
    try:
        resultado = cur.var(cx_Oracle.CURSOR)
        cur.execute(f"BEGIN :1 := {funcion_sql}(); END;", [resultado])
        return [row[0] for row in resultado.getvalue()]
    except Exception as e:
        print(f"Error al ejecutar {funcion_sql}:", e)
        return []
    finally:
        cur.close()
        conn.close()


# FUNCIONES AUXILIARES
def obtener_provincias_disponibles():
    return obtener_lista_cursor("FIDE_PROVINCIA_TB_LISTAR_ACTIVAS_FN")

def obtener_cantones_disponibles():
    return obtener_lista_cursor("FIDE_CANTON_TB_LISTAR_ACTIVOS_FN")

def obtener_distritos_disponibles():
    return obtener_lista_cursor("FIDE_DISTRITO_TB_LISTAR_ACTIVOS_FN")

def obtener_direcciones_disponibles():
    return obtener_lista_cursor("FIDE_DIRECCION_TB_LISTAR_COMO_DESCRIPCION_FN")

def obtener_estados_disponibles():
    return obtener_lista_cursor("FIDE_ESTADO_TB_LISTAR_ESTADOS_FN")


def listar_clientes():
    conn = get_connection()
    cur = conn.cursor()
    try:
        resultado = cur.var(cx_Oracle.CURSOR)
        cur.callproc("FIDE_CLIENTES_TB_LISTAR_SP", [resultado])
        clientes = []
        for row in resultado.getvalue():
            clientes.append({
                'id_cliente': row[0],
                'nombre': row[1],
                'telefono': row[2],
                'correo': row[3],
                'fecha_registro': row[4],
                'direccion': row[5],
                'estado': row[6]
            })
        return clientes
    except Exception as e:
        print("Error al listar clientes:", e)
        return []
    finally:
        cur.close()
        conn.close()


def insertar_cliente(nombre, telefono, correo, fecha, direccion_desc, estado_desc):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.callproc("FIDE_CLIENTES_TB_INSERTAR_SP", [
            nombre, telefono, correo, fecha, direccion_desc, estado_desc
        ])
        conn.commit()
        return True
    except Exception as e:
        print("Error al insertar cliente:", e)
        return False
    finally:
        cur.close()
        conn.close()


def actualizar_cliente(id_cliente, nombre, telefono, correo, fecha, direccion_desc, estado_desc):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.callproc("FIDE_CLIENTES_TB_ACTUALIZAR_SP", [
            id_cliente, nombre, telefono, correo, fecha, direccion_desc, estado_desc
        ])
        conn.commit()
        return True
    except Exception as e:
        print("Error al actualizar cliente:", e)
        return False
    finally:
        cur.close()
        conn.close()


def inactivar_cliente(id_cliente):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.callproc("FIDE_CLIENTES_TB_INACTIVAR_SP", [id_cliente])
        conn.commit()
        return True
    except Exception as e:
        print("Error al inactivar cliente:", e)
        return False
    finally:
        cur.close()
        conn.close()

def generar_direcciones_disponibles():
    provincias = obtener_provincias_disponibles()
    cantones = obtener_cantones_disponibles()
    distritos = obtener_distritos_disponibles()
    
    direcciones = []
    for p in provincias:
        for c in cantones:
            for d in distritos:
                direccion = f"{p} - {c} - {d}"
                direcciones.append(direccion)  # solo una vez, sin tupla duplicada
    return direcciones
