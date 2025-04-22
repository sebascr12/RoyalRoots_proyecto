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
        print("Error al obtener estados:", e)
        return []
    finally:
        cur.close()
        conn.close()

def listar_productos():
    conn = get_connection()
    cur = conn.cursor()
    try:
        resultado = cur.var(cx_Oracle.CURSOR)
        cur.callproc("FIDE_PRODUCTO_TB_LISTAR_SP", [resultado])
        productos = []
        for row in resultado.getvalue():
            productos.append({
                'id': row[0],
                'nombre': row[1],
                'descripcion': row[2],
                'precio': row[3],
                'estado': row[4]
            })
        return productos
    except Exception as e:
        print("Error al listar productos:", e)
        return []
    finally:
        cur.close()
        conn.close()

def insertar_producto(nombre, descripcion, precio, estado):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.callproc("FIDE_PRODUCTO_TB_INSERTAR_SP", [
            nombre.upper(), descripcion.upper(), precio, estado.upper()
        ])
        conn.commit()
        return True
    except Exception as e:
        print("Error al insertar producto:", e)
        return False
    finally:
        cur.close()
        conn.close()

def actualizar_producto(id_producto, nuevo_nombre, nueva_descripcion, nuevo_precio, nuevo_estado):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.callproc("FIDE_PRODUCTO_TB_ACTUALIZAR_SP", [
            id_producto, nuevo_nombre.upper(), nueva_descripcion.upper(), nuevo_precio, nuevo_estado.upper()
        ])
        conn.commit()
        return True
    except Exception as e:
        print("Error al actualizar producto:", e)
        return False
    finally:
        cur.close()
        conn.close()

def inactivar_producto(id_producto):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.callproc("FIDE_PRODUCTO_TB_INACTIVAR_SP", [id_producto])
        conn.commit()
        return True
    except Exception as e:
        print("Error al inactivar producto:", e)
        return False
    finally:
        cur.close()
        conn.close()

##inventario

def listar_inventario():
    conn = get_connection()
    cur = conn.cursor()
    try:
        resultado = cur.var(cx_Oracle.CURSOR)
        cur.callproc("FIDE_INVENTARIO_TB_LISTAR_SP", [resultado])
        inventario = []
        for row in resultado.getvalue():
            inventario.append({
                'id': row[0],
                'cantidad': row[1],
                'fecha_actualizacion': row[2],
                'producto': row[3],
                'estado': row[4]
            })
        return inventario
    except Exception as e:
        print("Error al listar inventario:", e)
        return []
    finally:
        cur.close()
        conn.close()


def insertar_inventario(nombre_producto, cantidad, fecha_actualizacion, estado):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.callproc("FIDE_INVENTARIO_TB_INSERTAR_SP", [
            nombre_producto.upper(), cantidad, fecha_actualizacion.strftime('%d/%m/%Y'), estado.upper()
        ])
        conn.commit()
        return True
    except Exception as e:
        print("Error al insertar inventario:", e)
        return False
    finally:
        cur.close()
        conn.close()


def actualizar_inventario(id_inventario, nombre_producto, cantidad, fecha_actualizacion, estado):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.callproc("FIDE_INVENTARIO_TB_ACTUALIZAR_SP", [
            id_inventario, nombre_producto.upper(), cantidad, fecha_actualizacion.strftime('%d/%m/%Y'), estado.upper()
        ])
        conn.commit()
        return True
    except Exception as e:
        print("Error al actualizar inventario:", e)
        return False
    finally:
        cur.close()
        conn.close()


def inactivar_inventario(id_inventario):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.callproc("FIDE_INVENTARIO_TB_INACTIVAR_SP", [id_inventario])
        conn.commit()
        return True
    except Exception as e:
        print("Error al inactivar inventario:", e)
        return False
    finally:
        cur.close()
        conn.close()


def obtener_nombres_productos():
    conn = get_connection()
    cur = conn.cursor()
    try:
        resultado = cur.var(cx_Oracle.CURSOR)
        cur.callproc("FIDE_PRODUCTO_TB_LISTAR_NOMBRES_SP", [resultado])
        return [row[0] for row in resultado.getvalue()]
    except Exception as e:
        print("Error al obtener nombres de productos:", e)
        return []
    finally:
        cur.close()
        conn.close()

#provedores
def obtener_estados_disponibles():
    conn = get_connection()
    cur = conn.cursor()
    try:
        resultado = cur.var(cx_Oracle.CURSOR)
        cur.callproc("FIDE_ESTADO_TB_LISTAR_ESTADOS_SP", [resultado])
        return [row[0] for row in resultado.getvalue()]
    except Exception as e:
        print("Error al obtener estados:", e)
        return []
    finally:
        cur.close()
        conn.close()

def listar_proveedores():
    conn = get_connection()
    cur = conn.cursor()
    try:
        resultado = cur.var(cx_Oracle.CURSOR)
        cur.callproc("FIDE_PROVEEDOR_TB_LISTAR_SP", [resultado])
        proveedores = []
        for row in resultado.getvalue():
            proveedores.append({
                'id': row[0],
                'nombre': row[1],
                'contacto': row[2],
                'tipo': row[3],
                'estado': row[4]
            })
        return proveedores
    except Exception as e:
        print("Error al listar proveedores:", e)
        return []
    finally:
        cur.close()
        conn.close()

def insertar_proveedor(nombre, contacto, tipo, estado):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.callproc("FIDE_PROVEEDOR_TB_INSERTAR_SP", [
            nombre.upper(), contacto.upper(), tipo.upper(), estado.upper()
        ])
        conn.commit()
        return True
    except Exception as e:
        print("Error al insertar proveedor:", e)
        return False
    finally:
        cur.close()
        conn.close()

def actualizar_proveedor(id_proveedor, nuevo_nombre, nuevo_contacto, nuevo_tipo, nuevo_estado):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.callproc("FIDE_PROVEEDOR_TB_ACTUALIZAR_SP", [
            id_proveedor, nuevo_nombre.upper(), nuevo_contacto.upper(), nuevo_tipo.upper(), nuevo_estado.upper()
        ])
        conn.commit()
        return True
    except Exception as e:
        print("Error al actualizar proveedor:", e)
        return False
    finally:
        cur.close()
        conn.close()

def inactivar_proveedor(id_proveedor):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.callproc("FIDE_PROVEEDOR_TB_INACTIVAR_SP", [id_proveedor])
        conn.commit()
        return True
    except Exception as e:
        print("Error al inactivar proveedor:", e)
        return False
    finally:
        cur.close()
        conn.close()

#ordenes compra
def obtener_estados_disponibles():
    conn = get_connection()
    cur = conn.cursor()
    try:
        resultado = cur.var(cx_Oracle.CURSOR)
        cur.callproc("FIDE_ESTADO_TB_LISTAR_ESTADOS_SP", [resultado])
        return [row[0] for row in resultado.getvalue()]
    except Exception as e:
        print("Error al obtener estados:", e)
        return []
    finally:
        cur.close()
        conn.close()

def obtener_nombres_proveedores():
    conn = get_connection()
    cur = conn.cursor()
    try:
        resultado = cur.var(cx_Oracle.CURSOR)
        cur.callproc("FIDE_PROVEEDOR_TB_LISTAR_NOMBRES_SP", [resultado])
        return [row[0] for row in resultado.getvalue()]
    except Exception as e:
        print("Error al obtener nombres de proveedores:", e)
        return []
    finally:
        cur.close()
        conn.close()

def listar_ordenes_compra():
    conn = get_connection()
    cur = conn.cursor()
    try:
        resultado = cur.var(cx_Oracle.CURSOR)
        cur.callproc("FIDE_ORDENES_COMPRA_TB_LISTAR_SP", [resultado])
        ordenes = []
        for row in resultado.getvalue():
            ordenes.append({
                'id': row[0],
                'proveedor': row[1],
                'fecha': row[2],
                'total': row[3],
                'estado': row[4]
            })
        return ordenes
    except Exception as e:
        print("Error al listar órdenes de compra:", e)
        return []
    finally:
        cur.close()
        conn.close()

def insertar_orden_compra(nombre_proveedor, fecha, total, estado):
    conn = get_connection()
    cur = conn.cursor()
    try:
        fecha_formato = fecha.strftime("%d/%m/%Y")
        cur.callproc("FIDE_ORDENES_COMPRA_TB_INSERTAR_SP", [
            nombre_proveedor.upper(), fecha_formato, float(total), estado.upper()
        ])
        conn.commit()
        return True
    except Exception as e:
        print("Error al insertar orden de compra:", e)
        return False
    finally:
        cur.close()
        conn.close()

def actualizar_orden_compra(id_orden, proveedor, fecha, total, estado):
    conn = get_connection()
    cur = conn.cursor()
    try:
        fecha_formato = fecha.strftime("%d/%m/%Y")
        cur.callproc("FIDE_ORDENES_COMPRA_TB_ACTUALIZAR_SP", [
            id_orden, proveedor.upper(), fecha_formato, float(total), estado.upper()
        ])
        conn.commit()
        return True
    except Exception as e:
        print("Error al actualizar orden:", e)
        return False
    finally:
        cur.close()
        conn.close()

def inactivar_orden_compra(id_orden):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.callproc("FIDE_ORDENES_COMPRA_TB_INACTIVAR_SP", [id_orden])
        conn.commit()
        return True
    except Exception as e:
        print("Error al inactivar orden:", e)
        return False
    finally:
        cur.close()
        conn.close()