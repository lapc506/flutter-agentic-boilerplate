# Script de configuración para Flutter Boilerplate Monorepo
# Este script inicializa un proyecto Flutter en una estructura de monorepo

param(
    [string]$ProjectName = ""
)

# Configurar política de ejecución para este script
$ErrorActionPreference = "Stop"

# Cambiar al directorio raíz del proyecto (donde está este script)
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = Split-Path -Parent $scriptPath
Set-Location $projectRoot

# Colores para output (PowerShell)
function Write-Info {
    param([string]$Message)
    Write-Host "[INFO] $Message" -ForegroundColor Cyan
}

function Write-Success {
    param([string]$Message)
    Write-Host "[SUCCESS] $Message" -ForegroundColor Green
}

function Write-Warning {
    param([string]$Message)
    Write-Host "[WARNING] $Message" -ForegroundColor Yellow
}

function Write-Error {
    param([string]$Message)
    Write-Host "[ERROR] $Message" -ForegroundColor Red
}

# Verificar que Flutter esté instalado
function Test-Flutter {
    Write-Info "Verificando instalación de Flutter..."
    
    # Verificar si el comando flutter existe
    $flutterCommand = Get-Command flutter -ErrorAction SilentlyContinue
    if (-not $flutterCommand) {
        Write-Error "Flutter no está instalado o no está en el PATH"
        Write-Info "Por favor, instala Flutter desde: https://flutter.dev/docs/get-started/install"
        Write-Info "Asegúrate de agregar Flutter al PATH del sistema"
        exit 1
    }
    
    try {
        # Ejecutar flutter --version y capturar la salida
        $flutterOutput = flutter --version 2>&1
        $flutterExitCode = $LASTEXITCODE
        
        # Si hay error o el código de salida no es 0, verificar más
        if ($flutterExitCode -ne 0 -and $flutterExitCode -ne $null) {
            throw "Flutter no está disponible correctamente"
        }
        
        # Extraer la primera línea con la versión
        $flutterVersion = ($flutterOutput | Select-Object -First 1).ToString()
        if ([string]::IsNullOrWhiteSpace($flutterVersion)) {
            $flutterVersion = "Flutter instalado"
        }
        
        Write-Success "Flutter encontrado: $flutterVersion"
        
        # Verificar que Flutter esté configurado correctamente (sin mostrar toda la salida)
        Write-Info "Verificando configuración de Flutter..."
        $doctorOutput = flutter doctor 2>&1 | Out-Null
    }
    catch {
        Write-Error "Error al verificar Flutter: $_"
        Write-Info "Por favor, verifica que Flutter esté correctamente instalado y en el PATH"
        Write-Info "Puedes verificar ejecutando: flutter --version"
        exit 1
    }
}

# Obtener el nombre del proyecto
function Get-ProjectName {
    if ([string]::IsNullOrWhiteSpace($ProjectName)) {
        $input = Read-Host "Ingresa el nombre del proyecto (default: my_flutter_app)"
        if ([string]::IsNullOrWhiteSpace($input)) {
            $script:ProjectName = "my_flutter_app"
        } else {
            $script:ProjectName = $input
        }
    }
    Write-Info "Nombre del proyecto: $script:ProjectName"
}

# Crear estructura de directorios
function New-ProjectStructure {
    Write-Info "Creando estructura de monorepo..."
    
    # Crear directorio backend si no existe
    if (-not (Test-Path "backend")) {
        New-Item -ItemType Directory -Path "backend" -Force | Out-Null
        Write-Success "Directorio 'backend' creado"
    } else {
        Write-Warning "El directorio 'backend' ya existe"
    }
    
    # Crear directorio mobile si no existe
    if (-not (Test-Path "mobile")) {
        New-Item -ItemType Directory -Path "mobile" -Force | Out-Null
        Write-Success "Directorio 'mobile' creado"
    } else {
        Write-Warning "El directorio 'mobile' ya existe"
        $continue = Read-Host "¿Deseas continuar? Esto puede sobrescribir archivos existentes (y/n)"
        if ($continue -ne "y" -and $continue -ne "Y") {
            Write-Info "Operación cancelada"
            exit 0
        }
    }
}

# Crear proyecto Flutter
function New-FlutterProject {
    Write-Info "Creando proyecto Flutter en 'mobile/'..."
    
    Push-Location mobile
    
    try {
        # Verificar si ya existe un proyecto Flutter
        if (Test-Path "pubspec.yaml") {
            Write-Warning "Ya existe un proyecto Flutter en 'mobile/'"
            $recreate = Read-Host "¿Deseas recrear el proyecto? (y/n)"
            if ($recreate -ne "y" -and $recreate -ne "Y") {
                Write-Info "Manteniendo proyecto existente"
                Pop-Location
                return
            }
            # Limpiar directorio mobile (excepto .git si existe)
            Write-Info "Limpiando directorio mobile..."
            Get-ChildItem -Path . -Exclude ".git" | Remove-Item -Recurse -Force
        }
        
        # Crear proyecto Flutter
        Write-Info "Ejecutando 'flutter create .'..."
        flutter create . --project-name $script:ProjectName --org com.example
        
        if ($LASTEXITCODE -ne 0) {
            throw "Error al crear el proyecto Flutter"
        }
        
        Write-Success "Proyecto Flutter creado exitosamente"
    }
    finally {
        Pop-Location
    }
}

# Instalar dependencias
function Install-Dependencies {
    Write-Info "Instalando dependencias de Flutter..."
    
    Push-Location mobile
    
    try {
        flutter pub get
        if ($LASTEXITCODE -eq 0) {
            Write-Success "Dependencias instaladas correctamente"
        } else {
            throw "Error al instalar dependencias"
        }
    }
    finally {
        Pop-Location
    }
}

# Crear archivos de configuración adicionales
function New-ConfigFiles {
    Write-Info "Creando archivos de configuración..."
    
    Push-Location mobile
    
    try {
        # Crear directorio de assets si no existe
        if (-not (Test-Path "assets/icon")) {
            New-Item -ItemType Directory -Path "assets/icon" -Force | Out-Null
        }
        if (-not (Test-Path "assets/splash")) {
            New-Item -ItemType Directory -Path "assets/splash" -Force | Out-Null
        }
        
        # Crear .env-sample si no existe
        if (-not (Test-Path ".env-sample")) {
            $envSampleContent = @"
# Configuración de la aplicación
APP_NAME=$script:ProjectName
APP_VERSION=1.0.0

# API Configuration
API_BASE_URL=https://api.example.com
API_TIMEOUT=30000

# Firebase (opcional)
# FIREBASE_API_KEY=your_api_key_here
# FIREBASE_PROJECT_ID=your_project_id_here

# Otros servicios (opcional)
# ANALYTICS_ENABLED=true
# CRASH_REPORTING_ENABLED=true
"@
            Set-Content -Path ".env-sample" -Value $envSampleContent
            Write-Success "Archivo .env-sample creado"
        }
        
        # Crear .gitignore si no existe o actualizar
        if (-not (Test-Path ".gitignore")) {
            $gitignoreContent = @"
# Flutter/Dart/Pub related
**/doc/api/
**/ios/Flutter/.last_build_id
.dart_tool/
.flutter-plugins
.flutter-plugins-dependencies
.packages
.pub-cache/
.pub/
/build/

# Environment variables
.env
*.env
!*.env-sample
env.g.dart

# Firebase
**/ios/Runner/GoogleService-Info.plist
**/android/app/google-services.json

# IDE
.idea/
.vscode/
*.iml
*.ipr
*.iws

# OS
.DS_Store
Thumbs.db
"@
            Set-Content -Path ".gitignore" -Value $gitignoreContent
            Write-Success "Archivo .gitignore creado"
        }
    }
    finally {
        Pop-Location
    }
}

# Crear README para mobile
function New-MobileReadme {
    Write-Info "Creando README para mobile..."
    
    Push-Location mobile
    
    try {
        if (-not (Test-Path "README.md")) {
            $readmeContent = @"
# $script:ProjectName

Aplicación Flutter generada desde el boilerplate.

## Desarrollo

``````bash
# Instalar dependencias
flutter pub get

# Ejecutar en modo debug
flutter run

# Ejecutar tests
flutter test

# Generar build de Android
flutter build apk --release

# Generar build de iOS
flutter build ios --release
``````

## Configuración

1. Copia `.env-sample` a `.env` y configura tus variables de entorno
2. Configura Firebase si es necesario
3. Personaliza los iconos y splash screen
"@
            Set-Content -Path "README.md" -Value $readmeContent
            Write-Success "README.md creado para mobile"
        }
    }
    finally {
        Pop-Location
    }
}

# Resumen final
function Show-Summary {
    Write-Success "¡Configuración completada!"
    Write-Host ""
    Write-Host "Estructura del proyecto:"
    Write-Host "  ├── backend/          (directorio para tu backend)"
    Write-Host "  └── mobile/           (proyecto Flutter)"
    Write-Host ""
    Write-Host "Próximos pasos:"
    Write-Host "  1. cd mobile"
    Write-Host "  2. Copia .env-sample a .env y configura tus variables"
    Write-Host "  3. flutter pub get (si no se ejecutó automáticamente)"
    Write-Host "  4. Configura Firebase si es necesario"
    Write-Host "  5. Personaliza iconos y splash screen"
    Write-Host "  6. ¡Comienza a desarrollar!"
    Write-Host ""
    Write-Info "Para más información, consulta el README.md principal"
}

# Función principal
function Main {
    Write-Host ""
    Write-Host "=========================================="
    Write-Host "  Flutter Boilerplate Setup Script"
    Write-Host "=========================================="
    Write-Host ""
    
    Test-Flutter
    Get-ProjectName
    New-ProjectStructure
    New-FlutterProject
    Install-Dependencies
    New-ConfigFiles
    New-MobileReadme
    Show-Summary
}

# Ejecutar script principal
Main

