@echo off
REM Nombre del script: start_dev_server.bat
REM Propósito: Activa el entorno virtual de Python y arranca el servidor de desarrollo de Django.

REM --- CONFIGURACIÓN (Ajusta estas variables si es necesario) ---

REM Ruta al directorio del entorno virtual (relativa a la ubicación de este script .bat)
REM Asume que el venv está en una carpeta llamada "venv" o ".venv" dentro del directorio del proyecto.
SET VENV_DIR=venv

REM Nombre del script de activación del venv (generalmente 'activate.bat' en Windows)
SET VENV_ACTIVATE_SCRIPT=%VENV_DIR%\Scripts\activate.bat

REM Puerto para el servidor de desarrollo de Django (opcional, Django usa 8000 por defecto)
REM SET DJANGO_PORT=8000

REM Dirección IP para el servidor (opcional, 127.0.0.1 por defecto)
REM SET DJANGO_IP=127.0.0.1

REM --- FIN CONFIGURACIÓN ---

ECHO Iniciando TaskFlow Development Server...
ECHO.

REM Verificar si el directorio del proyecto actual es correcto (donde está manage.py)
IF NOT EXIST manage.py (
    ECHO ERROR: No se encontró 'manage.py' en el directorio actual.
    ECHO Asegúrate de ejecutar este script desde la raíz de tu proyecto Django.
    PAUSE
    EXIT /B 1
)

REM Verificar si existe el script de activación del venv
IF NOT EXIST "%VENV_ACTIVATE_SCRIPT%" (
    ECHO ERROR: No se encontró el script de activación del entorno virtual en:
    ECHO %VENV_ACTIVATE_SCRIPT%
    ECHO.
    ECHO Asegúrate de que el entorno virtual '%VENV_DIR%' exista y esté correctamente configurado.
    ECHO Si tu venv tiene otro nombre o ubicación, ajusta la variable VENV_DIR en este script.
    PAUSE
    EXIT /B 1
)

REM Activar el entorno virtual
ECHO Activando entorno virtual: %VENV_DIR%
CALL "%VENV_ACTIVATE_SCRIPT%"

IF ERRORLEVEL 1 (
    ECHO ERROR: Falló la activación del entorno virtual.
    PAUSE
    EXIT /B 1
)

ECHO Entorno virtual activado.
ECHO.

REM Navegar al directorio del proyecto Django si este script no está ya allí
REM (Esto es redundante si el script está en la raíz y ya verificamos manage.py,
REM pero lo dejamos por si se mueve el .bat a una subcarpeta del proyecto)
REM cd /d "%~dp0"

REM Iniciar el servidor de desarrollo de Django
ECHO Iniciando servidor de desarrollo de Django...
ECHO (Presiona CTRL+C para detener el servidor)
ECHO.

REM Construir el comando para runserver con IP y puerto opcionales
SET RUNSERVER_COMMAND=python manage.py runserver
IF DEFINED DJANGO_IP (
    IF DEFINED DJANGO_PORT (
        SET RUNSERVER_COMMAND=%RUNSERVER_COMMAND% %DJANGO_IP%:%DJANGO_PORT%
    ) ELSE (
        SET RUNSERVER_COMMAND=%RUNSERVER_COMMAND% %DJANGO_IP%:8000
    )
) ELSE (
    IF DEFINED DJANGO_PORT (
        SET RUNSERVER_COMMAND=%RUNSERVER_COMMAND% %DJANGO_PORT%
    )
)

REM Ejecutar el comando
%RUNSERVER_COMMAND%

ECHO.
ECHO Servidor de desarrollo detenido.

REM Opcional: Desactivar el entorno virtual (generalmente no es necesario ya que el cmd se cierra o vuelve al prompt original)
REM CALL deactivate

REM PAUSE
EXIT /B 0