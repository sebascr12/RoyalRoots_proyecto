from royalroots.init_oracle import get_connection
import cx_Oracle

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

def obtener_clientes_disponibles():
    conn = get_connection()
    cur = conn.cursor()
    try:
        resultado = cur.var(cx_Oracle.CURSOR)
        cur.callproc("FIDE_CLIENTES_TB_LISTAR_NOMBRES_SP", [resultado])
        return [row[0] for row in resultado.getvalue()]
    except Exception as e:
        print("Error al obtener clientes:", e)
        return []
    finally:
        cur.close()
        conn.close()

def obtener_empleados_disponibles():
    conn = get_connection()
    cur = conn.cursor()
    try:
        resultado = cur.var(cx_Oracle.CURSOR)
        cur.callproc("FIDE_EMPLEADOS_TB_LISTAR_CORREOS_SP", [resultado])
        return [row[0] for row in resultado.getvalue()]
    except Exception as e:
        print("Error al obtener empleados:", e)
        return []
    finally:
        cur.close()
        conn.close()

def obtener_servicios_disponibles():
    conn = get_connection()
    cur = conn.cursor()
    try:
        resultado = cur.var(cx_Oracle.CURSOR)
        cur.callproc("FIDE_SERVICIOS_TB_LISTAR_NOMBRES_SP", [resultado])
        return [row[0] for row in resultado.getvalue()]
    except Exception as e:
        print("Error al obtener servicios:", e)
        return []
    finally:
        cur.close()
        conn.close()

def listar_reservas():
    conn = get_connection()
    cur = conn.cursor()
    try:
        resultado = cur.var(cx_Oracle.CURSOR)
        cur.callproc("FIDE_RESERVAS_TB_LISTAR_SP", [resultado])
        reservas = []
        for row in resultado.getvalue():
            reservas.append({
                'id_reserva': row[0],
                'cliente': row[1],
                'empleado': row[2],
                'servicio': row[3],
                'fecha_hora': row[4],
                'estado': row[5]
            })
        return reservas
    except Exception as e:
        print("Error al listar reservas:", e)
        return []
    finally:
        cur.close()
        conn.close()

def insertar_reserva(nombre_cliente, correo_empleado, nombre_servicio, fecha_hora, estado_desc):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.callproc("FIDE_RESERVAS_TB_INSERTAR_SP", [
            nombre_cliente, correo_empleado, nombre_servicio, fecha_hora, estado_desc
        ])
        conn.commit()
        return True
    except Exception as e:
        print("Error al insertar reserva:", e)
        return False
    finally:
        cur.close()
        conn.close()

def actualizar_reserva(id_reserva, nombre_cliente, correo_empleado, nombre_servicio, fecha_hora, estado_desc):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.callproc("FIDE_RESERVAS_TB_ACTUALIZAR_SP", [
            id_reserva, nombre_cliente, correo_empleado, nombre_servicio, fecha_hora, estado_desc
        ])
        conn.commit()
        return True
    except Exception as e:
        print("Error al actualizar reserva:", e)
        return False
    finally:
        cur.close()
        conn.close()

def inactivar_reserva(id_reserva):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.callproc("FIDE_RESERVAS_TB_INACTIVAR_SP", [id_reserva])
        conn.commit()
        return True
    except Exception as e:
        print("Error al inactivar reserva:", e)
        return False
    finally:
        cur.close()
        conn.close()
