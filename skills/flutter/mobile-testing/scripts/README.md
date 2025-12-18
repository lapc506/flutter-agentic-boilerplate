# Scripts de Validación de Configuración Android

Este directorio contiene scripts para validar que la configuración de Android SDK esté correcta antes de ejecutar pruebas de integración móvil.

## Scripts Disponibles

### `validate_android_setup_linux.sh` (Bash/Linux)

Script de validación específico para sistemas Linux que verifica:

- ✅ Variables de entorno `ANDROID_HOME` o `ANDROID_SDK_ROOT`
- ✅ `adb` (Android Debug Bridge) en PATH
- ✅ `emulator` (Android Emulator) en PATH
- ✅ `avdmanager` (AVD Manager) disponible
- ✅ AVDs (Android Virtual Devices) creados
- ✅ Dispositivos conectados

**Uso:**
```bash
# Dar permisos de ejecución
chmod +x validate_android_setup_linux.sh

# Ejecutar
./validate_android_setup_linux.sh
```

### `validate_android_setup_macos.sh` (Bash/macOS)

Script de validación específico para macOS que verifica los mismos componentes, optimizado para las rutas comunes de macOS.

**Uso:**
```bash
# Dar permisos de ejecución
chmod +x validate_android_setup_macos.sh

# Ejecutar
./validate_android_setup_macos.sh
```

### `validate_android_setup.ps1` (PowerShell/Windows)

Script de validación para Windows que verifica los mismos componentes.

**Uso:**
```powershell
# Ejecutar desde PowerShell
.\validate_android_setup.ps1

# O con política de ejecución
powershell -ExecutionPolicy Bypass -File .\validate_android_setup.ps1
```

## Diferencias entre Linux y macOS

Los scripts de Linux y macOS son similares pero tienen diferencias en:

- **Rutas de detección automática**: 
  - Linux: `$HOME/Android/Sdk`, `/opt/android-sdk`, `/usr/local/android-sdk`
  - macOS: `$HOME/Library/Android/sdk`, `$HOME/Android/Sdk`, `/opt/android-sdk`
- **Archivos de configuración recomendados**:
  - Linux: `~/.bashrc` o `~/.zshrc`
  - macOS: `~/.zshrc` (macOS usa zsh por defecto) o `~/.bash_profile`

## Qué Verifican los Scripts

### 1. Variables de Entorno
- `ANDROID_HOME` o `ANDROID_SDK_ROOT` configuradas
- Detección automática en ubicaciones comunes si no están configuradas

### 2. Herramientas en PATH
- **adb**: Android Debug Bridge para comunicación con dispositivos
- **emulator**: Android Emulator para ejecutar AVDs
- **avdmanager**: Herramienta para gestionar AVDs

### 3. AVDs Disponibles
- Lista todos los AVDs creados
- Muestra cuántos están disponibles

### 4. Dispositivos Conectados
- Lista dispositivos físicos y emuladores conectados
- Verifica que `adb` puede comunicarse con ellos

## Salida del Script

Los scripts proporcionan:

- ✅ **Verde**: Configuración correcta
- ⚠️ **Amarillo**: Advertencias (configuración funcional pero mejorable)
- ❌ **Rojo**: Errores (configuración incorrecta)

### Ejemplo de Salida Exitosa

```
🔍 Validando configuración de Android SDK (Linux)...

📦 Verificando variables de entorno Android...
✅ ANDROID_HOME está configurado: /home/user/Android/Sdk

🔧 Verificando adb (Android Debug Bridge)...
✅ adb encontrado en PATH: /home/user/Android/Sdk/platform-tools/adb
   Versión: Android Debug Bridge version 1.0.41

📱 Verificando emulator (Android Emulator)...
✅ emulator encontrado en PATH: /home/user/Android/Sdk/emulator/emulator

📋 Verificando avdmanager (AVD Manager)...
✅ avdmanager encontrado: /home/user/Android/Sdk/cmdline-tools/latest/bin/avdmanager

📱 Verificando AVDs (Android Virtual Devices)...
✅ Se encontraron 2 AVD(s):
   - Pixel_5_API_33
   - Pixel_7_API_34

🔌 Verificando dispositivos conectados...
✅ Se encontraron 1 dispositivo(s) conectado(s):
   emulator-5554    device

📊 Resumen:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Todo está correctamente configurado!
```

## Solución de Problemas

### Error: "adb no está en PATH"

**Linux:**
```bash
# Agregar a ~/.bashrc o ~/.zshrc
export ANDROID_HOME=$HOME/Android/Sdk
export PATH=$PATH:$ANDROID_HOME/platform-tools
export PATH=$PATH:$ANDROID_HOME/emulator
```

**macOS:**
```bash
# Agregar a ~/.zshrc o ~/.bash_profile
export ANDROID_HOME=$HOME/Library/Android/sdk
export PATH=$PATH:$ANDROID_HOME/platform-tools
export PATH=$PATH:$ANDROID_HOME/emulator
```

### Error: "emulator no está en PATH"

**Solución:**
```bash
export PATH=$PATH:$ANDROID_HOME/emulator
```

### Error: "No se encontraron AVDs"

**Solución:**
1. Abre Android Studio
2. Ve a Tools > Device Manager
3. Crea un nuevo AVD
4. O usa `avdmanager` desde la línea de comandos

### Windows: Problemas con PowerShell

Si tienes problemas de ejecución en PowerShell:

```powershell
# Verificar política de ejecución
Get-ExecutionPolicy

# Cambiar política temporalmente (solo para este script)
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\validate_android_setup.ps1
```

## Integración con CI/CD

Estos scripts pueden usarse en pipelines de CI/CD para validar el entorno antes de ejecutar tests:

```yaml
# Ejemplo para GitHub Actions (Linux)
- name: Validate Android Setup
  run: |
    chmod +x scripts/validate_android_setup_linux.sh
    ./scripts/validate_android_setup_linux.sh

# Ejemplo para GitHub Actions (macOS)
- name: Validate Android Setup
  run: |
    chmod +x scripts/validate_android_setup_macos.sh
    ./scripts/validate_android_setup_macos.sh
```

## Referencias

- [Android SDK Setup Guide](https://developer.android.com/studio/command-line)
- [Flutter Android Setup](https://docs.flutter.dev/get-started/install)
- [AVD Manager Documentation](https://developer.android.com/studio/run/managing-avds)

