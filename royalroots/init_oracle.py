# royalroots_oracle/init_oracle.py

import cx_Oracle
import os

oracle_client_path = r"C:\oracle\instantclient-basic-windows.x64-23.7.0.25.01\instantclient_23_7"

# Solo inicializa si no se ha hecho antes
if not getattr(cx_Oracle, "_client_initialized", False):
    cx_Oracle.init_oracle_client(lib_dir=oracle_client_path)
    cx_Oracle._client_initialized = True

def get_connection():
    return cx_Oracle.connect(
        user='ROYALROOTS',
        password='royalRoots',
        dsn='localhost/XEPDB1'
    )
