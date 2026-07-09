@echo off
setlocal EnableDelayedExpansion

REM zig-stdlib-io-writer-buffer-lab runner (Windows)
REM https://github.com/necat101/zig-stdlib-io-writer-buffer-lab

cd /d "%~dp0"

REM --- Find Python ---
where python >nul 2>&1
if %errorlevel% neq 0 (
  where python3 >nul 2>&1
  if %errorlevel% neq 0 (
    echo error: python not found in PATH
    echo   install Python 3 from https://www.python.org/
    exit /b 1
  )
  set "PY=python3"
) else (
  set "PY=python"
)

REM --- Find Zig ---
set "ZIG_BIN="
if defined ZIG_BIN if exist "%ZIG_BIN%" goto zig_found
if exist "%~dp0zig.exe" set "ZIG_BIN=%~dp0zig.exe" & goto zig_found
where zig >nul 2>&1
if %errorlevel% equ 0 set "ZIG_BIN=zig" & goto zig_found
for %%p in (
  "C:\zig\zig.exe"
  "C:\Program Files\zig\zig.exe"
  "%LOCALAPPDATA%\Programs\zig\zig.exe"
  "%USERPROFILE%\scoop\apps\zig\current\zig.exe"
) do if exist %%~p set "ZIG_BIN=%%~p" & goto zig_found

echo warning: zig not found – compiler validation will be skipped
echo   install Zig 0.16.0+ from https://ziglang.org/download/
echo   or set ZIG_BIN=C:\path\to\zig.exe
echo.
goto skip_zig_check

:zig_found
echo Using Zig:
"%ZIG_BIN%" version
echo.

:skip_zig_check

echo ==^> py_compile generate_cases.py run_lab.py
%PY% -m py_compile generate_cases.py run_lab.py
if %errorlevel% neq 0 exit /b %errorlevel%

echo ==^> generate_cases.py
%PY% generate_cases.py
if %errorlevel% neq 0 exit /b %errorlevel%

REM --- Fix Zig string literal newline bug ---
if exist fix_zig_newlines.py (
  echo ==^> fix_zig_newlines.py generated_cases
  %PY% fix_zig_newlines.py generated_cases
)

echo ==^> run_lab.py
%PY% run_lab.py
if %errorlevel% neq 0 exit /b %errorlevel%

echo.
echo Done.
echo   RESULTS.md
echo   results_rows.json / results_rows.csv
echo   cases.json
echo   generated_cases\*.zig
echo.
echo To verify a fresh clone:
echo   type VERIFY.md
echo.
