# Script de validación para configuración de Android SDK (PowerShell)
# Verifica que adb y AVD estén correctamente configurados en PATH

$ErrorActionPreference = "Continue"
$Errors = 0
$Warnings = 0

Write-Host "🔍 Validando configuración de Android SDK..." -ForegroundColor Cyan
Write-Host ""

# Función para imprimir éxito
function Print-Success {
    param([string]$Message)
    Write-Host "✅ $Message" -ForegroundColor Green
}

# Función para imprimir error
function Print-Error {
    param([string]$Message)
    Write-Host "❌ $Message" -ForegroundColor Red
    $script:Errors++
}

# Función para imprimir advertencia
function Print-Warning {
    param([string]$Message)
    Write-Host "⚠️  $Message" -ForegroundColor Yellow
    $script:Warnings++
}

# 1. Verificar ANDROID_HOME o ANDROID_SDK_ROOT
Write-Host "📦 Verificando variables de entorno Android..." -ForegroundColor Cyan

$AndroidSdkPath = $null

if ($env:ANDROID_HOME) {
    Print-Success "ANDROID_HOME está configurado: $env:ANDROID_HOME"
    $AndroidSdkPath = $env:ANDROID_HOME
}
elseif ($env:ANDROID_SDK_ROOT) {
    Print-Success "ANDROID_SDK_ROOT está configurado: $env:ANDROID_SDK_ROOT"
    $AndroidSdkPath = $env:ANDROID_SDK_ROOT
}
else {
    Print-Warning "ANDROID_HOME o ANDROID_SDK_ROOT no están configurados"
    Print-Warning "Intentando detectar desde ubicaciones comunes..."
    
    # Intentar detectar en ubicaciones comunes
    $CommonPaths = @(
        "$env:LOCALAPPDATA\Android\Sdk",
        "$env:USERPROFILE\AppData\Local\Android\Sdk",
        "$env:ProgramFiles\Android\Sdk",
        "C:\Android\Sdk"
    )
    
    $Found = $false
    foreach ($path in $CommonPaths) {
        if (Test-Path $path) {
            Print-Success "Android SDK detectado en: $path"
            $AndroidSdkPath = $path
            $Found = $true
            break
        }
    }
    
    if (-not $Found) {
        Print-Error "No se pudo detectar Android SDK. Configura ANDROID_HOME o ANDROID_SDK_ROOT"
    }
}

Write-Host ""

# 2. Verificar adb en PATH
Write-Host "🔧 Verificando adb (Android Debug Bridge)..." -ForegroundColor Cyan

$AdbPath = Get-Command adb -ErrorAction SilentlyContinue
if ($AdbPath) {
    $AdbVersion = adb version 2>&1 | Select-Object -First 1
    Print-Success "adb encontrado en PATH: $($AdbPath.Source)"
    Write-Host "   Versión: $AdbVersion"
}
else {
    Print-Error "adb no está en PATH"
    
    # Intentar encontrar adb en ANDROID_SDK_PATH
    if ($AndroidSdkPath) {
        $AdbCandidates = @(
            "$AndroidSdkPath\platform-tools\adb.exe",
            "$AndroidSdkPath\tools\adb.exe"
        )
        
        foreach ($adbCandidate in $AdbCandidates) {
            if (Test-Path $adbCandidate) {
                Print-Warning "adb encontrado pero no en PATH: $adbCandidate"
                Print-Warning "Agrega a PATH: $AndroidSdkPath\platform-tools"
                break
            }
        }
    }
}

Write-Host ""

# 3. Verificar emulator en PATH
Write-Host "📱 Verificando emulator (Android Emulator)..." -ForegroundColor Cyan

$EmulatorPath = Get-Command emulator -ErrorAction SilentlyContinue
if ($EmulatorPath) {
    Print-Success "emulator encontrado en PATH: $($EmulatorPath.Source)"
}
else {
    Print-Error "emulator no está en PATH"
    
    # Intentar encontrar emulator en ANDROID_SDK_PATH
    if ($AndroidSdkPath) {
        $EmulatorCandidates = @(
            "$AndroidSdkPath\emulator\emulator.exe",
            "$AndroidSdkPath\tools\emulator.exe"
        )
        
        foreach ($emulatorCandidate in $EmulatorCandidates) {
            if (Test-Path $emulatorCandidate) {
                Print-Warning "emulator encontrado pero no en PATH: $emulatorCandidate"
                Print-Warning "Agrega a PATH: $AndroidSdkPath\emulator"
                break
            }
        }
    }
}

Write-Host ""

# 4. Verificar avdmanager
Write-Host "📋 Verificando avdmanager (AVD Manager)..." -ForegroundColor Cyan

if ($AndroidSdkPath) {
    $AvdManagerCandidates = @(
        "$AndroidSdkPath\cmdline-tools\latest\bin\avdmanager.bat",
        "$AndroidSdkPath\tools\bin\avdmanager.bat"
    )
    
    $Found = $false
    foreach ($avdManagerCandidate in $AvdManagerCandidates) {
        if (Test-Path $avdManagerCandidate) {
            Print-Success "avdmanager encontrado: $avdManagerCandidate"
            $Found = $true
            break
        }
    }
    
    if (-not $Found) {
        Print-Warning "avdmanager no encontrado. Puede que necesites instalar Command-line Tools"
    }
}
else {
    Print-Warning "No se puede verificar avdmanager sin ANDROID_HOME configurado"
}

Write-Host ""

# 5. Verificar AVDs disponibles
Write-Host "📱 Verificando AVDs (Android Virtual Devices)..." -ForegroundColor Cyan

$AvdList = $null
if ($EmulatorPath) {
    try {
        $AvdList = emulator -list-avds 2>&1
        if ($AvdList -and $AvdList.Count -gt 0) {
            $AvdCount = ($AvdList | Where-Object { $_ -match '\S' }).Count
            Print-Success "Se encontraron $AvdCount AVD(s):"
            $AvdList | Where-Object { $_ -match '\S' } | ForEach-Object { Write-Host "   - $_" }
        }
        else {
            Print-Warning "No se encontraron AVDs. Crea uno usando Android Studio o avdmanager"
        }
    }
    catch {
        Print-Warning "Error al listar AVDs: $_"
    }
}
elseif ($AndroidSdkPath -and (Test-Path "$AndroidSdkPath\emulator\emulator.exe")) {
    try {
        $AvdList = & "$AndroidSdkPath\emulator\emulator.exe" -list-avds 2>&1
        if ($AvdList -and $AvdList.Count -gt 0) {
            $AvdCount = ($AvdList | Where-Object { $_ -match '\S' }).Count
            Print-Success "Se encontraron $AvdCount AVD(s):"
            $AvdList | Where-Object { $_ -match '\S' } | ForEach-Object { Write-Host "   - $_" }
        }
        else {
            Print-Warning "No se encontraron AVDs"
        }
    }
    catch {
        Print-Warning "Error al listar AVDs: $_"
    }
}
else {
    Print-Warning "No se puede listar AVDs sin emulator en PATH"
}

Write-Host ""

# 6. Verificar dispositivos conectados
Write-Host "🔌 Verificando dispositivos conectados..." -ForegroundColor Cyan

if ($AdbPath) {
    try {
        $DevicesOutput = adb devices 2>&1
        $Devices = $DevicesOutput | Where-Object { $_ -match 'device$' -or $_ -match 'emulator' }
        if ($Devices) {
            $DeviceCount = ($Devices | Measure-Object).Count
            Print-Success "Se encontraron $DeviceCount dispositivo(s) conectado(s):"
            $Devices | ForEach-Object { Write-Host "   $_" }
        }
        else {
            Print-Warning "No hay dispositivos conectados"
        }
    }
    catch {
        Print-Warning "Error al verificar dispositivos: $_"
    }
}
else {
    Print-Warning "No se puede verificar dispositivos sin adb en PATH"
}

Write-Host ""

# 7. Resumen y recomendaciones
Write-Host "📊 Resumen:" -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if ($Errors -eq 0 -and $Warnings -eq 0) {
    Write-Host "✅ Todo está correctamente configurado!" -ForegroundColor Green
    exit 0
}
elseif ($Errors -eq 0) {
    Write-Host "⚠️  Configuración funcional pero con advertencias" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Recomendaciones:" -ForegroundColor Cyan
    Write-Host "1. Configura ANDROID_HOME o ANDROID_SDK_ROOT en variables de entorno del sistema:"
    Write-Host "   [System.Environment]::SetEnvironmentVariable('ANDROID_HOME', 'C:\Users\$env:USERNAME\AppData\Local\Android\Sdk', 'User')"
    Write-Host ""
    Write-Host "2. Agrega las herramientas a PATH:"
    Write-Host "   [System.Environment]::SetEnvironmentVariable('Path', `$env:Path + ';' + `$env:ANDROID_HOME + '\platform-tools', 'User')"
    Write-Host "   [System.Environment]::SetEnvironmentVariable('Path', `$env:Path + ';' + `$env:ANDROID_HOME + '\emulator', 'User')"
    Write-Host "   [System.Environment]::SetEnvironmentVariable('Path', `$env:Path + ';' + `$env:ANDROID_HOME + '\tools', 'User')"
    Write-Host "   [System.Environment]::SetEnvironmentVariable('Path', `$env:Path + ';' + `$env:ANDROID_HOME + '\tools\bin', 'User')"
    Write-Host ""
    Write-Host "3. Reinicia PowerShell o recarga las variables:"
    Write-Host "   `$env:Path = [System.Environment]::GetEnvironmentVariable('Path', 'User') + ';' + [System.Environment]::GetEnvironmentVariable('Path', 'Machine')"
    exit 0
}
else {
    Write-Host "❌ Se encontraron $Errors error(es) y $Warnings advertencia(s)" -ForegroundColor Red
    Write-Host ""
    Write-Host "Pasos para corregir:" -ForegroundColor Cyan
    Write-Host "1. Instala Android SDK si no lo tienes"
    Write-Host "2. Configura ANDROID_HOME apuntando a la ubicación del SDK"
    Write-Host "3. Agrega las herramientas a PATH (ver arriba)"
    Write-Host "4. Reinicia PowerShell"
    exit 1
}

