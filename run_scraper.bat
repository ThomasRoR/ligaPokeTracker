@echo off
echo ===================================================
echo   Pokemon Price Tracker - Local Scraper
echo ===================================================
echo Conectando ao Supabase e extraindo dados...

:: Carregando as variaveis de ambiente do arquivo .env
for /F "tokens=*" %%I in (.env) do set %%I

:: Ativando o ambiente virtual, instalando dependencias e rodando o script
call .\venv\Scripts\activate.bat
python -m pip install -r scraper\requirements.txt
python -m playwright install chromium
python -m scraper.pipeline

echo.
echo Processo concluido!
pause
