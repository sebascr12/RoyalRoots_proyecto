from royalroots.init_oracle import get_connection
import cx_Oracle

def autenticar_usuario(usuario, clave):
    conn = get_connection()
    cur = conn.cursor()
    try:
        resultado = cur.var(cx_Oracle.NUMBER)
        id_rol = cur.var(cx_Oracle.STRING)
        valido = cur.var(cx_Oracle.NUMBER)

        cur.callproc("FIDE_USUARIOS_TB_LOGIN_SP", [
            usuario.upper(), clave, resultado, id_rol, valido
        ])

        if valido.getvalue() == 1:
            return {
                'id_usuario': resultado.getvalue(),
                'rol': id_rol.getvalue()
            }
        return None
    except Exception as e:
        print("Error al autenticar usuario:", e)
        return None
    finally:
        cur.close()
        conn.close()


def validar_usuario_login(usuario, clave):
    conn = get_connection()
    cur = conn.cursor()
    try:
        id_usuario = cur.var(cx_Oracle.NUMBER)
        rol = cur.var(cx_Oracle.STRING)
        valido = cur.var(cx_Oracle.NUMBER)

        cur.callproc("FIDE_LOGIN_VALIDAR_USUARIO_SP", [
            usuario.upper(), clave, id_usuario, rol, valido
        ])
        return {
            'id_usuario': int(id_usuario.getvalue()) if id_usuario.getvalue() else None,
            'rol': rol.getvalue(),
            'valido': valido.getvalue() == 1
        }
    except Exception as e:
        print("Error al validar usuario:", e)
        return {'id_usuario': None, 'rol': None, 'valido': False}
    finally:
        cur.close()
        conn.close()
