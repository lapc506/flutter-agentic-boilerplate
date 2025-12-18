#!/bin/bash

# Script de validación para configuración de Android SDK (macOS)
# Verifica que adb y AVD estén correctamente configurados en PATH

set -e

echo "🔍 Validando configuración de Android SDK (macOS)..."
echo ""

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Variables de estado
ERRORS=0
WARNINGS=0

# Función para imprimir éxito
print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

# Función para imprimir error
print_error() {
    echo -e "${RED}❌ $1${NC}"
    ERRORS=$((ERRORS + 1))
}

# Función para imprimir advertencia
print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
    WARNINGS=$((WARNINGS + 1))
}

# 1. Verificar ANDROID_HOME o ANDROID_SDK_ROOT
echo "📦 Verificando variables de entorno Android..."
if [ -n "$ANDROID_HOME" ]; then
    print_success "ANDROID_HOME está configurado: $ANDROID_HOME"
    ANDROID_SDK_PATH="$ANDROID_HOME"
elif [ -n "$ANDROID_SDK_ROOT" ]; then
    print_success "ANDROID_SDK_ROOT está configurado: $ANDROID_SDK_ROOT"
    ANDROID_SDK_PATH="$ANDROID_SDK_ROOT"
else
    print_warning "ANDROID_HOME o ANDROID_SDK_ROOT no están configurados"
    print_warning "Intentando detectar desde ubicaciones comunes de macOS..."
    
    # Intentar detectar en ubicaciones comunes de macOS
    COMMON_PATHS=(
        "$HOME/Library/Android/sdk"
        "$HOME/Android/Sdk"
        "/opt/android-sdk"
        "/usr/local/android-sdk"
    )
    
    FOUND=false
    for path in "${COMMON_PATHS[@]}"; do
        if [ -d "$path" ]; then
            print_success "Android SDK detectado en: $path"
            ANDROID_SDK_PATH="$path"
            FOUND=true
            break
        fi
    done
    
    if [ "$FOUND" = false ]; then
        print_error "No se pudo detectar Android SDK. Configura ANDROID_HOME o ANDROID_SDK_ROOT"
        ANDROID_SDK_PATH=""
    fi
fi

echo ""

# 2. Verificar adb en PATH
echo "🔧 Verificando adb (Android Debug Bridge)..."
if command -v adb &> /dev/null; then
    ADB_PATH=$(which adb)
    ADB_VERSION=$(adb version | head -n 1)
    print_success "adb encontrado en PATH: $ADB_PATH"
    echo "   Versión: $ADB_VERSION"
else
    print_error "adb no está en PATH"
    
    # Intentar encontrar adb en ANDROID_SDK_PATH
    if [ -n "$ANDROID_SDK_PATH" ]; then
        ADB_CANDIDATES=(
            "$ANDROID_SDK_PATH/platform-tools/adb"
            "$ANDROID_SDK_PATH/tools/adb"
        )
        
        for adb_path in "${ADB_CANDIDATES[@]}"; do
            if [ -f "$adb_path" ] && [ -x "$adb_path" ]; then
                print_warning "adb encontrado pero no en PATH: $adb_path"
                print_warning "Agrega a PATH: export PATH=\"\$PATH:$ANDROID_SDK_PATH/platform-tools\""
                break
            fi
        done
    fi
fi

echo ""

# 3. Verificar emulator en PATH
echo "📱 Verificando emulator (Android Emulator)..."
if command -v emulator &> /dev/null; then
    EMULATOR_PATH=$(which emulator)
    print_success "emulator encontrado en PATH: $EMULATOR_PATH"
else
    print_error "emulator no está en PATH"
    
    # Intentar encontrar emulator en ANDROID_SDK_PATH
    if [ -n "$ANDROID_SDK_PATH" ]; then
        EMULATOR_CANDIDATES=(
            "$ANDROID_SDK_PATH/emulator/emulator"
            "$ANDROID_SDK_PATH/tools/emulator"
        )
        
        for emulator_path in "${EMULATOR_CANDIDATES[@]}"; do
            if [ -f "$emulator_path" ] && [ -x "$emulator_path" ]; then
                print_warning "emulator encontrado pero no en PATH: $emulator_path"
                print_warning "Agrega a PATH: export PATH=\"\$PATH:$ANDROID_SDK_PATH/emulator\""
                break
            fi
        done
    fi
fi

echo ""

# 4. Verificar avdmanager
echo "📋 Verificando avdmanager (AVD Manager)..."
if [ -n "$ANDROID_SDK_PATH" ]; then
    AVDMANAGER_CANDIDATES=(
        "$ANDROID_SDK_PATH/cmdline-tools/latest/bin/avdmanager"
        "$ANDROID_SDK_PATH/tools/bin/avdmanager"
    )
    
    FOUND=false
    for avdmanager_path in "${AVDMANAGER_CANDIDATES[@]}"; do
        if [ -f "$avdmanager_path" ] && [ -x "$avdmanager_path" ]; then
            print_success "avdmanager encontrado: $avdmanager_path"
            FOUND=true
            break
        fi
    done
    
    if [ "$FOUND" = false ]; then
        print_warning "avdmanager no encontrado. Puede que necesites instalar Command-line Tools"
    fi
else
    print_warning "No se puede verificar avdmanager sin ANDROID_HOME configurado"
fi

echo ""

# 5. Verificar AVDs disponibles
echo "📱 Verificando AVDs (Android Virtual Devices)..."
if command -v emulator &> /dev/null; then
    AVD_LIST=$(emulator -list-avds 2>/dev/null || echo "")
    if [ -n "$AVD_LIST" ]; then
        AVD_COUNT=$(echo "$AVD_LIST" | wc -l | tr -d ' ')
        print_success "Se encontraron $AVD_COUNT AVD(s):"
        echo "$AVD_LIST" | sed 's/^/   - /'
    else
        print_warning "No se encontraron AVDs. Crea uno usando Android Studio o avdmanager"
    fi
elif [ -n "$ANDROID_SDK_PATH" ] && [ -f "$ANDROID_SDK_PATH/emulator/emulator" ]; then
    AVD_LIST=$("$ANDROID_SDK_PATH/emulator/emulator" -list-avds 2>/dev/null || echo "")
    if [ -n "$AVD_LIST" ]; then
        AVD_COUNT=$(echo "$AVD_LIST" | wc -l | tr -d ' ')
        print_success "Se encontraron $AVD_COUNT AVD(s):"
        echo "$AVD_LIST" | sed 's/^/   - /'
    else
        print_warning "No se encontraron AVDs"
    fi
else
    print_warning "No se puede listar AVDs sin emulator en PATH"
fi

echo ""

# 6. Verificar dispositivos conectados
echo "🔌 Verificando dispositivos conectados..."
if command -v adb &> /dev/null; then
    DEVICES=$(adb devices 2>/dev/null | grep -v "List of devices" | grep "device$" | wc -l | tr -d ' ')
    if [ "$DEVICES" -gt 0 ]; then
        print_success "Se encontraron $DEVICES dispositivo(s) conectado(s):"
        adb devices | grep -v "List of devices" | grep -E "(device|emulator)" | sed 's/^/   /'
    else
        print_warning "No hay dispositivos conectados"
    fi
else
    print_warning "No se puede verificar dispositivos sin adb en PATH"
fi

echo ""

# 7. Resumen y recomendaciones
echo "📊 Resumen:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    echo -e "${GREEN}✅ Todo está correctamente configurado!${NC}"
    exit 0
elif [ $ERRORS -eq 0 ]; then
    echo -e "${YELLOW}⚠️  Configuración funcional pero con advertencias${NC}"
    echo ""
    echo "Recomendaciones para macOS:"
    echo "1. Configura ANDROID_HOME en tu ~/.zshrc (macOS usa zsh por defecto) o ~/.bash_profile:"
    echo "   export ANDROID_HOME=\$HOME/Library/Android/sdk"
    echo ""
    echo "2. Agrega las herramientas a PATH:"
    echo "   export PATH=\"\$PATH:\$ANDROID_HOME/platform-tools\""
    echo "   export PATH=\"\$PATH:\$ANDROID_HOME/emulator\""
    echo "   export PATH=\"\$PATH:\$ANDROID_HOME/tools\""
    echo "   export PATH=\"\$PATH:\$ANDROID_HOME/tools/bin\""
    echo ""
    echo "3. Recarga la configuración:"
    echo "   source ~/.zshrc  # o source ~/.bash_profile"
    exit 0
else
    echo -e "${RED}❌ Se encontraron $ERRORS error(es) y $WARNINGS advertencia(s)${NC}"
    echo ""
    echo "Pasos para corregir:"
    echo "1. Instala Android SDK si no lo tienes"
    echo "2. Configura ANDROID_HOME apuntando a la ubicación del SDK"
    echo "3. Agrega las herramientas a PATH (ver arriba)"
    echo "4. Reinicia tu terminal o ejecuta: source ~/.zshrc"
    exit 1
fi

