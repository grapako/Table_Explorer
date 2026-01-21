@echo off
setlocal EnableDelayedExpansion
pushd %~dp0

REM =========================================
REM CONFIGURACION
REM =========================================
set "ENV_NAME=JIP_env"
set "SCRIPT_FILE=table_explorer.py"
set "SCRIPT_PATH=%~dp0%SCRIPT_FILE%"

echo --- Buscando entorno Conda y preparando ejecucion ---

REM ----------------------------------------------------
REM 1. DETECCION INTELIGENTE DE CONDA
REM ----------------------------------------------------
set "TEMP_ACTIVATE="

REM A) Intentar encontrar conda en el PATH
for /f "delims=" %%C in ('where conda 2^>nul') do (
    set "CONDA_EXE=%%C"
    set "CONDA_ROOT=%%~dpC"
    
    REM Caso 1: conda esta en 'Scripts' -> activate esta ahi mismo
    if exist "!CONDA_ROOT!activate.bat" (
        set "TEMP_ACTIVATE=!CONDA_ROOT!activate.bat"
        goto :FOUND_CONDA
    )
    
    REM Caso 2: conda esta en 'condabin' -> activate podria estar ahi o en ../Scripts
    if exist "!CONDA_ROOT!..\Scripts\activate.bat" (
        set "TEMP_ACTIVATE=!CONDA_ROOT!..\Scripts\activate.bat"
        goto :FOUND_CONDA
    )
    
    REM Caso 3: activate en condabin (menos comun pero posible)
    if exist "!CONDA_ROOT!activate.bat" (
        set "TEMP_ACTIVATE=!CONDA_ROOT!activate.bat"
        goto :FOUND_CONDA
    )
)

REM B) Buscar en rutas estandar si no esta en PATH
set "POSSIBLE_PATHS=%USERPROFILE%\Anaconda3\Scripts;C:\ProgramData\Anaconda3\Scripts;%USERPROFILE%\Miniconda3\Scripts;C:\ProgramData\Miniconda3\Scripts;C:\Anaconda3\Scripts;C:\Miniconda3\Scripts"

for %%P in (%POSSIBLE_PATHS%) do (
    if exist "%%P\activate.bat" (
        set "TEMP_ACTIVATE=%%P\activate.bat"
        goto :FOUND_CONDA
    )
)

echo [AVISO] No se encontro una instalacion de Conda automatica.
echo Se intentara usar el Python del sistema (si existe).
REM Si no encontramos conda, cerramos delayed expansion antes de seguir
REM También preservamos las variables de configuración
endlocal & set "ENV_NAME=%ENV_NAME%" & set "SCRIPT_FILE=%SCRIPT_FILE%" & set "SCRIPT_PATH=%SCRIPT_PATH%"
goto :RUN_PYTHON

:FOUND_CONDA
REM ==============================================================================
REM TRUCO CRITICO: Cerrar EnableDelayedExpansion antes de llamar a activate.bat
REM CORRECCION: Debemos pasar las variables ENV_NAME y SCRIPT_PATH fuera del scope local
REM ==============================================================================
endlocal & set "ACTIVATE_BAT=%TEMP_ACTIVATE%" & set "ENV_NAME=%ENV_NAME%" & set "SCRIPT_FILE=%SCRIPT_FILE%" & set "SCRIPT_PATH=%SCRIPT_PATH%"

echo [INFO] Conda detectado en: "%ACTIVATE_BAT%"
echo [INFO] Activando entorno: "%ENV_NAME%"

REM Activamos el entorno
call "%ACTIVATE_BAT%" %ENV_NAME%
if errorlevel 1 (
    echo [ERROR] Fallo la activacion del entorno. Verifica que '%ENV_NAME%' exista.
    echo Se intentara continuar con el Python base...
    pause
)

:RUN_PYTHON
REM ----------------------------------------------------
REM 2. EJECUCION DEL SCRIPT
REM ----------------------------------------------------
echo.
echo Ejecutando: %SCRIPT_FILE%
echo ----------------------------------------------------

if not exist "%SCRIPT_PATH%" (
    echo [ERROR FATAL] No se encuentra el archivo: %SCRIPT_PATH%
    pause
    exit /b 1
)

python "%SCRIPT_PATH%"

echo.
echo ----------------------------------------------------
echo Ejecucion finalizada.
pause