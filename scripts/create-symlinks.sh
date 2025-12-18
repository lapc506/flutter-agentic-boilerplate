#!/bin/bash
# Script para crear symlinks de skills a diferentes herramientas
# Uso: ./scripts/create-symlinks.sh

set -e

# Obtener la ruta del proyecto (raíz del repo)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SKILLS_DIR="$PROJECT_ROOT/skills"

echo "📦 Creando symlinks desde skills/ hacia diferentes herramientas..."
echo "Proyecto: $PROJECT_ROOT"
echo "Skills: $SKILLS_DIR"
echo ""

# 1. Cursor Rules (.cursor/rules/)
CURSOR_RULES_DIR="$PROJECT_ROOT/.cursor/rules"
mkdir -p "$CURSOR_RULES_DIR"
CURSOR_SYMLINK="$CURSOR_RULES_DIR/skills"

if [ -e "$CURSOR_SYMLINK" ] || [ -L "$CURSOR_SYMLINK" ]; then
    echo "⚠️  Ya existe: $CURSOR_SYMLINK"
    rm -f "$CURSOR_SYMLINK"
fi
ln -s "$SKILLS_DIR" "$CURSOR_SYMLINK"
echo "✅ Symlink creado: $CURSOR_SYMLINK -> $SKILLS_DIR"

# 2. Kiro Steering (.kilocode/rules/)
KIRO_RULES_DIR="$PROJECT_ROOT/.kilocode/rules"
mkdir -p "$KIRO_RULES_DIR"
KIRO_SYMLINK="$KIRO_RULES_DIR/skills"

if [ -e "$KIRO_SYMLINK" ] || [ -L "$KIRO_SYMLINK" ]; then
    echo "⚠️  Ya existe: $KIRO_SYMLINK"
    rm -f "$KIRO_SYMLINK"
fi
ln -s "$SKILLS_DIR" "$KIRO_SYMLINK"
echo "✅ Symlink creado: $KIRO_SYMLINK -> $SKILLS_DIR"

# 3. Claude Project Skills (.claude/skills/)
CLAUDE_SKILLS_DIR="$PROJECT_ROOT/.claude/skills"
mkdir -p "$CLAUDE_SKILLS_DIR"

# Crear symlinks para cada skill individual
for SKILL_DIR in "$SKILLS_DIR"/*; do
    if [ -d "$SKILL_DIR" ]; then
        SKILL_NAME=$(basename "$SKILL_DIR")
        CLAUDE_SKILL_SYMLINK="$CLAUDE_SKILLS_DIR/$SKILL_NAME"
        
        if [ -e "$CLAUDE_SKILL_SYMLINK" ] || [ -L "$CLAUDE_SKILL_SYMLINK" ]; then
            echo "⚠️  Ya existe: $CLAUDE_SKILL_SYMLINK"
            rm -f "$CLAUDE_SKILL_SYMLINK"
        fi
        
        ln -s "$SKILL_DIR" "$CLAUDE_SKILL_SYMLINK"
        echo "✅ Symlink creado: $CLAUDE_SKILL_SYMLINK -> $SKILL_DIR"
    fi
done

# 4. Gemini CLI Extensions (~/.gemini/extensions/)
GEMINI_EXTENSIONS_DIR="$HOME/.gemini/extensions"
mkdir -p "$GEMINI_EXTENSIONS_DIR"

# Crear una extensión "flutter-agent-skills" que apunta a todo el directorio skills
GEMINI_EXTENSION_NAME="flutter-agent-skills"
GEMINI_EXTENSION_DIR="$GEMINI_EXTENSIONS_DIR/$GEMINI_EXTENSION_NAME"

if [ -e "$GEMINI_EXTENSION_DIR" ] || [ -L "$GEMINI_EXTENSION_DIR" ]; then
    echo "⚠️  Ya existe: $GEMINI_EXTENSION_DIR"
    rm -rf "$GEMINI_EXTENSION_DIR"
fi
ln -s "$SKILLS_DIR" "$GEMINI_EXTENSION_DIR"
echo "✅ Symlink creado: $GEMINI_EXTENSION_DIR -> $SKILLS_DIR"

# Crear gemini-extension.json si no existe
GEMINI_EXTENSION_JSON="$SKILLS_DIR/gemini-extension.json"
if [ ! -f "$GEMINI_EXTENSION_JSON" ]; then
    cat > "$GEMINI_EXTENSION_JSON" << 'EOF'
{
  "name": "flutter-agent-skills",
  "version": "1.0.0",
  "description": "Flutter Agent Skills - Comprehensive collection of Flutter development skills",
  "author": "Flutter Agent Skills Team",
  "repository": "https://github.com/your-org/flutter-agent-skills"
}
EOF
    echo "✅ Creado: gemini-extension.json"
fi

# 5. OpenAI Codex (codex/skills/)
CODEX_SKILLS_DIR="$PROJECT_ROOT/codex/skills"
mkdir -p "$CODEX_SKILLS_DIR"

# Crear symlinks para cada skill individual
for SKILL_DIR in "$SKILLS_DIR"/*; do
    if [ -d "$SKILL_DIR" ]; then
        SKILL_NAME=$(basename "$SKILL_DIR")
        CODEX_SKILL_SYMLINK="$CODEX_SKILLS_DIR/$SKILL_NAME"
        
        if [ -e "$CODEX_SKILL_SYMLINK" ] || [ -L "$CODEX_SKILL_SYMLINK" ]; then
            echo "⚠️  Ya existe: $CODEX_SKILL_SYMLINK"
            rm -f "$CODEX_SKILL_SYMLINK"
        fi
        
        ln -s "$SKILL_DIR" "$CODEX_SKILL_SYMLINK"
        echo "✅ Symlink creado: $CODEX_SKILL_SYMLINK -> $SKILL_DIR"
    fi
done

echo ""
echo "✨ ¡Symlinks creados exitosamente!"
echo ""
echo "📋 Resumen:"
echo "  • Cursor Rules: .cursor/rules/skills"
echo "  • Kiro Steering: .kilocode/rules/skills"
echo "  • Claude Skills: .claude/skills/*"
echo "  • Gemini Extensions: ~/.gemini/extensions/flutter-agent-skills"
echo "  • OpenAI Codex: codex/skills/*"
echo ""

