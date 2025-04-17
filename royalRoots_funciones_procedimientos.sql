--MODULO EMPLEADOS
--FUNCIONES
--PARA NO MOSTRAR IDS EN EL FRONT END
CREATE OR REPLACE FUNCTION FIDE_ESTADO_TB_OBTENER_ID_ESTADO_FN
(p_descripcion VARCHAR2)
RETURN NUMBER IS
V_ID_ESTADO NUMBER;
BEGIN
SELECT ID_ESTADO INTO V_ID_ESTADO 
FROM FIDE_ESTADO_TB 
WHERE UPPER(DESCRIPCION) = UPPER(p_descripcion);
RETURN v_id_estado;

EXCEPTION
  WHEN NO_DATA_FOUND THEN
    RETURN NULL;
END;
/

CREATE OR REPLACE PROCEDURE FIDE_ESTADO_TB_LISTAR_ESTADOS_SP (
    p_cursor OUT SYS_REFCURSOR
) IS
BEGIN
    OPEN p_cursor FOR
        SELECT DESCRIPCION
        FROM FIDE_ESTADO_TB
        WHERE UPPER(DESCRIPCION) IN ('ACTIVO', 'INACTIVO');
END;
/

CREATE OR REPLACE FUNCTION FIDE_EMPLEADOS_FUNCION_TB_OBTENER_ID_FUNCION_FN
(p_nombre_funcion VARCHAR2)
RETURN NUMBER IS
  v_id_funcion NUMBER;
BEGIN
  SELECT ID_FUNCION INTO v_id_funcion
  FROM FIDE_EMPLEADOS_FUNCION_TB
  WHERE UPPER(NOMBRE_FUNCION) = UPPER(p_nombre_funcion);

  RETURN v_id_funcion;
EXCEPTION
  WHEN NO_DATA_FOUND THEN
    RETURN NULL;
END;
/

CREATE OR REPLACE FUNCTION FIDE_TURNOS_TB_OBTENER_ID_TURNO_FN(p_inicio DATE, p_fin DATE)
RETURN NUMBER IS
  v_id_turno NUMBER;
BEGIN
  SELECT ID_TURNO INTO v_id_turno
  FROM FIDE_TURNOS_TB
  WHERE HORA_INICIO = p_inicio AND HORA_FIN = p_fin;

  RETURN v_id_turno;
EXCEPTION
  WHEN NO_DATA_FOUND THEN
    RETURN NULL;
END;
/


--PROCEDIMIENTOS
CREATE OR REPLACE PROCEDURE FIDE_EMPLEADOS_TB_INSERTAR_EMPLEADO_SP (
    p_nombre IN VARCHAR2,
    p_apellido IN VARCHAR2,
    p_correo IN VARCHAR2,
    p_telefono IN VARCHAR2,
    p_fecha IN DATE,
    p_salario IN NUMBER,
    p_funcion_nombre IN VARCHAR2,
    p_hora_inicio IN TIMESTAMP,
    p_hora_fin IN TIMESTAMP,
    p_estado_nombre IN VARCHAR2
)
AS
    v_funcion_id  NUMBER;
    v_estado_id   NUMBER;
    v_turno_id    NUMBER;
    v_empleado_id NUMBER;
BEGIN
    SELECT ID_FUNCION INTO v_funcion_id
    FROM FIDE_EMPLEADOS_FUNCION_TB
    WHERE NOMBRE_FUNCION = p_funcion_nombre;

    SELECT ID_ESTADO INTO v_estado_id
    FROM FIDE_ESTADO_TB
    WHERE DESCRIPCION = p_estado_nombre;

    SELECT ID_TURNO INTO v_turno_id
    FROM FIDE_TURNOS_TB
    WHERE HORA_INICIO = p_hora_inicio AND HORA_FIN = p_hora_fin;

    SELECT FIDE_EMPLEADOS_TB_SEQ.NEXTVAL INTO v_empleado_id FROM DUAL;

    INSERT INTO FIDE_EMPLEADOS_TB (
        ID_EMPLEADO, NOMBRE_EMPLEADO, APELLIDO_EMPLEADO, ADMIN_CORREO,
        TELEFONO, FECHA_CONTRATACION, SALARIO,
        ID_FUNCION, ID_TURNO, ID_ESTADO
    ) VALUES (
        v_empleado_id, p_nombre, p_apellido, p_correo,
        p_telefono, p_fecha, p_salario,
        v_funcion_id, v_turno_id, v_estado_id
    );

    COMMIT;
END;
/


CREATE OR REPLACE PROCEDURE FIDE_EMPLEADOS_TB_ACTUALIZAR_EMPLEADO_SP (
    p_nombre IN VARCHAR2,
    p_apellido IN VARCHAR2,
    p_correo IN VARCHAR2,
    p_telefono IN VARCHAR2,
    p_fecha IN DATE,
    p_salario IN NUMBER,
    p_funcion_nombre IN VARCHAR2,
    p_hora_inicio IN TIMESTAMP,
    p_hora_fin IN TIMESTAMP,
    p_estado_nombre IN VARCHAR2
)
AS
    v_funcion_id  NUMBER;
    v_estado_id   NUMBER;
    v_turno_id    NUMBER;
    v_empleado_id NUMBER;
BEGIN
    SELECT ID_FUNCION INTO v_funcion_id
    FROM FIDE_EMPLEADOS_FUNCION_TB
    WHERE NOMBRE_FUNCION = p_funcion_nombre;

    SELECT ID_ESTADO INTO v_estado_id
    FROM FIDE_ESTADO_TB
    WHERE DESCRIPCION = p_estado_nombre;

    SELECT ID_TURNO INTO v_turno_id
    FROM FIDE_TURNOS_TB
    WHERE HORA_INICIO = p_hora_inicio AND HORA_FIN = p_hora_fin;

    SELECT ID_EMPLEADO INTO v_empleado_id
    FROM FIDE_EMPLEADOS_TB
    WHERE ADMIN_CORREO = p_correo;

    UPDATE FIDE_EMPLEADOS_TB
    SET 
        NOMBRE_EMPLEADO = p_nombre,
        APELLIDO_EMPLEADO = p_apellido,
        TELEFONO = p_telefono,
        FECHA_CONTRATACION = p_fecha,
        SALARIO = p_salario,
        ID_FUNCION = v_funcion_id,
        ID_TURNO = v_turno_id,
        ID_ESTADO = v_estado_id
    WHERE ID_EMPLEADO = v_empleado_id;

    COMMIT;
END;
/



CREATE OR REPLACE PROCEDURE FIDE_EMPLEADOS_TB_ELIMINAR_EMPLEADO_SP (
    p_correo IN VARCHAR2
)
AS
    v_empleado_id NUMBER;
    v_estado_inactivo_id NUMBER;
BEGIN
    SELECT ID_EMPLEADO INTO v_empleado_id
    FROM FIDE_EMPLEADOS_TB
    WHERE ADMIN_CORREO = p_correo;

    SELECT ID_ESTADO INTO v_estado_inactivo_id
    FROM FIDE_ESTADO_TB
    WHERE UPPER(DESCRIPCION) = 'INACTIVO';

    UPDATE FIDE_EMPLEADOS_TB
    SET ID_ESTADO = v_estado_inactivo_id
    WHERE ID_EMPLEADO = v_empleado_id;

    COMMIT;
END;
/


CREATE OR REPLACE PROCEDURE FIDE_EMPLEADOS_TB_LISTAR_EMPLEADOS_SP (
    p_resultado OUT SYS_REFCURSOR
)
AS
BEGIN
    OPEN p_resultado FOR
        SELECT 
            E.ID_EMPLEADO,
            E.NOMBRE_EMPLEADO,
            E.APELLIDO_EMPLEADO,
            E.ADMIN_CORREO,
            E.TELEFONO,
            E.FECHA_CONTRATACION,
            E.SALARIO,
            TO_CHAR(T.HORA_INICIO, 'HH24:MI') AS HORA_INICIO,
            TO_CHAR(T.HORA_FIN, 'HH24:MI') AS HORA_FIN,
            F.NOMBRE_FUNCION,
            S.DESCRIPCION AS ESTADO
        FROM FIDE_EMPLEADOS_TB E
        JOIN FIDE_TURNOS_TB T ON E.ID_TURNO = T.ID_TURNO
        JOIN FIDE_EMPLEADOS_FUNCION_TB F ON E.ID_FUNCION = F.ID_FUNCION
        JOIN FIDE_ESTADO_TB S ON E.ID_ESTADO = S.ID_ESTADO
        WHERE UPPER(S.DESCRIPCION) != 'INACTIVO';
END;
/




--FIDE TURNOS
CREATE OR REPLACE PROCEDURE FIDE_TURNOS_TB_INSERTAR_TURNO_SP(
    p_hora_inicio IN TIMESTAMP,
    p_hora_fin IN TIMESTAMP,
    p_estado_desc IN VARCHAR2
)
AS
    v_id_estado NUMBER;
    v_id_turno NUMBER;
BEGIN
    DBMS_OUTPUT.PUT_LINE('Inicio del procedimiento');

    SELECT ID_ESTADO INTO v_id_estado
    FROM FIDE_ESTADO_TB
    WHERE UPPER(DESCRIPCION) = UPPER(p_estado_desc);

    SELECT FIDE_TURNOS_TB_SEQ.NEXTVAL INTO v_id_turno FROM DUAL;

    INSERT INTO FIDE_TURNOS_TB (
        ID_TURNO, HORA_INICIO, HORA_FIN, ID_ESTADO
    ) VALUES (
        v_id_turno, p_hora_inicio, p_hora_fin, v_id_estado
    );

    DBMS_OUTPUT.PUT_LINE('Insert ejecutado con turno ID: ' || v_id_turno);

    COMMIT;
    
    DBMS_OUTPUT.PUT_LINE('Turno insertado correctamente.');
EXCEPTION
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('Error al insertar turno: ' || SQLERRM);
        ROLLBACK;
END;
/

BEGIN
  FIDE_TURNOS_TB_INSERTAR_TURNO_SP(TO_DATE('08:00', 'HH24:MI'), TO_DATE('16:00', 'HH24:MI'), 'ACTIVO');
END;



CREATE OR REPLACE PROCEDURE FIDE_TURNOS_TB_ELIMINAR_TURNO_SP(
    p_hora_inicio IN TIMESTAMP,
    p_hora_fin IN TIMESTAMP
)
AS
    v_id_turno NUMBER;
    v_id_estado NUMBER;
BEGIN
    SELECT ID_TURNO INTO v_id_turno
    FROM FIDE_TURNOS_TB
    WHERE HORA_INICIO = p_hora_inicio AND HORA_FIN = p_hora_fin;

    SELECT ID_ESTADO INTO v_id_estado
    FROM FIDE_ESTADO_TB
    WHERE UPPER(DESCRIPCION) = 'INACTIVO';

    UPDATE FIDE_TURNOS_TB
    SET ID_ESTADO = v_id_estado
    WHERE ID_TURNO = v_id_turno;

    COMMIT;
EXCEPTION
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('Error al inactivar turno: ' || SQLERRM);
        ROLLBACK;
END;
/



CREATE OR REPLACE PROCEDURE FIDE_TURNOS_TB_ACTUALIZAR_TURNO_SP(
    p_hora_inicio IN TIMESTAMP,
    p_hora_fin IN TIMESTAMP,
    p_nueva_hora_inicio IN TIMESTAMP,
    p_nueva_hora_fin IN TIMESTAMP,
    p_estado_desc IN VARCHAR2
)
AS
    v_id_turno NUMBER;
    v_id_estado NUMBER;
BEGIN
    SELECT ID_TURNO INTO v_id_turno
    FROM FIDE_TURNOS_TB
    WHERE HORA_INICIO = p_hora_inicio AND HORA_FIN = p_hora_fin;

    SELECT ID_ESTADO INTO v_id_estado
    FROM FIDE_ESTADO_TB
    WHERE UPPER(DESCRIPCION) = UPPER(p_estado_desc);

    UPDATE FIDE_TURNOS_TB
    SET HORA_INICIO = p_nueva_hora_inicio,
        HORA_FIN = p_nueva_hora_fin,
        ID_ESTADO = v_id_estado
    WHERE ID_TURNO = v_id_turno;

    COMMIT;
EXCEPTION
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('Error al actualizar turno: ' || SQLERRM);
        ROLLBACK;
END;
/



CREATE OR REPLACE PROCEDURE FIDE_TURNOS_TB_LISTAR_TURNOS_SP(
    p_resultado OUT SYS_REFCURSOR
)
AS
BEGIN
    OPEN p_resultado FOR
        SELECT 
            TO_CHAR(HORA_INICIO, 'HH24:MI') AS HORA_INICIO,
            TO_CHAR(HORA_FIN, 'HH24:MI') AS HORA_FIN,
            E.DESCRIPCION AS ESTADO
        FROM FIDE_TURNOS_TB T
        JOIN FIDE_ESTADO_TB E ON T.ID_ESTADO = E.ID_ESTADO;
END;
/


--FIDE FUNCION
CREATE OR REPLACE FUNCTION FIDE_EMPLEADOS_FUNCION_TB_OBTENER_ID_FUNCION_FN(
    p_nombre_funcion VARCHAR2
) RETURN NUMBER IS
    v_id_funcion NUMBER;
BEGIN
    SELECT ID_FUNCION INTO v_id_funcion
    FROM FIDE_EMPLEADOS_FUNCION_TB
    WHERE UPPER(NOMBRE_FUNCION) = UPPER(p_nombre_funcion);

    RETURN v_id_funcion;
EXCEPTION
    WHEN NO_DATA_FOUND THEN
        RETURN NULL;
END;
/

CREATE OR REPLACE PROCEDURE FIDE_EMPLEADOS_FUNCION_TB_INSERTAR_SP (
    p_nombre_funcion IN VARCHAR2,
    p_descripcion IN VARCHAR2,
    p_estado_desc IN VARCHAR2
) AS
    v_id_funcion NUMBER;
    v_id_estado NUMBER;
BEGIN
    SELECT FIDE_EMPLEADOS_FUNCION_TB_SEQ.NEXTVAL INTO v_id_funcion FROM DUAL;

    SELECT ID_ESTADO INTO v_id_estado
    FROM FIDE_ESTADO_TB
    WHERE UPPER(DESCRIPCION) = UPPER(p_estado_desc);

    INSERT INTO FIDE_EMPLEADOS_FUNCION_TB (
        ID_FUNCION, NOMBRE_FUNCION, DESCRIPCION, ID_ESTADO
    ) VALUES (
        v_id_funcion, p_nombre_funcion, p_descripcion, v_id_estado
    );

    COMMIT;
EXCEPTION
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('Error al insertar función: ' || SQLERRM);
        ROLLBACK;
END;
/

CREATE OR REPLACE PROCEDURE FIDE_EMPLEADOS_FUNCION_TB_ACTUALIZAR_SP (
    p_nombre_funcion_actual IN VARCHAR2,
    p_nuevo_nombre_funcion IN VARCHAR2,
    p_nueva_descripcion IN VARCHAR2,
    p_estado_desc IN VARCHAR2
) AS
    v_id_estado NUMBER;
BEGIN
    SELECT ID_ESTADO INTO v_id_estado
    FROM FIDE_ESTADO_TB
    WHERE UPPER(DESCRIPCION) = UPPER(p_estado_desc);

    UPDATE FIDE_EMPLEADOS_FUNCION_TB
    SET NOMBRE_FUNCION = p_nuevo_nombre_funcion,
        DESCRIPCION = p_nueva_descripcion,
        ID_ESTADO = v_id_estado
    WHERE UPPER(NOMBRE_FUNCION) = UPPER(p_nombre_funcion_actual);

    COMMIT;
EXCEPTION
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('Error al actualizar función: ' || SQLERRM);
        ROLLBACK;
END;
/

CREATE OR REPLACE PROCEDURE FIDE_EMPLEADOS_FUNCION_TB_INACTIVAR_SP (
    p_nombre_funcion IN VARCHAR2
) AS
    v_id_estado NUMBER;
BEGIN
    SELECT ID_ESTADO INTO v_id_estado
    FROM FIDE_ESTADO_TB
    WHERE UPPER(DESCRIPCION) = 'INACTIVO';

    UPDATE FIDE_EMPLEADOS_FUNCION_TB
    SET ID_ESTADO = v_id_estado
    WHERE UPPER(NOMBRE_FUNCION) = UPPER(p_nombre_funcion);

    COMMIT;
EXCEPTION
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('Error al inactivar función: ' || SQLERRM);
        ROLLBACK;
END;
/

CREATE OR REPLACE PROCEDURE FIDE_EMPLEADOS_FUNCION_TB_LISTAR_SP (
    p_resultado OUT SYS_REFCURSOR
) AS
BEGIN
    OPEN p_resultado FOR
        SELECT 
            F.NOMBRE_FUNCION,
            F.DESCRIPCION AS FUNCION_DESC,
            E.DESCRIPCION AS ESTADO
        FROM FIDE_EMPLEADOS_FUNCION_TB F
        JOIN FIDE_ESTADO_TB E ON F.ID_ESTADO = E.ID_ESTADO;
END;
/




--vacaciones
CREATE OR REPLACE FUNCTION FIDE_EMPLEADOS_TB_OBTENER_ID_EMPLEADO_FN (
    p_correo IN VARCHAR2
) RETURN NUMBER IS
    v_id_empleado NUMBER;
BEGIN
    SELECT ID_EMPLEADO INTO v_id_empleado
    FROM FIDE_EMPLEADOS_TB
    WHERE UPPER(ADMIN_CORREO) = UPPER(p_correo);

    RETURN v_id_empleado;
EXCEPTION
    WHEN NO_DATA_FOUND THEN
        RETURN NULL;
END;
/


CREATE OR REPLACE PROCEDURE FIDE_VACACIONES_TB_INSERTAR_SP (
    p_fecha IN DATE,
    p_correo IN VARCHAR2,
    p_nombre_funcion IN VARCHAR2,
    p_estado_desc IN VARCHAR2
) AS
    v_id_empleado NUMBER;
    v_id_funcion NUMBER;
    v_id_estado NUMBER;
    v_id_vacacion NUMBER;
BEGIN
    v_id_empleado := FIDE_EMPLEADOS_TB_OBTENER_ID_EMPLEADO_FN(p_correo);
    v_id_funcion := FIDE_EMPLEADOS_FUNCION_TB_OBTENER_ID_FUNCION_FN(p_nombre_funcion);
    v_id_estado := FIDE_ESTADO_TB_OBTENER_ID_ESTADO_FN(p_estado_desc);
    SELECT FIDE_VACACIONES_TB_SEQ.NEXTVAL INTO v_id_vacacion FROM DUAL;

    INSERT INTO FIDE_VACACIONES_TB (
        ID_VACACION, FECHA, ID_EMPLEADO, ID_FUNCION, ID_ESTADO
    ) VALUES (
        v_id_vacacion, p_fecha, v_id_empleado, v_id_funcion, v_id_estado
    );
    COMMIT;
EXCEPTION
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('Error al insertar vacación: ' || SQLERRM);
        ROLLBACK;
END;
/

create or replace PROCEDURE FIDE_VACACIONES_TB_LISTAR_SP (
    p_resultado OUT SYS_REFCURSOR
)
AS
BEGIN
    OPEN p_resultado FOR
        SELECT 
            E.NOMBRE_empleado || ' ' || E.APELLIDO_empleado AS EMPLEADO,
            V.FECHA,
            F.NOMBRE_FUNCION,
            ES.DESCRIPCION AS ESTADO
        FROM FIDE_VACACIONES_TB V
        JOIN FIDE_EMPLEADOS_TB E ON V.ID_EMPLEADO = E.ID_EMPLEADO
        JOIN FIDE_EMPLEADOS_FUNCION_TB F ON V.ID_FUNCION = F.ID_FUNCION
        JOIN FIDE_ESTADO_TB ES ON V.ID_ESTADO = ES.ID_ESTADO;
END;
/


CREATE OR REPLACE PROCEDURE FIDE_VACACIONES_TB_ACTUALIZAR_SP (
    p_correo IN VARCHAR2,
    p_fecha IN DATE,
    p_nueva_fecha IN DATE,
    p_nueva_funcion IN VARCHAR2,
    p_estado_desc IN VARCHAR2
)
AS
    v_id_empleado NUMBER;
    v_id_funcion NUMBER;
    v_id_estado NUMBER;
BEGIN
    v_id_empleado := FIDE_EMPLEADOS_TB_OBTENER_ID_EMPLEADO_FN(p_correo);
    v_id_funcion := FIDE_EMPLEADOS_FUNCION_TB_OBTENER_ID_FUNCION_FN(p_nueva_funcion);
    v_id_estado := FIDE_ESTADO_TB_OBTENER_ID_ESTADO_FN(p_estado_desc);

    UPDATE FIDE_VACACIONES_TB
    SET FECHA = p_nueva_fecha,
        ID_FUNCION = v_id_funcion,
        ID_ESTADO = v_id_estado
    WHERE ID_EMPLEADO = v_id_empleado AND FECHA = p_fecha;

    COMMIT;
EXCEPTION
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('Error al actualizar vacación: ' || SQLERRM);
        ROLLBACK;
END;
/

CREATE OR REPLACE PROCEDURE FIDE_VACACIONES_TB_INACTIVAR_SP (
    p_correo IN VARCHAR2,
    p_fecha IN DATE
)
AS
    v_id_empleado NUMBER;
    v_id_estado NUMBER;
BEGIN
    v_id_empleado := FIDE_EMPLEADOS_TB_OBTENER_ID_EMPLEADO_FN(p_correo);
    v_id_estado := FIDE_ESTADO_TB_OBTENER_ID_ESTADO_FN('INACTIVO');

    UPDATE FIDE_VACACIONES_TB
    SET ID_ESTADO = v_id_estado
    WHERE ID_EMPLEADO = v_id_empleado AND FECHA = p_fecha;

    COMMIT;
EXCEPTION
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('Error al inactivar vacación: ' || SQLERRM);
        ROLLBACK;
END;
/


























--modulos de direccion
CREATE OR REPLACE PROCEDURE FIDE_PROVINCIA_TB_INSERTAR_PROVINCIA_SP (
    p_nombre_provincia IN VARCHAR2,
    p_estado_desc IN VARCHAR2
) AS
    v_id_estado NUMBER;
    v_id_provincia NUMBER;
BEGIN
    -- Obtener ID del estado
    v_id_estado := FIDE_ESTADO_TB_OBTENER_ID_ESTADO_FN(p_estado_desc);

    -- Generar ID automático
    SELECT FIDE_PROVINCIA_TB_SEQ.NEXTVAL INTO v_id_provincia FROM DUAL;

    INSERT INTO FIDE_PROVINCIA_TB (
        ID_PROVINCIA, PROVINCIA, ID_ESTADO
    ) VALUES (
        v_id_provincia, UPPER (p_nombre_provincia), v_id_estado
    );
    COMMIT;
EXCEPTION
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('Error al insertar provincia: ' || SQLERRM);
        ROLLBACK;
END;
/

CREATE OR REPLACE PROCEDURE FIDE_PROVINCIA_TB_LISTAR_PROVINCIAS_SP (
    p_resultado OUT SYS_REFCURSOR
)
AS
BEGIN
    OPEN p_resultado FOR
        SELECT P.PROVINCIA,
               E.DESCRIPCION AS ESTADO
        FROM FIDE_PROVINCIA_TB P
        JOIN FIDE_ESTADO_TB E ON P.ID_ESTADO = E.ID_ESTADO;
END;
/

CREATE OR REPLACE PROCEDURE FIDE_PROVINCIA_TB_ACTUALIZAR_PROVINCIA_SP (
    p_nombre_actual IN VARCHAR2,
    p_nuevo_nombre IN VARCHAR2,
    p_nuevo_estado_desc IN VARCHAR2
) AS
    v_id_estado NUMBER;
BEGIN
    -- Obtener ID del nuevo estado
    v_id_estado := FIDE_ESTADO_TB_OBTENER_ID_ESTADO_FN(p_nuevo_estado_desc);

    UPDATE FIDE_PROVINCIA_TB
    SET PROVINCIA = p_nuevo_nombre,
        ID_ESTADO = v_id_estado
    WHERE UPPER(PROVINCIA) = UPPER(p_nombre_actual);
    COMMIT;
EXCEPTION
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('Error al actualizar provincia: ' || SQLERRM);
        ROLLBACK;
END;
/

CREATE OR REPLACE PROCEDURE FIDE_PROVINCIA_TB_INACTIVAR_PROVINCIA_SP (
    p_nombre_provincia IN VARCHAR2
) AS
    v_id_estado_inactivo NUMBER;
BEGIN
    v_id_estado_inactivo := FIDE_ESTADO_TB_OBTENER_ID_ESTADO_FN('INACTIVO');

    UPDATE FIDE_PROVINCIA_TB
    SET ID_ESTADO = v_id_estado_inactivo
    WHERE UPPER(PROVINCIA) = UPPER(p_nombre_provincia);

    COMMIT;
EXCEPTION
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('Error al inactivar provincia: ' || SQLERRM);
        ROLLBACK;
END;
/


--obtiene el id de provincia
CREATE OR REPLACE FUNCTION FIDE_PROVINCIA_TB_OBTENER_ID_PROVINCIA_FN (
    p_nombre_provincia VARCHAR2
) RETURN NUMBER IS
    v_id_provincia NUMBER;
BEGIN
    SELECT ID_PROVINCIA INTO v_id_provincia
    FROM FIDE_PROVINCIA_TB
    WHERE UPPER(PROVINCIA) = UPPER(p_nombre_provincia);

    RETURN v_id_provincia;
EXCEPTION
    WHEN NO_DATA_FOUND THEN
        RETURN NULL;
END;
/



--canton
CREATE OR REPLACE PROCEDURE FIDE_CANTON_TB_INSERTAR_SP (
    p_nombre_canton IN VARCHAR2,
    p_provincia_nombre IN VARCHAR2,
    p_estado_desc IN VARCHAR2
) AS
    v_id_provincia NUMBER;
    v_id_estado NUMBER;
    v_id_canton NUMBER;
BEGIN
    v_id_provincia := FIDE_PROVINCIA_TB_OBTENER_ID_PROVINCIA_FN(p_provincia_nombre);
    v_id_estado := FIDE_ESTADO_TB_OBTENER_ID_ESTADO_FN(p_estado_desc);
    SELECT FIDE_CANTON_TB_SEQ.NEXTVAL INTO v_id_canton FROM DUAL;

    INSERT INTO FIDE_CANTON_TB (
        ID_CANTON, CANTON, ID_PROVINCIA, ID_ESTADO
    ) VALUES (
        v_id_canton, UPPER(p_nombre_canton), v_id_provincia, v_id_estado
    );
    COMMIT;
EXCEPTION
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('Error al insertar cantón: ' || SQLERRM);
        ROLLBACK;
END;
/

CREATE OR REPLACE PROCEDURE FIDE_CANTON_TB_LISTAR_SP (
    p_resultado OUT SYS_REFCURSOR
)
AS
BEGIN
    OPEN p_resultado FOR
        SELECT 
            C.CANTON,
            P.PROVINCIA,
            E.DESCRIPCION AS ESTADO
        FROM FIDE_CANTON_TB C
        JOIN FIDE_PROVINCIA_TB P ON C.ID_PROVINCIA = P.ID_PROVINCIA
        JOIN FIDE_ESTADO_TB E ON C.ID_ESTADO = E.ID_ESTADO;
END;
/


CREATE OR REPLACE PROCEDURE FIDE_CANTON_TB_ACTUALIZAR_SP (
    p_nombre_actual IN VARCHAR2,
    p_nuevo_nombre IN VARCHAR2,
    p_nueva_provincia_nombre IN VARCHAR2,
    p_estado_desc IN VARCHAR2
) AS
    v_id_estado NUMBER;
    v_id_provincia NUMBER;
BEGIN
    v_id_estado := FIDE_ESTADO_TB_OBTENER_ID_ESTADO_FN(p_estado_desc);
    v_id_provincia := FIDE_PROVINCIA_TB_OBTENER_ID_PROVINCIA_FN(p_nueva_provincia_nombre);

    UPDATE FIDE_CANTON_TB
    SET CANTON = p_nuevo_nombre,
        ID_PROVINCIA = v_id_provincia,
        ID_ESTADO = v_id_estado
    WHERE UPPER(CANTON) = UPPER(p_nombre_actual);

    COMMIT;
EXCEPTION
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('Error al actualizar cantón: ' || SQLERRM);
        ROLLBACK;
END;
/

CREATE OR REPLACE PROCEDURE FIDE_CANTON_TB_INACTIVAR_SP (
    p_nombre_canton IN VARCHAR2
) AS
    v_id_estado NUMBER;
BEGIN
    v_id_estado := FIDE_ESTADO_TB_OBTENER_ID_ESTADO_FN('INACTIVO');

    UPDATE FIDE_CANTON_TB
    SET ID_ESTADO = v_id_estado
    WHERE UPPER(CANTON) = UPPER(p_nombre_canton);

    COMMIT;
EXCEPTION
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('Error al inactivar cantón: ' || SQLERRM);
        ROLLBACK;
END;
/

--distritos
CREATE OR REPLACE FUNCTION FIDE_CANTON_TB_OBTENER_ID_CANTON_FN (
    p_nombre_canton VARCHAR2
) RETURN NUMBER IS
    v_id_canton NUMBER;
BEGIN
    SELECT ID_CANTON INTO v_id_canton
    FROM FIDE_CANTON_TB
    WHERE UPPER(CANTON) = UPPER(p_nombre_canton);

    RETURN v_id_canton;
END;

CREATE OR REPLACE PROCEDURE FIDE_DISTRITO_TB_INSERTAR_SP (
    p_nombre_distrito IN VARCHAR2,
    p_nombre_canton IN VARCHAR2,
    p_estado_desc IN VARCHAR2
) AS
    v_id_canton NUMBER;
    v_id_estado NUMBER;
    v_id_distrito NUMBER;
BEGIN
    v_id_canton := FIDE_CANTON_TB_OBTENER_ID_CANTON_FN(p_nombre_canton);
    v_id_estado := FIDE_ESTADO_TB_OBTENER_ID_ESTADO_FN(p_estado_desc);
    SELECT FIDE_DISTRITO_TB_SEQ.NEXTVAL INTO v_id_distrito FROM DUAL;

    INSERT INTO FIDE_DISTRITO_TB (
        ID_DISTRITO, DISTRITO, ID_CANTON, ID_ESTADO
    ) VALUES (
        v_id_distrito, UPPER (p_nombre_distrito), v_id_canton, v_id_estado
    );
    COMMIT;
EXCEPTION
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('Error al insertar distrito: ' || SQLERRM);
        ROLLBACK;
END;
/

CREATE OR REPLACE PROCEDURE FIDE_DISTRITO_TB_LISTAR_SP (
    p_resultado OUT SYS_REFCURSOR
)
AS
BEGIN
    OPEN p_resultado FOR
        SELECT 
            D.DISTRITO,
            C.CANTON,
            E.DESCRIPCION AS ESTADO
        FROM FIDE_DISTRITO_TB D
        JOIN FIDE_CANTON_TB C ON D.ID_CANTON = C.ID_CANTON
        JOIN FIDE_ESTADO_TB E ON D.ID_ESTADO = E.ID_ESTADO;
END;
/

CREATE OR REPLACE PROCEDURE FIDE_DISTRITO_TB_ACTUALIZAR_SP (
    p_nombre_actual IN VARCHAR2,
    p_nuevo_nombre IN VARCHAR2,
    p_nuevo_canton_nombre IN VARCHAR2,
    p_estado_desc IN VARCHAR2
) AS
    v_id_estado NUMBER;
    v_id_canton NUMBER;
BEGIN
    v_id_estado := FIDE_ESTADO_TB_OBTENER_ID_ESTADO_FN(p_estado_desc);
    v_id_canton := FIDE_CANTON_TB_OBTENER_ID_CANTON_FN(p_nuevo_canton_nombre);

    UPDATE FIDE_DISTRITO_TB
    SET DISTRITO = p_nuevo_nombre,
        ID_CANTON = v_id_canton,
        ID_ESTADO = v_id_estado
    WHERE UPPER(DISTRITO) = UPPER(p_nombre_actual);

    COMMIT;
EXCEPTION
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('Error al actualizar distrito: ' || SQLERRM);
        ROLLBACK;
END;
/


CREATE OR REPLACE PROCEDURE FIDE_DISTRITO_TB_INACTIVAR_SP (
    p_nombre_distrito IN VARCHAR2
) AS
    v_id_estado NUMBER;
BEGIN
    v_id_estado := FIDE_ESTADO_TB_OBTENER_ID_ESTADO_FN('INACTIVO');

    UPDATE FIDE_DISTRITO_TB
    SET ID_ESTADO = v_id_estado
    WHERE UPPER(DISTRITO) = UPPER(p_nombre_distrito);

    COMMIT;
EXCEPTION
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('Error al inactivar distrito: ' || SQLERRM);
        ROLLBACK;
END;
/

--fide_direccion

CREATE OR REPLACE FUNCTION FIDE_DISTRITO_TB_OBTENER_ID_DISTRITO_FN (
    p_nombre_distrito VARCHAR2
) RETURN NUMBER IS
    v_id_distrito NUMBER;
BEGIN
    SELECT ID_DISTRITO INTO v_id_distrito
    FROM FIDE_DISTRITO_TB
    WHERE UPPER(DISTRITO) = UPPER(p_nombre_distrito);

    RETURN v_id_distrito;
END;



--funciones para listar opciones activas

CREATE OR REPLACE FUNCTION FIDE_PROVINCIA_TB_LISTAR_ACTIVAS_FN
RETURN SYS_REFCURSOR IS
    resultado SYS_REFCURSOR;
BEGIN
    OPEN resultado FOR
        SELECT PROVINCIA
        FROM FIDE_PROVINCIA_TB
        WHERE ID_ESTADO = (
            SELECT ID_ESTADO FROM FIDE_ESTADO_TB WHERE UPPER(DESCRIPCION) = 'ACTIVO'
        );
    RETURN resultado;
END;
/


CREATE OR REPLACE FUNCTION FIDE_CANTON_TB_LISTAR_ACTIVOS_FN
RETURN SYS_REFCURSOR IS
    resultado SYS_REFCURSOR;
BEGIN
    OPEN resultado FOR
        SELECT CANTON
        FROM FIDE_CANTON_TB
        WHERE ID_ESTADO = (
            SELECT ID_ESTADO FROM FIDE_ESTADO_TB WHERE UPPER(DESCRIPCION) = 'ACTIVO'
        );
    RETURN resultado;
END;
/

CREATE OR REPLACE FUNCTION FIDE_DISTRITO_TB_LISTAR_ACTIVOS_FN
RETURN SYS_REFCURSOR IS
    resultado SYS_REFCURSOR;
BEGIN
    OPEN resultado FOR
        SELECT DISTRITO
        FROM FIDE_DISTRITO_TB
        WHERE ID_ESTADO = (
            SELECT ID_ESTADO FROM FIDE_ESTADO_TB WHERE UPPER(DESCRIPCION) = 'ACTIVO'
        );
    RETURN resultado;
END;
/



CREATE OR REPLACE PROCEDURE FIDE_DIRECCION_TB_INSERTAR_SP (
    p_provincia_nombre IN VARCHAR2,
    p_canton_nombre    IN VARCHAR2,
    p_distrito_nombre  IN VARCHAR2,
    p_estado_nombre    IN VARCHAR2
)
AS
    v_id_provincia NUMBER;
    v_id_canton    NUMBER;
    v_id_distrito  NUMBER;
    v_id_estado    NUMBER;
    v_id_direccion NUMBER;
BEGIN
    -- Obtener IDs desde funciones
    v_id_provincia := FIDE_PROVINCIA_TB_OBTENER_ID_PROVINCIA_FN(p_provincia_nombre);
    v_id_canton    := FIDE_CANTON_TB_OBTENER_ID_CANTON_FN(p_canton_nombre);
    v_id_distrito  := FIDE_DISTRITO_TB_OBTENER_ID_DISTRITO_FN(p_distrito_nombre);

    SELECT ID_ESTADO INTO v_id_estado
    FROM FIDE_ESTADO_TB
    WHERE UPPER(DESCRIPCION) = UPPER(p_estado_nombre);

    -- Obtener nuevo ID
    SELECT FIDE_DIRECCION_TB_SEQ.NEXTVAL INTO v_id_direccion FROM DUAL;

    -- Insertar dirección
    INSERT INTO FIDE_DIRECCION_TB (
        ID_DIRECCION, ID_PROVINCIA, ID_CANTON, ID_DISTRITO, ID_ESTADO
    ) VALUES (
        v_id_direccion, v_id_provincia, v_id_canton, v_id_distrito, v_id_estado
    );

    COMMIT;
END;
/


CREATE OR REPLACE PROCEDURE FIDE_DIRECCION_TB_LISTAR_SP (
    p_resultado OUT SYS_REFCURSOR
)
AS
BEGIN
    OPEN p_resultado FOR
    SELECT 
        D.ID_DIRECCION,
        P.PROVINCIA,
        C.CANTON,
        DI.DISTRITO,
        E.DESCRIPCION AS ESTADO
    FROM FIDE_DIRECCION_TB D
    JOIN FIDE_PROVINCIA_TB P ON D.ID_PROVINCIA = P.ID_PROVINCIA
    JOIN FIDE_CANTON_TB C ON D.ID_CANTON = C.ID_CANTON
    JOIN FIDE_DISTRITO_TB DI ON D.ID_DISTRITO = DI.ID_DISTRITO
    JOIN FIDE_ESTADO_TB E ON D.ID_ESTADO = E.ID_ESTADO;
    
END;
/


CREATE OR REPLACE PROCEDURE FIDE_DIRECCION_TB_ACTUALIZAR_SP (
    p_id_direccion     IN NUMBER,
    p_provincia_nombre IN VARCHAR2,
    p_canton_nombre    IN VARCHAR2,
    p_distrito_nombre  IN VARCHAR2,
    p_estado_nombre    IN VARCHAR2
)
AS
    v_id_provincia NUMBER;
    v_id_canton    NUMBER;
    v_id_distrito  NUMBER;
    v_id_estado    NUMBER;
BEGIN
    -- Obtener IDs desde funciones
    v_id_provincia := FIDE_PROVINCIA_TB_OBTENER_ID_PROVINCIA_FN(p_provincia_nombre);
    v_id_canton    := FIDE_CANTON_TB_OBTENER_ID_CANTON_FN(p_canton_nombre);
    v_id_distrito  := FIDE_DISTRITO_TB_OBTENER_ID_DISTRITO_FN(p_distrito_nombre);

    SELECT ID_ESTADO INTO v_id_estado
    FROM FIDE_ESTADO_TB
    WHERE UPPER(DESCRIPCION) = UPPER(p_estado_nombre);

    UPDATE FIDE_DIRECCION_TB
    SET 
        ID_PROVINCIA = v_id_provincia,
        ID_CANTON = v_id_canton,
        ID_DISTRITO = v_id_distrito,
        ID_ESTADO = v_id_estado
    WHERE ID_DIRECCION = p_id_direccion;

    COMMIT;
END;
/


CREATE OR REPLACE PROCEDURE FIDE_DIRECCION_TB_INACTIVAR_SP (
    p_id_direccion IN NUMBER
)
AS
    v_id_estado NUMBER;
BEGIN
    SELECT ID_ESTADO INTO v_id_estado
    FROM FIDE_ESTADO_TB
    WHERE UPPER(DESCRIPCION) = 'INACTIVO';

    UPDATE FIDE_DIRECCION_TB
    SET ID_ESTADO = v_id_estado
    WHERE ID_DIRECCION = p_id_direccion;

    COMMIT;
END;
/




--modulo clientes
--FIDE SERVICIOS
CREATE OR REPLACE PROCEDURE FIDE_SERVICIOS_TB_INSERTAR_SP (
    p_nombre IN VARCHAR2,
    p_descripcion IN VARCHAR2,
    p_precio IN NUMBER,
    p_estado IN VARCHAR2
) AS
    v_estado_id NUMBER;
    v_servicio_id NUMBER;
BEGIN
    SELECT FIDE_SERVICIOS_TB_SEQ.NEXTVAL INTO v_servicio_id FROM DUAL;

    v_estado_id := FIDE_ESTADO_TB_OBTENER_ID_ESTADO_FN(p_estado);

    INSERT INTO FIDE_SERVICIOS_TB (
        ID_SERVICIO, NOMBRE_SERVICIO, DESCRIPCION, PRECIO, ID_ESTADO
    ) VALUES (
        v_servicio_id, p_nombre, p_descripcion, p_precio, v_estado_id
    );

    COMMIT;
END;
/

CREATE OR REPLACE PROCEDURE FIDE_SERVICIOS_TB_LISTAR_SP(
    p_resultado OUT SYS_REFCURSOR
) AS
BEGIN
    OPEN p_resultado FOR
        SELECT 
            S.NOMBRE_SERVICIO,
            S.DESCRIPCION,
            S.PRECIO,
            E.DESCRIPCION AS ESTADO
        FROM FIDE_SERVICIOS_TB S
        JOIN FIDE_ESTADO_TB E ON S.ID_ESTADO = E.ID_ESTADO;
END;
/

CREATE OR REPLACE PROCEDURE FIDE_SERVICIOS_TB_ACTUALIZAR_SP (
    p_nombre_original IN VARCHAR2,
    p_nombre_nuevo IN VARCHAR2,
    p_descripcion IN VARCHAR2,
    p_precio IN NUMBER,
    p_estado IN VARCHAR2
) AS
    v_estado_id NUMBER;
BEGIN
    v_estado_id := FIDE_ESTADO_TB_OBTENER_ID_ESTADO_FN(p_estado);

    UPDATE FIDE_SERVICIOS_TB
    SET NOMBRE_SERVICIO = p_nombre_nuevo,
        DESCRIPCION = p_descripcion,
        PRECIO = p_precio,
        ID_ESTADO = v_estado_id
    WHERE UPPER(NOMBRE_SERVICIO) = UPPER(p_nombre_original);

    COMMIT;
END;
/

CREATE OR REPLACE PROCEDURE FIDE_SERVICIOS_TB_INACTIVAR_SP (
    p_nombre IN VARCHAR2
) AS
    v_estado_inactivo NUMBER;
BEGIN
    v_estado_inactivo := FIDE_ESTADO_TB_OBTENER_ID_ESTADO_FN('INACTIVO');

    UPDATE FIDE_SERVICIOS_TB
    SET ID_ESTADO = v_estado_inactivo;
    COMMIT;
END;
/


--FIDE_BENEFICIO CRUD
CREATE OR REPLACE FUNCTION FIDE_SERVICIOS_TB_OBTENER_ID_SERVICIO_FN(
    p_nombre_servicio IN VARCHAR2
) RETURN NUMBER IS
    v_id_servicio NUMBER;
BEGIN
    SELECT ID_SERVICIO INTO v_id_servicio
    FROM FIDE_SERVICIOS_TB
    WHERE UPPER(NOMBRE_SERVICIO) = UPPER(p_nombre_servicio);

    RETURN v_id_servicio;
EXCEPTION
    WHEN NO_DATA_FOUND THEN
        RETURN NULL;
    WHEN OTHERS THEN
        RETURN NULL;
END;
/


CREATE OR REPLACE PROCEDURE FIDE_BENEFICIO_TB_INSERTAR_SP (
    p_detalle_beneficio IN VARCHAR2,
    p_nombre_servicio IN VARCHAR2,
    p_estado IN VARCHAR2
) AS
    v_id_beneficio NUMBER;
    v_id_servicio NUMBER;
    v_id_estado NUMBER;
BEGIN
    SELECT FIDE_BENEFICIO_TB_SEQ.NEXTVAL INTO v_id_beneficio FROM DUAL;

    v_id_servicio := FIDE_SERVICIOS_TB_OBTENER_ID_SERVICIO_FN(p_nombre_servicio);

    SELECT ID_ESTADO INTO v_id_estado
    FROM FIDE_ESTADO_TB
    WHERE UPPER(DESCRIPCION) = UPPER(p_estado);

    INSERT INTO FIDE_BENEFICIO_TB (
        ID_BENEFICIO, DETALLE_BENEFICIO, ID_SERVICIO, ID_ESTADO
    ) VALUES (
        v_id_beneficio, p_detalle_beneficio, v_id_servicio, v_id_estado
    );

    COMMIT;
END;
/


CREATE OR REPLACE PROCEDURE FIDE_BENEFICIO_TB_ACTUALIZAR_SP (
    p_detalle_actual IN VARCHAR2,
    p_detalle_nuevo IN VARCHAR2,
    p_nombre_servicio IN VARCHAR2,
    p_estado IN VARCHAR2
) AS
    v_id_beneficio NUMBER;
    v_id_servicio NUMBER;
    v_id_estado NUMBER;
BEGIN
    SELECT ID_BENEFICIO INTO v_id_beneficio
    FROM FIDE_BENEFICIO_TB
    WHERE UPPER(DETALLE_BENEFICIO) = UPPER(p_detalle_actual);

    v_id_servicio := FIDE_SERVICIOS_TB_OBTENER_ID_SERVICIO_FN(p_nombre_servicio);

    SELECT ID_ESTADO INTO v_id_estado
    FROM FIDE_ESTADO_TB
    WHERE UPPER(DESCRIPCION) = UPPER(p_estado);

    UPDATE FIDE_BENEFICIO_TB
    SET DETALLE_BENEFICIO = p_detalle_nuevo,
        ID_SERVICIO = v_id_servicio,
        ID_ESTADO = v_id_estado
    WHERE ID_BENEFICIO = v_id_beneficio;

    COMMIT;
END;
/


CREATE OR REPLACE PROCEDURE FIDE_BENEFICIO_TB_INACTIVAR_SP (
    p_detalle_beneficio IN VARCHAR2
) AS
    v_id_beneficio NUMBER;
    v_id_estado NUMBER;
BEGIN
    SELECT ID_BENEFICIO INTO v_id_beneficio
    FROM FIDE_BENEFICIO_TB
    WHERE UPPER(DETALLE_BENEFICIO) = UPPER(p_detalle_beneficio);

    SELECT ID_ESTADO INTO v_id_estado
    FROM FIDE_ESTADO_TB
    WHERE UPPER(DESCRIPCION) = 'INACTIVO';

    UPDATE FIDE_BENEFICIO_TB
    SET ID_ESTADO = v_id_estado
    WHERE ID_BENEFICIO = v_id_beneficio;

    COMMIT;
END;
/


CREATE OR REPLACE PROCEDURE FIDE_BENEFICIO_TB_LISTAR_SP (
    p_resultado OUT SYS_REFCURSOR
)
AS
BEGIN
    OPEN p_resultado FOR
        SELECT 
            B.DETALLE_BENEFICIO,
            S.NOMBRE_SERVICIO,
            E.DESCRIPCION AS ESTADO
        FROM FIDE_BENEFICIO_TB B
        JOIN FIDE_SERVICIOS_TB S ON B.ID_SERVICIO = S.ID_SERVICIO
        JOIN FIDE_ESTADO_TB E ON B.ID_ESTADO = E.ID_ESTADO;
END;
/


--FIDE_CLIENTES
CREATE OR REPLACE FUNCTION FIDE_DIRECCION_TB_OBTENER_ID_DIRECCION_FN (
    p_descripcion VARCHAR2
) RETURN NUMBER
IS
    v_provincia VARCHAR2(100);
    v_canton    VARCHAR2(100);
    v_distrito  VARCHAR2(100);
    v_id_provincia NUMBER;
    v_id_canton    NUMBER;
    v_id_distrito  NUMBER;
    v_id_direccion NUMBER;
BEGIN
    -- Separar la descripción
    v_provincia := REGEXP_SUBSTR(p_descripcion, '^[^-]+');
    v_canton    := REGEXP_SUBSTR(p_descripcion, '[^-]+', 1, 2);
    v_distrito  := REGEXP_SUBSTR(p_descripcion, '[^-]+', 1, 3);

    -- Convertir a mayúsculas
    v_provincia := UPPER(TRIM(v_provincia));
    v_canton    := UPPER(TRIM(v_canton));
    v_distrito  := UPPER(TRIM(v_distrito));

    -- Obtener IDs desde funciones existentes
    v_id_provincia := FIDE_PROVINCIA_TB_OBTENER_ID_PROVINCIA_FN(v_provincia);
    v_id_canton    := FIDE_CANTON_TB_OBTENER_ID_CANTON_FN(v_canton);
    v_id_distrito  := FIDE_DISTRITO_TB_OBTENER_ID_DISTRITO_FN(v_distrito);

    -- Buscar dirección exacta
    SELECT ID_DIRECCION INTO v_id_direccion
    FROM FIDE_DIRECCION_TB
    WHERE ID_PROVINCIA = v_id_provincia
      AND ID_CANTON = v_id_canton
      AND ID_DISTRITO = v_id_distrito;

    RETURN v_id_direccion;

EXCEPTION
    WHEN NO_DATA_FOUND THEN RETURN NULL;
    WHEN OTHERS THEN RETURN NULL;
END;
/



CREATE OR REPLACE PROCEDURE FIDE_CLIENTES_TB_INSERTAR_SP (
    p_nombre_cliente    IN VARCHAR2,
    p_telefono_cliente  IN VARCHAR2,
    p_correo_cliente    IN VARCHAR2,
    p_fecha_registro    IN VARCHAR2,
    p_direccion_desc    IN VARCHAR2,
    p_estado_desc       IN VARCHAR2
)
AS
    v_id_cliente    NUMBER;
    v_id_direccion  NUMBER;
    v_id_estado     NUMBER;
BEGIN
    -- Obtener valores
    v_id_direccion := FIDE_DIRECCION_TB_OBTENER_ID_DIRECCION_FN(UPPER(p_direccion_desc));
    v_id_estado    := FIDE_ESTADO_TB_OBTENER_ID_ESTADO_FN(UPPER(p_estado_desc));

    -- Validación para evitar errores por valores NULL
    IF v_id_direccion IS NULL THEN
        RAISE_APPLICATION_ERROR(-20001, 'ERROR: Dirección no válida: ' || p_direccion_desc);
    END IF;

    IF v_id_estado IS NULL THEN
        RAISE_APPLICATION_ERROR(-20002, 'ERROR: Estado no válido: ' || p_estado_desc);
    END IF;

    -- Obtener ID automático
    SELECT FIDE_CLIENTES_TB_SEQ.NEXTVAL INTO v_id_cliente FROM DUAL;

    INSERT INTO FIDE_CLIENTES_TB (
        ID_CLIENTE, NOMBRE_CLIENTE, TELEFONO_CLIENTE, CORREO_CLIENTE,
        FECHA_REGISTRO, ID_DIRECCION, ID_ESTADO,
        CREATED_BY, CREATION_DATE, ACCION
    ) VALUES (
        v_id_cliente,
        UPPER(p_nombre_cliente),
        p_telefono_cliente,
        UPPER(p_correo_cliente),
        TRUNC(TO_DATE(p_fecha_registro, 'DD/MM/YYYY')),
        v_id_direccion,
        v_id_estado,
        USER, SYSDATE, 'INSERT'
    );

    COMMIT;
END;
/

CREATE OR REPLACE PROCEDURE FIDE_CLIENTES_TB_LISTAR_SP (
    p_resultado OUT SYS_REFCURSOR
)
AS
BEGIN
    OPEN p_resultado FOR
        SELECT 
            C.ID_CLIENTE,
            C.NOMBRE_CLIENTE,
            C.TELEFONO_CLIENTE,
            C.CORREO_CLIENTE,
            TO_CHAR(C.FECHA_REGISTRO, 'DD/MM/YYYY') AS FECHA_REGISTRO,
            D.ID_DIRECCION,
            E.DESCRIPCION AS ESTADO
        FROM FIDE_CLIENTES_TB C
        JOIN FIDE_DIRECCION_TB D ON C.ID_DIRECCION = D.ID_DIRECCION
        JOIN FIDE_ESTADO_TB E ON C.ID_ESTADO = E.ID_ESTADO;
END;
/

CREATE OR REPLACE PROCEDURE FIDE_CLIENTES_TB_ACTUALIZAR_SP (
    p_id_cliente        IN NUMBER,
    p_nombre_cliente    IN VARCHAR2,
    p_telefono_cliente  IN VARCHAR2,
    p_correo_cliente    IN VARCHAR2,
    p_fecha_registro    IN VARCHAR2,
    p_direccion_desc    IN VARCHAR2,
    p_estado_desc       IN VARCHAR2
)
AS
    v_id_direccion  NUMBER;
    v_id_estado     NUMBER;
BEGIN
    v_id_direccion := FIDE_DIRECCION_TB_OBTENER_ID_DIRECCION_FN(UPPER(p_direccion_desc));
    v_id_estado    := FIDE_ESTADO_TB_OBTENER_ID_ESTADO_FN(UPPER(p_estado_desc));

    UPDATE FIDE_CLIENTES_TB
    SET 
        NOMBRE_CLIENTE   = UPPER(p_nombre_cliente),
        TELEFONO_CLIENTE = (p_telefono_cliente),
        CORREO_CLIENTE   = UPPER(p_correo_cliente),
        FECHA_REGISTRO   = TRUNC(TO_DATE(p_fecha_registro, 'DD/MM/YYYY')),
        ID_DIRECCION     = v_id_direccion,
        ID_ESTADO        = v_id_estado,
        LAST_UPDATED_BY  = USER,
        LAST_UPDATE_DATE = SYSDATE,
        ACCION           = 'UPDATE'
    WHERE ID_CLIENTE = p_id_cliente;

    COMMIT;
END;
/

CREATE OR REPLACE PROCEDURE FIDE_CLIENTES_TB_INACTIVAR_SP (
    p_id_cliente IN NUMBER
)
AS
    v_id_estado NUMBER;
BEGIN
    v_id_estado := FIDE_ESTADO_TB_OBTENER_ID_ESTADO_FN('INACTIVO');

    UPDATE FIDE_CLIENTES_TB
    SET 
        ID_ESTADO = v_id_estado,
        LAST_UPDATED_BY = USER,
        LAST_UPDATE_DATE = SYSDATE,
        ACCION = 'INACTIVAR'
    WHERE ID_CLIENTE = p_id_cliente;

    COMMIT;
END;
/



CREATE OR REPLACE FUNCTION FIDE_DIRECCION_TB_LISTAR_COMO_DESCRIPCION_FN
RETURN SYS_REFCURSOR
IS
    resultado SYS_REFCURSOR;
BEGIN
    OPEN resultado FOR
        SELECT 
            P.PROVINCIA || ' - ' || C.CANTON || ' - ' || D.DISTRITO AS DESCRIPCION
        FROM FIDE_DIRECCION_TB DIR
        JOIN FIDE_PROVINCIA_TB P ON DIR.ID_PROVINCIA = P.ID_PROVINCIA
        JOIN FIDE_CANTON_TB C ON DIR.ID_CANTON = C.ID_CANTON
        JOIN FIDE_DISTRITO_TB D ON DIR.ID_DISTRITO = D.ID_DISTRITO
        WHERE DIR.ID_ESTADO = (
            SELECT ID_ESTADO FROM FIDE_ESTADO_TB WHERE UPPER(DESCRIPCION) = 'ACTIVO'
        );
    RETURN resultado;
END;
/





SELECT 
    PR.PROVINCIA || ' - ' || CA.CANTON || ' - ' || DI.DISTRITO AS DESCRIPCION
FROM FIDE_DIRECCION_TB DIR
JOIN FIDE_PROVINCIA_TB PR ON DIR.ID_PROVINCIA = PR.ID_PROVINCIA
JOIN FIDE_CANTON_TB    CA ON DIR.ID_CANTON = CA.ID_CANTON
JOIN FIDE_DISTRITO_TB DI ON DIR.ID_DISTRITO = DI.ID_DISTRITO;



















--obtener nombres de la direccion por id_direccion
CREATE OR REPLACE FUNCTION FIDE_DIRECCION_TB_OBTENER_PROVINCIA_FN (
    p_id_direccion IN NUMBER
) RETURN VARCHAR2
IS
    v_provincia VARCHAR2(100);
BEGIN
    SELECT P.PROVINCIA INTO v_provincia
    FROM FIDE_DIRECCION_TB D
    JOIN FIDE_PROVINCIA_TB P ON D.ID_PROVINCIA = P.ID_PROVINCIA
    WHERE D.ID_DIRECCION = p_id_direccion;

    RETURN v_provincia;

EXCEPTION
    WHEN NO_DATA_FOUND THEN RETURN NULL;
    WHEN OTHERS THEN RETURN NULL;
END;
/

CREATE OR REPLACE FUNCTION FIDE_DIRECCION_TB_OBTENER_CANTON_FN (
    p_id_direccion IN NUMBER
) RETURN VARCHAR2
IS
    v_canton VARCHAR2(100);
BEGIN
    SELECT C.NOMBRE_CANTON INTO v_canton
    FROM FIDE_DIRECCION_TB D
    JOIN FIDE_CANTON_TB C ON D.ID_CANTON = C.ID_CANTON
    WHERE D.ID_DIRECCION = p_id_direccion;

    RETURN v_canton;

EXCEPTION
    WHEN NO_DATA_FOUND THEN RETURN NULL;
    WHEN OTHERS THEN RETURN NULL;
END;
/

CREATE OR REPLACE FUNCTION FIDE_DIRECCION_TB_OBTENER_DISTRITO_FN (
    p_id_direccion IN NUMBER
) RETURN VARCHAR2
IS
    v_distrito VARCHAR2(100);
BEGIN
    SELECT DI.NOMBRE_DISTRITO INTO v_distrito
    FROM FIDE_DIRECCION_TB D
    JOIN FIDE_DISTRITO_TB DI ON D.ID_DISTRITO = DI.ID_DISTRITO
    WHERE D.ID_DIRECCION = p_id_direccion;

    RETURN v_distrito;

EXCEPTION
    WHEN NO_DATA_FOUND THEN RETURN NULL;
    WHEN OTHERS THEN RETURN NULL;
END;
/




--clientes
CREATE OR REPLACE FUNCTION FIDE_CLIENTES_TB_OBTENER_ID_CLIENTE_FN (
    p_nombre_cliente IN VARCHAR2
) RETURN NUMBER IS
    v_id_cliente NUMBER;
BEGIN
    SELECT ID_CLIENTE INTO v_id_cliente
    FROM FIDE_CLIENTES_TB
    WHERE UPPER(NOMBRE_CLIENTE) = UPPER(p_nombre_cliente);

    RETURN v_id_cliente;
EXCEPTION
    WHEN NO_DATA_FOUND THEN RETURN NULL;
    WHEN OTHERS THEN RETURN NULL;
END;
/





















select * from FIDE_direccion_TB;

ALTER SESSION SET CONTAINER = XEPDB1;
SHOW CON_NAME;


