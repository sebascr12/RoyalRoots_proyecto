--USUARIO
SELECT name, value 
FROM v$parameter 
WHERE name = 'common_user_prefix';
 
/
CREATE USER royalRoots IDENTIFIED BY royalRoots;
 
/
ALTER SYSTEM SET common_user_prefix='' scope=spfile;
 
/
Grant CREATE session TO royalRoots;
 
/
Grant DBA to royalRoots;
 
/
Grant resource to royalRoots;
/
GRANT CONNECT TO royalRoots; 
/
--ver tablespace
select tablespace_name, file_name, bytes /1024/1024 as size_mb
from dba_data_files;

GRANT SET CONTAINER TO ROYALROOTS;


--SOLUCIONES A PROBLEMAS
ALTER SESSION SET CONTAINER = XEPDB1;

ALTER USER ROYALROOTS
DEFAULT TABLESPACE FIDE_ROYALROOTS_TBS;

SELECT TABLESPACE_NAME, FILE_NAME
FROM DBA_DATA_FILES;


CREATE TABLESPACE FIDE_ROYALROOTS_TBS
datafile 'C:\APP\SPINA\PRODUCT\21C\ORADATA\XE\XEPDB1\FIDE_ROYALROOTS_TBS.DBF' size 100M;

--AUDITORIA
GRANT AUDIT_ADMIN TO ROYALROOTS;
