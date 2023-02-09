@echo off

SET CUR_YEAR=%date:~6,4%
SET /a NEX_YEAR=%CUR_YEAR% + 1

SET DATE_START=%CUR_YEAR%-01-01
SET DATE_END=%NEX_YEAR%-01-01
SET API_URL=https://mia.mobil.knute.edu.ua

SET SCRIPT_DIR=%~dp0
SET ROOT_DIR=%~dp0..

:: Check if cache is installed
if exist "%ROOT_DIR%\cache\temp-mkr-cache.loaded" (
    call :setup_cache || exit 1
    exit 0
)

call :clear_temp_cache

:: Install cacher if not installed
echo Installing cacher
start cmd /k call "%SCRIPT_DIR%install-cacher.bat" -y || (
    echo Failed to install cacher
    exit 1
) && echo Cacher installed

:: Load cache
"%ROOT_DIR%\bin\cacher.exe" -url=%API_URL% -dateStart=%DATE_START% -dateEnd=%DATE_END% -output="%ROOT_DIR%\cache\temp-mkr-cache.sqlite" || (
    echo Failed to load cache
    call :clear_temp_cache
    exit 1
)

call :setup_cache || exit 1


:: Setup cache file
:setup_cache
echo Setting up cache file
move "%ROOT_DIR%\cache\temp-mkr-cache.sqlite" "%ROOT_DIR%\cache\mkr-cache.sqlite" || (
    echo Failed to setup cache file. Perhaps you forgot to stop the bot first?
    copy /y NUL "%ROOT_DIR%\cache\temp-mkr-cache.loaded" > NUL
    exit /b 1
)
call :clear_temp_cache
echo Done
exit /b 0

:: Function that clears broken cache in case of error
:clear_temp_cache
echo Clearing temp cache
del "%ROOT_DIR%\cache\temp-mkr-cache.*" 2>nul || (
    echo Failed to clear cache
    exit /b 1
)
exit /b 0
