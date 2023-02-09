@echo OFF

SET BIN_FILE=cacher.exe
SET TEMP_DIR=%TMP%\mkr-cacher

:: Read root dir path
if "%1" == "-y" (
    SET skip_input="true"
) else (
    SET skip_input="false"
)

SET DEF_ROOT_DIR=%~dp0..
if %skip_input% NEQ "true" (
    echo "Enter the path to the bot's root directory [default %DEF_ROOT_DIR%]"
    SET /p root_dir=">>> "
)

if ["%root_dir%"] == [] (
    SET root_dir=%DEF_ROOT_DIR%
)

if EXIST "%root_dir%\bin\%BIN_FILE%" (
    echo Module already installed. Exiting
    exit 0
)


echo Installing module

echo Cloning source code
git clone https://github.com/cubicbyte/mkr-cacher "%TEMP_DIR%"

echo Building module
cd /D %TEMP_DIR%
go build -o %BIN_FILE% main.go

if NOT EXIST "%root_dir%\bin" mkdir -p "%root_dir%\bin"
move %BIN_FILE% "%ROOT_DIR%\bin"
cd /D "%ROOT_DIR%"
rmdir /s /q "%TEMP_DIR%"

echo Done
