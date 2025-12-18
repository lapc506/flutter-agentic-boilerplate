# 🔗 Configuración de Symlinks para Skills

Este documento explica cómo crear symlinks (enlaces simbólicos) desde la carpeta `skills/` hacia las ubicaciones requeridas por diferentes herramientas de IA.

## 📋 Herramientas Soportadas

1. **Cursor Rules** - `.cursor/rules/skills`
2. **Kiro Steering** - `.kilocode/rules/skills`
3. **Claude Project Skills** - `.claude/skills/*`
4. **Gemini CLI Extensions** - `~/.gemini/extensions/flutter-agent-skills`
5. **OpenAI Codex** - `codex/skills/*`

## 🚀 Uso Rápido

### Windows (PowerShell como Administrador)

```powershell
# Ejecutar como administrador
.\scripts\create-symlinks.ps1
```

### Linux / macOS

```bash
./scripts/create-symlinks.sh
```

## 📂 Estructura de Symlinks Creados

Después de ejecutar el script, se crearán los siguientes symlinks:

```
proyecto/
├── .cursor/
│   └── rules/
│       └── skills -> ../skills/
├── .kilocode/
│   └── rules/
│       └── skills -> ../skills/
├── .claude/
│   └── skills/
│       ├── flutter/ -> ../../skills/flutter/
│       ├── cicd/ -> ../../skills/cicd/
│       ├── figma/ -> ../../skills/figma/
│       └── ...
├── codex/
│   └── skills/
│       ├── flutter/ -> ../../skills/flutter/
│       ├── cicd/ -> ../../skills/cicd/
│       └── ...
└── skills/ (directorio original)

~/.gemini/extensions/
└── flutter-agent-skills -> /path/to/project/skills/
```

## 🔧 Configuración por Herramienta

### 1. Cursor Rules

**Ubicación:** `.cursor/rules/skills`

Cursor detecta automáticamente los archivos `.mdc` en `.cursor/rules/`. El symlink permite que Cursor acceda a todos los skills.

**Uso:**
- Los skills se cargan automáticamente cuando Cursor detecta archivos `SKILL.md`
- Puedes referenciar skills en tus prompts usando keywords

### 2. Kiro Steering

**Ubicación:** `.kilocode/rules/skills`

Kiro Steering busca reglas en `.kilocode/rules/`. El symlink permite que Kiro acceda a los skills.

**Uso:**
- Similar a Cursor, los skills se detectan automáticamente
- Usa keywords en tus prompts para invocar skills específicos

### 3. Claude Project Skills

**Ubicación:** `.claude/skills/*`

Claude Agent SDK busca skills en `.claude/skills/` cuando se configura `settingSources: ["project"]`.

**Configuración requerida:**

```typescript
// TypeScript
import { query } from "@anthropic-ai/claude-agent-sdk";

for await (const message of query({
  prompt: "Help me with Flutter MVVM",
  options: {
    cwd: "/path/to/project",
    settingSources: ["user", "project"],  // Carga skills del proyecto
    allowedTools: ["Skill", "Read", "Write", "Bash"]
  }
})) {
  console.log(message);
}
```

```python
# Python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions

async def main():
    options = ClaudeAgentOptions(
        cwd="/path/to/project",
        setting_sources=["user", "project"],  # Carga skills del proyecto
        allowed_tools=["Skill", "Read", "Write", "Bash"]
    )

    async for message in query(
        prompt="Help me with Flutter MVVM",
        options=options
    ):
        print(message)

asyncio.run(main())
```

**Referencia:** [Claude Agent SDK Skills Documentation](https://platform.claude.com/docs/en/agent-sdk/skills#skill-locations)

### 4. Gemini CLI Extensions

**Ubicación:** `~/.gemini/extensions/flutter-agent-skills`

Gemini CLI busca extensiones en `~/.gemini/extensions/`. El symlink crea una extensión llamada `flutter-agent-skills`.

**Configuración:**

El archivo `skills/gemini-extension.json` se crea automáticamente con la configuración necesaria.

**Uso:**

```bash
# Verificar que la extensión está instalada
gemini extensions list

# Usar skills en tus prompts
gemini "Crea una app Flutter usando mvvm"
```

**Referencia:** [Gemini CLI Extensions Documentation](https://geminicli.com/docs/extensions/)

### 5. OpenAI Codex

**Ubicación:** `codex/skills/*`

OpenAI Codex busca skills en `codex/skills/`. Cada skill se crea como un symlink individual.

**Nota:** La estructura exacta puede variar según la versión de Codex. Consulta la [documentación oficial de Codex](https://github.com/openai/codex/blob/main/docs/skills.md) para más detalles.

## 🔄 Actualización de Symlinks

Si agregas nuevos skills a la carpeta `skills/`, necesitas volver a ejecutar el script para crear los symlinks correspondientes:

```bash
# Linux/Mac
./scripts/create-symlinks.sh

# Windows (PowerShell como Admin)
.\scripts\create-symlinks.ps1
```

El script elimina symlinks existentes antes de crear nuevos, así que es seguro ejecutarlo múltiples veces.

## 🐛 Solución de Problemas

### Windows: "No se puede crear el symlink"

**Problema:** Windows requiere permisos de administrador para crear symlinks.

**Solución:**
1. Abre PowerShell como administrador
2. Ejecuta: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
3. Ejecuta el script nuevamente

### Linux/Mac: "Permission denied"

**Problema:** El script no tiene permisos de ejecución.

**Solución:**
```bash
chmod +x scripts/create-symlinks.sh
./scripts/create-symlinks.sh
```

### Symlinks no funcionan en Cursor

**Problema:** Cursor puede no seguir symlinks en ciertos casos.

**Solución alternativa:** Copia los skills directamente en lugar de usar symlinks:

```bash
# Linux/Mac
cp -r skills/* .cursor/rules/skills/

# Windows (PowerShell)
Copy-Item -Path skills\* -Destination .cursor\rules\skills\ -Recurse
```

**Nota:** Esto crea copias, no symlinks. Necesitarás actualizar manualmente cuando cambien los skills.

### Gemini CLI no detecta la extensión

**Problema:** La extensión no aparece en `gemini extensions list`.

**Solución:**
1. Verifica que el symlink existe: `ls -la ~/.gemini/extensions/flutter-agent-skills`
2. Verifica que `gemini-extension.json` existe en `skills/`
3. Reinicia Gemini CLI

## 📝 Notas Importantes

1. **Symlinks vs Copias:** Los symlinks son preferibles porque mantienen los skills sincronizados. Sin embargo, algunas herramientas pueden no soportarlos completamente.

2. **Git:** Los symlinks se pueden versionar en Git, pero algunos sistemas pueden tener problemas. Considera agregar excepciones en `.gitignore` si es necesario.

3. **Multiplataforma:** Los scripts están diseñados para funcionar en Windows, Linux y macOS. Sin embargo, el comportamiento de symlinks puede variar ligeramente entre sistemas.

4. **Estructura de Skills:** Cada skill debe tener un archivo `SKILL.md` en su directorio raíz para ser detectado correctamente por las herramientas.

## 🔗 Referencias

- [Claude Agent SDK Skills](https://platform.claude.com/docs/en/agent-sdk/skills)
- [Gemini CLI Extensions](https://geminicli.com/docs/extensions/)
- [OpenAI Codex Skills](https://github.com/openai/codex/blob/main/docs/skills.md)
- [Cursor Rules Documentation](https://docs.cursor.com/en/context/rules)

---

**Última actualización:** Diciembre 2025

