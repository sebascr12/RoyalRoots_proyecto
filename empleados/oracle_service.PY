from royalroots.init_oracle import get_connection
import cx_Oracle
from datetime import datetime
from datetime import datetime, date, time


def obtener_funciones_disponibles():
    conn = get_connection()
    cur = conn.cursor()
    try:
        resultado = cur.var(cx_Oracle.CURSOR)
        cur.callproc("FIDE_EMPLEADOS_FUNCION_TB_LISTAR_SP", [resultado])
        return [row[0] for row in resultado.getvalue()]
    except Exception as e:
        print("Error al obtener funciones:", e)
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
        print("Error al obtener estados:", e)
        return []
    finally:
        cur.close()
        conn.close()


def obtener_turnos_disponibles():
    conn = get_connection()
    cur = conn.cursor()
    try:
        resultado = cur.var(cx_Oracle.CURSOR)
        cur.callproc("FIDE_TURNOS_TB_LISTAR_TURNOS_SP", [resultado])
        return [(row[0], row[1]) for row in resultado.getvalue()]  # lista de tuplas (inicio, fin)
    except Exception as e:
        print("Error al obtener turnos:", e)
        return []
    finally:
        cur.close()
        conn.close()


def insertar_empleado(nombre, apellido, correo, telefono, fecha, salario, funcion, turno_inicio, turno_fin, estado):
    conn = get_connection()
    cur = conn.cursor()
    try:
        # Fecha de contratación como datetime (sin hora)
        if isinstance(fecha, str):
            fecha = datetime.strptime(fecha, "%Y-%m-%d")
        elif isinstance(fecha, date) and not isinstance(fecha, datetime):
            fecha = datetime.combine(fecha, time(0, 0))

        # Turno inicio y fin como datetime completo (TIMESTAMP)
        if isinstance(turno_inicio, str):
            turno_inicio = datetime.combine(date.today(), datetime.strptime(turno_inicio, "%H:%M").time())
        if isinstance(turno_fin, str):
            turno_fin = datetime.combine(date.today(), datetime.strptime(turno_fin, "%H:%M").time())

        cur.callproc("FIDE_EMPLEADOS_TB_INSERTAR_EMPLEADO_SP", [
            nombre,
            apellido,
            correo,
            telefono,
            fecha,
            salario,
            funcion,
            turno_inicio,
            turno_fin,
            estado
        ])
        conn.commit()
        return True
    except Exception as e:
        print("Error al insertar empleado:", e)
        return False
    finally:
        cur.close()
        conn.close()



def listar_empleados():
    conn = get_connection()
    cur = conn.cursor()
    try:
        resultado = cur.var(cx_Oracle.CURSOR)
        cur.callproc("FIDE_EMPLEADOS_TB_LISTAR_EMPLEADOS_SP", [resultado])
        empleados_cursor = resultado.getvalue()
        empleados = []
        for row in empleados_cursor:
            empleados.append({
                'id': row[0],
                'nombre_completo': row[1],
                'funcion': row[2],
                'estado': row[3]
            })
        return empleados
    except Exception as e:
        print("Error al listar empleados:", e)
        return []
    finally:
        cur.close()
        conn.close()


def inactivar_empleado(correo):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.callproc("FIDE_EMPLEADOS_TB_ELIMINAR_EMPLEADO_SP", [correo])
        conn.commit()
        return True
    except Exception as e:
        print("Error al inactivar empleado:", e)
        return False
    finally:
        cur.close()
        conn.close()


def actualizar_empleado(nombre, apellido, correo, telefono, fecha, salario, funcion, turno_inicio, turno_fin, estado):
    conn = get_connection()
    cur = conn.cursor()
    try:
        if isinstance(fecha, date):
            fecha = datetime.combine(fecha, time.min)

        if isinstance(turno_inicio, str):
            turno_inicio = datetime.strptime(turno_inicio, "%H:%M").time()
        if isinstance(turno_fin, str):
            turno_fin = datetime.strptime(turno_fin, "%H:%M").time()

        dummy_date = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
        inicio_ts = datetime.combine(dummy_date.date(), turno_inicio)
        fin_ts = datetime.combine(dummy_date.date(), turno_fin)

        cur.callproc("FIDE_EMPLEADOS_TB_ACTUALIZAR_EMPLEADO_SP", [
            nombre, apellido, correo, telefono,
            fecha, salario,
            funcion, inicio_ts, fin_ts, estado
        ])
        conn.commit()
        return True
    except Exception as e:
        print("Error al actualizar empleado:", e)
        return False
    finally:
        cur.close()
        conn.close()


# Listar empleados
def listar_empleados():
    conn = get_connection()
    cur = conn.cursor()
    try:
        resultado = cur.var(cx_Oracle.CURSOR)
        cur.callproc("FIDE_EMPLEADOS_TB_LISTAR_EMPLEADOS_SP", [resultado])
        empleados_cursor = resultado.getvalue()
        empleados = []
        for row in empleados_cursor:
            empleados.append({
                'id': row[0],
                'nombre': row[1],
                'apellido': row[2],
                'funcion': row[3],
                'estado': row[4],
                'correo': row[5],
                'telefono': row[6],
                'fecha_contratacion': row[7],
                'salario': row[8],
                'hora_inicio': row[9],
                'hora_fin': row[10]
            })
        return empleados
    except Exception as e:
        print("Error al listar empleados:", e)
        return []
    finally:
        cur.close()
        conn.close()

# Inactivar empleado
def inactivar_empleado(correo):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.callproc("FIDE_EMPLEADOS_TB_ELIMINAR_EMPLEADO_SP", [correo])
        conn.commit()
        return True
    except Exception as e:
        print("Error al inactivar empleado:", e)
        return False
    finally:
        cur.close()
        conn.close()

# Actualizar empleado
def actualizar_empleado(nombre, apellido, correo, telefono, fecha, salario, funcion, turno_inicio, turno_fin, estado):
    conn = get_connection()
    cur = conn.cursor()
    try:
        fecha_formateada = fecha if isinstance(fecha, datetime) else datetime.strptime(fecha, "%Y-%m-%d")

        dummy_date = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
        inicio = datetime.combine(dummy_date.date(), datetime.strptime(turno_inicio, "%H:%M").time())
        fin = datetime.combine(dummy_date.date(), datetime.strptime(turno_fin, "%H:%M").time())

        cur.callproc("FIDE_EMPLEADOS_TB_ACTUALIZAR_EMPLEADO_SP", [
            nombre, apellido, correo, telefono,
            fecha_formateada, salario,
            funcion, inicio, fin, estado
        ])
        conn.commit()
        return True
    except Exception as e:
        print("Error al actualizar empleado:", e)
        return False
    finally:
        cur.close()
        conn.close()

#turnos

def insertar_turno(hora_inicio, hora_fin, estado):
    conn = get_connection()
    cur = conn.cursor()
    try:
        # Convertir hora_inicio y hora_fin a datetime con fecha dummy
        dummy_date = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
        inicio_dt = datetime.combine(dummy_date.date(), datetime.strptime(hora_inicio, "%H:%M").time())
        fin_dt = datetime.combine(dummy_date.date(), datetime.strptime(hora_fin, "%H:%M").time())

        cur.callproc("FIDE_TURNOS_TB_INSERTAR_TURNO_SP", [
            inicio_dt,
            fin_dt,
            estado
        ])
        conn.commit()
        return True
    except Exception as e:
        print("Error al insertar turno:", e)
        return False
    finally:
        cur.close()
        conn.close()

def listar_turnos():
    conn = get_connection()
    cur = conn.cursor()
    try:
        resultado = cur.var(cx_Oracle.CURSOR)
        cur.callproc("FIDE_TURNOS_TB_LISTAR_TURNOS_SP", [resultado])
        turnos_cursor = resultado.getvalue()
        turnos = []
        for row in turnos_cursor:
            turnos.append({
                'hora_inicio': row[0],
                'hora_fin': row[1],
                'estado': row[2],
            })
        return turnos
    except Exception as e:
        print("Error al listar turnos:", e)
        return []
    finally:
        cur.close()
        conn.close()

def actualizar_turno(hora_inicio, hora_fin, nueva_hora_inicio, nueva_hora_fin, estado):
    conn = get_connection()
    cur = conn.cursor()
    try:
        # Crear una fecha dummy para componer los TIMESTAMP
        dummy_date = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)

        hora_inicio_dt = datetime.combine(dummy_date.date(), datetime.strptime(hora_inicio, "%H:%M").time())
        hora_fin_dt = datetime.combine(dummy_date.date(), datetime.strptime(hora_fin, "%H:%M").time())
        nueva_inicio_dt = datetime.combine(dummy_date.date(), datetime.strptime(nueva_hora_inicio, "%H:%M").time())
        nueva_fin_dt = datetime.combine(dummy_date.date(), datetime.strptime(nueva_hora_fin, "%H:%M").time())

        # Llamada al procedimiento almacenado
        cur.callproc("FIDE_TURNOS_TB_ACTUALIZAR_TURNO_SP", [
            hora_inicio_dt,
            hora_fin_dt,
            nueva_inicio_dt,
            nueva_fin_dt,
            estado
        ])
        conn.commit()
        return True
    except Exception as e:
        print("Error al actualizar turno:", e)
        return False
    finally:
        cur.close()
        conn.close()

def eliminar_turno(hora_inicio, hora_fin):
    conn = get_connection()
    cur = conn.cursor()
    try:
        dummy_date = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
        inicio_dt = datetime.combine(dummy_date.date(), datetime.strptime(hora_inicio, "%H:%M").time())
        fin_dt = datetime.combine(dummy_date.date(), datetime.strptime(hora_fin, "%H:%M").time())

        cur.callproc("FIDE_TURNOS_TB_ELIMINAR_TURNO_SP", [
            inicio_dt,
            fin_dt
        ])
        conn.commit()
        return True
    except Exception as e:
        print("Error al eliminar turno:", e)
        return False
    finally:
        cur.close()
        conn.close()


##funciones de empleados

def insertar_funcion(nombre_funcion, descripcion, estado):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.callproc("FIDE_EMPLEADOS_FUNCION_TB_INSERTAR_SP", [
            nombre_funcion,
            descripcion,
            estado
        ])
        conn.commit()
        return True
    except Exception as e:
        print("Error al insertar función:", e)
        return False
    finally:
        cur.close()
        conn.close()


def listar_funciones():
    conn = get_connection()
    cur = conn.cursor()
    try:
        resultado = cur.var(cx_Oracle.CURSOR)
        cur.callproc("FIDE_EMPLEADOS_FUNCION_TB_LISTAR_SP", [resultado])
        funciones_cursor = resultado.getvalue()
        funciones = []
        for row in funciones_cursor:
            funciones.append({
                'nombre_funcion': row[0],
                'descripcion': row[1],
                'estado': row[2],
            })
        return funciones
    except Exception as e:
        print("Error al listar funciones:", e)
        return []
    finally:
        cur.close()
        conn.close()


def actualizar_funcion(nombre_funcion_actual, nuevo_nombre, nueva_descripcion, nuevo_estado):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.callproc("FIDE_EMPLEADOS_FUNCION_TB_ACTUALIZAR_SP", [
            nombre_funcion_actual,
            nuevo_nombre,
            nueva_descripcion,
            nuevo_estado
        ])
        conn.commit()
        return True
    except Exception as e:
        print("Error al actualizar función:", e)
        return False
    finally:
        cur.close()
        conn.close()


def inactivar_funcion(nombre_funcion):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.callproc("FIDE_EMPLEADOS_FUNCION_TB_INACTIVAR_SP", [nombre_funcion])
        conn.commit()
        return True
    except Exception as e:
        print("Error al inactivar función:", e)
        return False
    finally:
        cur.close()
        conn.close()