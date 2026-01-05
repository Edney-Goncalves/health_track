@echo off
title Health Track - Inicializador

echo ========================================
echo      INICIANDO HEALTH TRACK
echo ========================================

echo.
echo Verificando banco de dados...
python db_reader.py

if %errorlevel% neq 0 (
    echo.
    echo [ERRO] Falha ao acessar o banco de dados.
    pause
    exit /b %errorlevel%
)

echo.
echo Iniciando interface grafica...
python "Interface Grafica with db.py"

if %errorlevel% neq 0 (
    echo.
    echo [ERRO] Ocorreu um erro ao executar o sistema.
    pause
    exit /b %errorlevel%
)

echo.
echo Aplicacao encerrada.
pause
