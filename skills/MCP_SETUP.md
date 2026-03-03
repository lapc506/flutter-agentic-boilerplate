# 🔧 Configuración MCP para Múltiples IDEs

Este proyecto incluye un **único archivo `mcp.json`** en la raíz que puede ser usado por cualquier IDE o agente de IA que soporte el Model Context Protocol.

## 📍 Ubicación del Archivo

```
mcp.json  ← Archivo único en la raíz del proyecto
```

## 🤖 Configuración por IDE/Agente

### Cursor

Cursor detecta automáticamente `mcp.json` en la raíz del proyecto o en `.cursor/mcp.json`.

**Configuración automática (ya incluida):**
- `.cursor/mcp.json` → symlink a `mcp.json` (raíz)

**No requiere acción adicional.** El proyecto ya está configurado.

---

### Cline (VS Code Extension)

Cline busca `mcp.json` en `.cline/` o puede configurarse para usar el archivo raíz.

**Opción 1: Symlink (Recomendado)**
```bash
# En la raíz del proyecto
mkdir -p .cline
cd .cline
ln -s ../mcp.json mcp.json

# En Windows (PowerShell como Admin):
New-Item -ItemType Directory -Force -Path ".cline"
New-Item -ItemType SymbolicLink -Path ".cline\mcp.json" -Target "$PWD\mcp.json"
```

**Opción 2: Configuración en VS Code**
Agrega a `.vscode/settings.json`:
```json
{
  "cline.mcpConfigPath": "${workspaceFolder}/mcp.json"
}
```

---

### Windsurf

Windsurf busca configuración MCP en `.windsurf/mcp.json`.

**Configuración (Symlink):**
```bash
# En la raíz del proyecto
mkdir -p .windsurf
cd .windsurf
ln -s ../mcp.json mcp.json

# En Windows (PowerShell como Admin):
New-Item -ItemType Directory -Force -Path ".windsurf"
New-Item -ItemType SymbolicLink -Path ".windsurf\mcp.json" -Target "$PWD\mcp.json"
```

---

### Gemini CLI

Gemini CLI busca configuración en `.gemini/settings.json` (proyecto) o `~/.gemini/settings.json` (global).

**Para uso local en este proyecto:**
```bash
# En la raíz del proyecto
mkdir -p .gemini
cd .gemini
ln -s ../mcp.json settings.json

# En Windows (PowerShell como Admin):
New-Item -ItemType Directory -Force -Path ".gemini"
New-Item -ItemType SymbolicLink -Path ".gemini\settings.json" -Target "$PWD\mcp.json"
```

**Para uso global (todos los proyectos):**
```bash
# Copia el contenido a tu configuración global
cp mcp.json ~/.gemini/settings.json
```

---

### Firebase Studio (IDX)

Firebase Studio busca configuración en `.idx/mcp.json`.

**Configuración (Symlink):**
```bash
# En la raíz del proyecto
mkdir -p .idx
cd .idx
ln -s ../mcp.json mcp.json

# En Windows (PowerShell como Admin):
New-Item -ItemType Directory -Force -Path ".idx"
New-Item -ItemType SymbolicLink -Path ".idx\mcp.json" -Target "$PWD\mcp.json"
```

Luego reconstruye el workspace:
1. Abre Command Palette (Shift+Ctrl+P)
2. Ejecuta: **Firebase Studio: Rebuild Environment**

---

### Claude Code (Anthropic)

Claude Code busca configuración en el directorio del proyecto o puede usar configuración global.

**Para este proyecto:**

Claude Code debería detectar automáticamente `mcp.json` en la raíz. Si no, crea:

```bash
mkdir -p .claude
cd .claude
ln -s ../mcp.json mcp.json
```

---

### GitHub Copilot (VS Code)

GitHub Copilot con Agent mode usa la API nativa de VS Code para MCP.

**Configuración:**

Asegúrate de tener Dart extension v3.116+ y agrega a `.vscode/settings.json`:

```json
{
  "dart.mcpServer": true,
  "mcp.configPath": "${workspaceFolder}/mcp.json"
}
```

---

### Otros IDEs/Agentes

Para cualquier otro IDE que soporte MCP:

1. **Consulta la documentación** del IDE para saber dónde busca `mcp.json`
2. **Crea un symlink** desde esa ubicación al `mcp.json` raíz:
   ```bash
   ln -s /path/to/project/mcp.json /path/to/ide-config/mcp.json
   ```

---

## 🔐 Variables de Entorno

El archivo `mcp.json` usa variables de entorno para credenciales sensibles:

```json
{
  "env": {
    "FIGMA_PERSONAL_ACCESS_TOKEN": "${FIGMA_TOKEN}"
  }
}
```

### Configurar Variables de Entorno

**En tu sistema (Linux/Mac):**
```bash
# Agrega a ~/.bashrc o ~/.zshrc
export FIGMA_TOKEN="your-figma-token-here"
```

**En Windows:**
```powershell
# PowerShell
[Environment]::SetEnvironmentVariable("FIGMA_TOKEN", "your-token", "User")

# O en CMD
setx FIGMA_TOKEN "your-token"
```

**En tu IDE:**

La mayoría de los IDEs permiten configurar variables de entorno en sus settings.

---

## ✅ Verificar Configuración

### Cursor
```
Pregunta en el chat: "¿Están activos los servidores MCP?"
```

### VS Code (Copilot Agent Mode)
```
Escribe en el chat: /mcp
```

### Gemini CLI
```bash
gemini mcp list
```

### Cline
```
Verifica en la configuración de extensiones que detecta los servidores
```

---

## 📋 Contenido del mcp.json

El archivo incluye configuración para:

### 1. Flutter/Dart MCP Server
```json
{
  "dart": {
    "command": "dart",
    "args": ["mcp-server", "--force-roots-fallback"]
  }
}
```

**Capacidades:**
- Análisis estático de código
- Búsqueda de paquetes en pub.dev
- Gestión de dependencias
- Inspección del árbol de widgets
- Detección de errores de runtime

### 2. Figma MCP Server
```json
{
  "figma": {
    "command": "npx",
    "args": ["-y", "@figma/mcp-server-figma"],
    "env": {
      "FIGMA_PERSONAL_ACCESS_TOKEN": "${FIGMA_TOKEN}"
    }
  }
}
```

**Capacidades:**
- Extracción de assets (SVG, PNG, etc.)
- Obtención de tokens de diseño
- Consulta de componentes
- Especificaciones de diseño

### 3. Context7 MCP Server

```json
{
  "context7": {
    "command": "npx",
    "args": ["-y", "@upstash/context7-mcp"],
    "env": {
      "CONTEXT7_API_KEY": "${CONTEXT7_API_KEY}"
    }
  }
}
```

**Capacidades:**
- Documentación actualizada de librerías de código
- Resolución de IDs de librerías
- Búsqueda de documentación por topic
- Soporte para múltiples lenguajes y frameworks
- Documentación de Flutter/Dart packages

**Configuración de API Key (Opcional):**
- Sin API key: Funciona con rate limits
- Con API key: Sin rate limits (obtén una gratis en [context7.com/dashboard](https://context7.com/dashboard))

**Variables de entorno:**
```bash
# Linux/Mac
export CONTEXT7_API_KEY="your-api-key-here"

# Windows PowerShell
[Environment]::SetEnvironmentVariable("CONTEXT7_API_KEY", "your-api-key", "User")

# Windows CMD
setx CONTEXT7_API_KEY "your-api-key"
```

---

## 🐛 Troubleshooting

### Los servidores MCP no se detectan

1. **Verifica que el archivo existe:**
   ```bash
   ls -la mcp.json
   ```

2. **Verifica la sintaxis JSON:**
   ```bash
   cat mcp.json | jq .
   ```

3. **Reinicia tu IDE/Agente**

4. **Verifica los symlinks (si aplica):**
   ```bash
   ls -la .cursor/mcp.json
   ls -la .cline/mcp.json
   # etc.
   ```

### Error con Figma MCP

1. **Verifica que la variable de entorno está configurada:**
   ```bash
   echo $FIGMA_TOKEN    # Linux/Mac
   echo %FIGMA_TOKEN%   # Windows CMD
   $env:FIGMA_TOKEN     # Windows PowerShell
   ```

2. **Verifica que npx puede ejecutar el servidor:**
   ```bash
   npx -y @figma/mcp-server-figma --help
   ```

### Error con Flutter MCP

1. **Verifica que Dart está instalado:**
   ```bash
   dart --version
   ```

2. **Verifica que el comando mcp-server existe:**
   ```bash
   dart mcp-server --help
   ```

### Error con Context7 MCP

1. **Verifica que npx puede ejecutar el servidor:**
   ```bash
   npx -y @upstash/context7-mcp --help
   ```

2. **Si encuentras errores de módulo, prueba con bunx:**
   ```json
   {
     "context7": {
       "command": "bunx",
       "args": ["-y", "@upstash/context7-mcp"]
     }
   }
   ```

3. **Para problemas de ESM, agrega flag experimental:**
   ```json
   {
     "context7": {
       "command": "npx",
       "args": [
         "-y",
         "--node-options=--experimental-vm-modules",
         "@upstash/context7-mcp@1.0.6"
       ]
     }
   }
   ```

4. **Verifica que la API key está configurada (si usas una):**
   ```bash
   echo $CONTEXT7_API_KEY    # Linux/Mac
   echo %CONTEXT7_API_KEY%   # Windows CMD
   $env:CONTEXT7_API_KEY     # Windows PowerShell
   ```

5. **Nota:** Context7 funciona sin API key, pero con rate limits. Obtén una API key gratuita en [context7.com/dashboard](https://context7.com/dashboard) para uso ilimitado.

---

## 📚 Referencias

- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Flutter MCP Server](https://dart.dev/tools/mcp-server/)
- [Figma MCP Server](https://github.com/figma/mcp-server-guide/)
- [Context7 MCP Server](https://github.com/upstash/context7)
- [Context7 Website](https://context7.com/)

---

## 🔄 Actualizar Configuración

Para agregar un nuevo servidor MCP, edita el archivo `mcp.json` en la raíz:

```json
{
  "mcpServers": {
    "dart": { ... },
    "figma": { ... },
    "nuevo-servidor": {
      "command": "...",
      "args": [...],
      "env": {}
    }
  }
}
```

Todos los IDEs con symlinks recibirán la actualización automáticamente.

---

**Última actualización:** Diciembre 2025
