from royalroots.init_oracle import get_connection
import cx_Oracle

def listar_metodos_pago():
    conn = get_connection()
    cur = conn.cursor()
    try:
        resultado = cur.var(cx_Oracle.CURSOR)
        cur.callproc("FIDE_METODO_PAGO_TB_LISTAR_SP", [resultado])
        metodos = []
        for row in resultado.getvalue():
            metodos.append({
                'id': row[0],
                'nombre': row[1],
                'estado': row[2]
            })
        return metodos
    except Exception as e:
        print("Error al listar métodos de pago:", e)
        return []
    finally:
        cur.close()
        conn.close()

def insertar_metodo_pago(nombre, estado):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.callproc("FIDE_METODO_PAGO_TB_INSERTAR_SP", [nombre.upper(), estado.upper()])
        conn.commit()
        return True
    except Exception as e:
        print("Error al insertar método de pago:", e)
        return False
    finally:
        cur.close()
        conn.close()

def actualizar_metodo_pago(id_metodo, nuevo_nombre, nuevo_estado):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.callproc("FIDE_METODO_PAGO_TB_ACTUALIZAR_SP", [id_metodo, nuevo_nombre.upper(), nuevo_estado.upper()])
        conn.commit()
        return True
    except Exception as e:
        print("Error al actualizar método de pago:", e)
        return False
    finally:
        cur.close()
        conn.close()

def inactivar_metodo_pago(id_metodo):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.callproc("FIDE_METODO_PAGO_TB_INACTIVAR_SP", [id_metodo])
        conn.commit()
        return True
    except Exception as e:
        print("Error al inactivar método de pago:", e)
        return False
    finally:
        cur.close()
        conn.close()

def obtener_estados_disponibles():
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT DESCRIPCION FROM FIDE_ESTADO_TB WHERE UPPER(DESCRIPCION) IN ('ACTIVO', 'INACTIVO')")
        return [row[0] for row in cur.fetchall()]
    except Exception as e:
        print("Error al obtener estados disponibles:", e)
        return []
    finally:
        cur.close()
        conn.close()



#historial pago
from royalroots.init_oracle import get_connection
import cx_Oracle

def listar_historial_pagos():
    conn = get_connection()
    cur = conn.cursor()
    try:
        resultado = cur.var(cx_Oracle.CURSOR)
        cur.callproc("FIDE_HISTORIAL_PAGOS_TB_LISTAR_SP", [resultado])
        pagos = []
        for row in resultado.getvalue():
            pagos.append({
                'id': row[0],
                'cliente': row[1],
                'monto': row[2],
                'fecha': row[3],
                'estado': row[4]
            })
        return pagos
    except Exception as e:
        print("Error al listar historial de pagos:", e)
        return []
    finally:
        cur.close()
        conn.close()

def insertar_historial_pago(nombre_cliente, monto, fecha_pago, estado):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.callproc("FIDE_HISTORIAL_PAGOS_TB_INSERTAR_SP", [
            nombre_cliente.upper(),
            monto,
            fecha_pago,
            estado.upper()
        ])
        conn.commit()
        return True
    except Exception as e:
        print("Error al insertar historial de pago:", e)
        return False
    finally:
        cur.close()
        conn.close()

def actualizar_historial_pago(id_pago, monto, fecha_pago, estado):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.callproc("FIDE_HISTORIAL_PAGOS_TB_ACTUALIZAR_SP", [
            id_pago,
            monto,
            fecha_pago,
            estado.upper()
        ])
        conn.commit()
        return True
    except Exception as e:
        print("Error al actualizar historial de pago:", e)
        return False
    finally:
        cur.close()
        conn.close()

def inactivar_historial_pago(id_pago):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.callproc("FIDE_HISTORIAL_PAGOS_TB_INACTIVAR_SP", [id_pago])
        conn.commit()
        return True
    except Exception as e:
        print("Error al inactivar historial de pago:", e)
        return False
    finally:
        cur.close()
        conn.close()

def obtener_estados_disponibles():
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT DESCRIPCION FROM FIDE_ESTADO_TB WHERE UPPER(DESCRIPCION) IN ('ACTIVO', 'INACTIVO')")
        return [row[0] for row in cur.fetchall()]
    except Exception as e:
        print("Error al obtener estados:", e)
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
        print("Error al obtener clientes desde SP:", e)
        return []
    finally:
        cur.close()
        conn.close()

#facturas
def listar_facturas():
    conn = get_connection()
    cur = conn.cursor()
    try:
        resultado = cur.var(cx_Oracle.CURSOR)
        cur.callproc("FIDE_FACTURAS_TB_LISTAR_SP", [resultado])
        facturas = []
        for row in resultado.getvalue():
            facturas.append({
                'id': row[0],
                'cliente': row[1],
                'fecha': row[2],
                'total': row[3],
                'metodo_pago': row[4],
                'estado': row[5]
            })
        return facturas
    except Exception as e:
        print("Error al listar facturas:", e)
        return []
    finally:
        cur.close()
        conn.close()

def insertar_factura(nombre_cliente, metodo_pago, fecha_emision, total, estado):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.callproc("FIDE_FACTURAS_TB_INSERTAR_SP", [
            nombre_cliente.upper(),
            metodo_pago.upper(),
            fecha_emision,
            total,
            estado.upper()
        ])
        conn.commit()
        return True
    except Exception as e:
        print("Error al insertar factura:", e)
        return False
    finally:
        cur.close()
        conn.close()

def actualizar_factura(id_factura, total, fecha_emision, estado):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.callproc("FIDE_FACTURAS_TB_ACTUALIZAR_SP", [
            id_factura,
            total,
            fecha_emision,
            estado.upper()
        ])
        conn.commit()
        return True
    except Exception as e:
        print("Error al actualizar factura:", e)
        return False
    finally:
        cur.close()
        conn.close()

def inactivar_factura(id_factura):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.callproc("FIDE_FACTURAS_TB_INACTIVAR_SP", [id_factura])
        conn.commit()
        return True
    except Exception as e:
        print("Error al inactivar factura:", e)
        return False
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

def obtener_metodos_pago_disponibles():
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT NOMBRE_METODO FROM FIDE_METODO_PAGO_TB WHERE ID_ESTADO = FIDE_ESTADO_TB_OBTENER_ID_ESTADO_FN('ACTIVO')")
        return [row[0] for row in cur.fetchall()]
    except Exception as e:
        print("Error al obtener métodos de pago:", e)
        return []
    finally:
        cur.close()
        conn.close()

def obtener_estados_disponibles():
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT DESCRIPCION FROM FIDE_ESTADO_TB WHERE UPPER(DESCRIPCION) IN ('ACTIVO', 'INACTIVO')")
        return [row[0] for row in cur.fetchall()]
    except Exception as e:
        print("Error al obtener estados:", e)
        return []
    finally:
        cur.close()
        conn.close()

#detalle de facturas
def listar_detalles_factura():
    conn = get_connection()
    cur = conn.cursor()
    try:
        resultado = cur.var(cx_Oracle.CURSOR)
        cur.callproc("FIDE_DETALLE_FACTURAS_TB_LISTAR_SP", [resultado])
        detalles = []
        for row in resultado.getvalue():
            detalles.append({
                'id': row[0],
                'factura': row[1],
                'producto': row[2],
                'subtotal': row[3],
                'estado': row[4]
            })
        return detalles
    except Exception as e:
        print("Error al listar detalles de factura:", e)
        return []
    finally:
        cur.close()
        conn.close()

def insertar_detalle_factura(id_factura_str, nombre_producto, subtotal, estado):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.callproc("FIDE_DETALLE_FACTURAS_TB_INSERTAR_SP", [
            id_factura_str,
            nombre_producto.upper(),
            subtotal,
            estado.upper()
        ])
        conn.commit()
        return True
    except Exception as e:
        print("Error al insertar detalle de factura:", e)
        return False
    finally:
        cur.close()
        conn.close()

def actualizar_detalle_factura(id_detalle, subtotal, estado):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.callproc("FIDE_DETALLE_FACTURAS_TB_ACTUALIZAR_SP", [
            id_detalle,
            subtotal,
            estado.upper()
        ])
        conn.commit()
        return True
    except Exception as e:
        print("Error al actualizar detalle de factura:", e)
        return False
    finally:
        cur.close()
        conn.close()

def inactivar_detalle_factura(id_detalle):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.callproc("FIDE_DETALLE_FACTURAS_TB_INACTIVAR_SP", [id_detalle])
        conn.commit()
        return True
    except Exception as e:
        print("Error al inactivar detalle de factura:", e)
        return False
    finally:
        cur.close()
        conn.close()

def obtener_facturas_disponibles():
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT TO_CHAR(ID_FACTURA) FROM FIDE_FACTURAS_TB WHERE ID_ESTADO = FIDE_ESTADO_TB_OBTENER_ID_ESTADO_FN('ACTIVO')")
        return [row[0] for row in cur.fetchall()]
    except Exception as e:
        print("Error al obtener facturas:", e)
        return []
    finally:
        cur.close()
        conn.close()

def obtener_productos_disponibles():
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT NOMBRE_PRODUCTO FROM FIDE_PRODUCTO_TB WHERE ID_ESTADO = FIDE_ESTADO_TB_OBTENER_ID_ESTADO_FN('ACTIVO')")
        return [row[0] for row in cur.fetchall()]
    except Exception as e:
        print("Error al obtener productos:", e)
        return []
    finally:
        cur.close()
        conn.close()

def obtener_estados_disponibles():
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT DESCRIPCION FROM FIDE_ESTADO_TB WHERE UPPER(DESCRIPCION) IN ('ACTIVO', 'INACTIVO')")
        return [row[0] for row in cur.fetchall()]
    except Exception as e:
        print("Error al obtener estados:", e)
        return []
    finally:
        cur.close()
        conn.close()
