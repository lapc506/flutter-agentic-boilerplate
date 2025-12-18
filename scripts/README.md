# 📜 Scripts de Utilidad

Este directorio contiene scripts útiles para configurar y mantener el proyecto.

## 🔗 create-symlinks

Crea symlinks (enlaces simbólicos) desde la carpeta `skills/` hacia las ubicaciones requeridas por diferentes herramientas de IA.

### Scripts Disponibles

- **`create-symlinks.ps1`** - Para Windows (PowerShell)
- **`create-symlinks.sh`** - Para Linux/macOS (Bash)

### Uso

#### Windows

```powershell
# Ejecutar como administrador
.\scripts\create-symlinks.ps1
```

#### Linux / macOS

```bash
./scripts/create-symlinks.sh
```

### Herramientas Soportadas

El script crea symlinks para:

1. **Cursor Rules** → `.cursor/rules/skills`
2. **Kiro Steering** → `.kilocode/rules/skills`
3. **Claude Project Skills** → `.claude/skills/*`
4. **Gemini CLI Extensions** → `~/.gemini/extensions/flutter-agent-skills`
5. **OpenAI Codex** → `codex/skills/*`

### Requisitos

- **Windows:** Permisos de administrador (para crear symlinks)
- **Linux/macOS:** Permisos de escritura en el directorio del proyecto

### Documentación Completa

Para más detalles, consulta [`../docs/SYMLINKS_SETUP.md`](../docs/SYMLINKS_SETUP.md).

---

**Nota:** Los symlinks se excluyen del control de versiones (ver `.gitignore`). Cada desarrollador debe ejecutar estos scripts localmente.

