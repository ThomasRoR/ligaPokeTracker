@echo off
echo ===================================================
echo   Pokemon Price Tracker - Local Scraper
echo ===================================================
echo Conectando ao Supabase e extraindo dados...

:: Carregando as variaveis de ambiente do arquivo .env
for /F "tokens=*" %%I in (.env) do set %%I

:: Fechando qualquer instancia do Chrome rodando em segundo plano para poder abrir com a porta de depuração
taskkill /F /IM chrome.exe /T >nul 2>&1

:: Abrindo o seu Google Chrome original com a porta de automação aberta
echo Iniciando o seu Google Chrome...
start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --remote-allow-origins="*"

:: Esperando o Chrome abrir
timeout /t 3 /nobreak >nul

:: Ativando o ambiente virtual, instalando dependencias e rodando o script
call .\venv\Scripts\activate.bat
python -m pip install -r scraper\requirements.txt
python -m scraper.pipeline

echo.
echo Processo concluido!
pause
