@echo off
for /f "usebackq delims=" %%i in (`"%ProgramFiles(x86)%\Microsoft Visual Studio\Installer\vswhere.exe" -products * -latest -property installationPath`) do set VS=%%i
call "%VS%\Common7\Tools\VsDevCmd.bat" -arch=x64 -host_arch=x64 -no_logo
cd /d %USERPROFILE%\Desktop\upm-alice
cmake --build out\build\x64-release-windows --target %* -- -k 0
echo salida compilar %ERRORLEVEL%
