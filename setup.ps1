<#
Simple Windows PowerShell setup script to create a venv and install dependencies.
Usage:
  .\setup.ps1            # create venv if missing and install requirements
  .\setup.ps1 -Recreate  # remove existing venv and recreate
#>

param(
    [switch]$Recreate
)

$ProjectRoot = Split-Path -Path $PSScriptRoot -Parent
Set-Location -Path $PSScriptRoot

$PythonPath = "C:\Users\busyp\AppData\Local\Programs\Python\Python312\python.exe"

if ($Recreate -and (Test-Path .\venv)) {
    Write-Output "Removing existing .\venv"
    Remove-Item -Recurse -Force .\venv
}

if (-not (Test-Path .\venv)) {
    Write-Output "Creating virtual environment .\venv using $PythonPath"
    & $PythonPath -m venv .\venv
} else {
    Write-Output "Virtual environment .\venv already exists"
}

Write-Output "Activating venv and installing packages"
. .\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r .\requirements.txt

Write-Output "Setup complete. Activate the venv with: .\venv\Scripts\Activate.ps1"