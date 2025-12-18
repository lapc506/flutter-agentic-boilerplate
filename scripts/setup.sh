#!/bin/bash

# Script de configuración para Flutter Boilerplate Monorepo
# Este script inicializa un proyecto Flutter en una estructura de monorepo

set -e  # Salir si hay algún error

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para imprimir mensajes
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Verificar que Flutter esté instalado
check_flutter() {
    print_info "Verificando instalación de Flutter..."
    if ! command -v flutter &> /dev/null; then
        print_error "Flutter no está instalado o no está en el PATH"
        print_info "Por favor, instala Flutter desde: https://flutter.dev/docs/get-started/install"
        exit 1
    fi
    
    FLUTTER_VERSION=$(flutter --version | head -n 1)
    print_success "Flutter encontrado: $FLUTTER_VERSION"
    
    # Verificar que Flutter esté configurado correctamente
    print_info "Verificando configuración de Flutter..."
    if ! flutter doctor &> /dev/null; then
        print_warning "Ejecuta 'flutter doctor' para verificar la configuración completa"
    fi
}

# Obtener el nombre del proyecto
get_project_name() {
    if [ -z "$PROJECT_NAME" ]; then
        read -p "Ingresa el nombre del proyecto (default: my_flutter_app): " PROJECT_NAME
        PROJECT_NAME=${PROJECT_NAME:-my_flutter_app}
    fi
    print_info "Nombre del proyecto: $PROJECT_NAME"
}

# Crear estructura de directorios
create_structure() {
    print_info "Creando estructura de monorepo..."
    
    # Crear directorio backend si no existe
    if [ ! -d "backend" ]; then
        mkdir -p backend
        print_success "Directorio 'backend' creado"
    else
        print_warning "El directorio 'backend' ya existe"
    fi
    
    # Crear directorio mobile si no existe
    if [ ! -d "mobile" ]; then
        mkdir -p mobile
        print_success "Directorio 'mobile' creado"
    else
        print_warning "El directorio 'mobile' ya existe"
        read -p "¿Deseas continuar? Esto puede sobrescribir archivos existentes (y/n): " CONTINUE
        if [ "$CONTINUE" != "y" ] && [ "$CONTINUE" != "Y" ]; then
            print_info "Operación cancelada"
            exit 0
        fi
    fi
}

# Crear proyecto Flutter
create_flutter_project() {
    print_info "Creando proyecto Flutter en 'mobile/'..."
    
    cd mobile
    
    # Verificar si ya existe un proyecto Flutter
    if [ -f "pubspec.yaml" ]; then
        print_warning "Ya existe un proyecto Flutter en 'mobile/'"
        read -p "¿Deseas recrear el proyecto? (y/n): " RECREATE
        if [ "$RECREATE" != "y" ] && [ "$RECREATE" != "Y" ]; then
            print_info "Manteniendo proyecto existente"
            cd ..
            return
        fi
        # Limpiar directorio mobile (excepto .git si existe)
        print_info "Limpiando directorio mobile..."
        find . -mindepth 1 -maxdepth 1 ! -name '.git' -exec rm -rf {} +
    fi
    
    # Crear proyecto Flutter
    print_info "Ejecutando 'flutter create .'..."
    flutter create . --project-name "$PROJECT_NAME" --org com.example
    
    print_success "Proyecto Flutter creado exitosamente"
    cd ..
}

# Instalar dependencias
install_dependencies() {
    print_info "Instalando dependencias de Flutter..."
    cd mobile
    
    if flutter pub get; then
        print_success "Dependencias instaladas correctamente"
    else
        print_error "Error al instalar dependencias"
        cd ..
        exit 1
    fi
    
    cd ..
}

# Crear archivos de configuración adicionales
create_config_files() {
    print_info "Creando archivos de configuración..."
    cd mobile
    
    # Crear directorio de assets si no existe
    mkdir -p assets/icon
    mkdir -p assets/splash
    
    # Crear .env-sample si no existe
    if [ ! -f ".env-sample" ]; then
        cat > .env-sample << EOF
# Configuración de la aplicación
APP_NAME=$PROJECT_NAME
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
EOF
        print_success "Archivo .env-sample creado"
    fi
    
    # Crear .gitignore si no existe o actualizar
    if [ ! -f ".gitignore" ]; then
        cat > .gitignore << EOF
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
EOF
        print_success "Archivo .gitignore creado"
    fi
    
    cd ..
}

# Crear README para mobile
create_mobile_readme() {
    print_info "Creando README para mobile..."
    cd mobile
    
    if [ ! -f "README.md" ]; then
        cat > README.md << EOF
# $PROJECT_NAME

Aplicación Flutter generada desde el boilerplate.

## Desarrollo

\`\`\`bash
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
\`\`\`

## Configuración

1. Copia \`.env-sample\` a \`.env\` y configura tus variables de entorno
2. Configura Firebase si es necesario
3. Personaliza los iconos y splash screen
EOF
        print_success "README.md creado para mobile"
    fi
    
    cd ..
}

# Resumen final
print_summary() {
    print_success "¡Configuración completada!"
    echo ""
    echo "Estructura del proyecto:"
    echo "  ├── backend/          (directorio para tu backend)"
    echo "  └── mobile/           (proyecto Flutter)"
    echo ""
    echo "Próximos pasos:"
    echo "  1. cd mobile"
    echo "  2. Copia .env-sample a .env y configura tus variables"
    echo "  3. flutter pub get (si no se ejecutó automáticamente)"
    echo "  4. Configura Firebase si es necesario"
    echo "  5. Personaliza iconos y splash screen"
    echo "  6. ¡Comienza a desarrollar!"
    echo ""
    print_info "Para más información, consulta el README.md principal"
}

# Función principal
main() {
    echo ""
    echo "=========================================="
    echo "  Flutter Boilerplate Setup Script"
    echo "=========================================="
    echo ""
    
    check_flutter
    get_project_name
    create_structure
    create_flutter_project
    install_dependencies
    create_config_files
    create_mobile_readme
    print_summary
}

# Ejecutar script principal
main

