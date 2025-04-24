import cx_Oracle
from royalroots.init_oracle import get_connection

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
            'id_usuario': id_usuario.getvalue(),
            'rol': rol.getvalue(),
            'valido': valido.getvalue() == 1
        }
    except Exception as e:
        print("Error al validar usuario:", e)
        return {'id_usuario': None, 'rol': None, 'valido': False}
    finally:
        cur.close()
        conn.close()
