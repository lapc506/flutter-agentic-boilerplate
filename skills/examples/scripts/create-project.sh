#!/bin/bash

# Script para crear un nuevo proyecto Flutter con Agent Skills
# Uso: ./create-project.sh --name <nombre-proyecto> --template <starter|offline-first|microservices> [--path <ruta>]

set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Variables por defecto
TEMPLATE="starter"
PROJECT_PATH="."
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMPLATES_DIR="$SCRIPT_DIR/../templates"

# Función de ayuda
show_help() {
	echo -e "${BLUE}Flutter Skills Project Generator${NC}"
	echo ""
	echo "Uso: $0 [OPTIONS]"
	echo ""
	echo "Opciones:"
	echo "  -n, --name <nombre>        Nombre del proyecto (requerido)"
	echo "  -t, --template <template>  Template a usar: starter, offline-first, microservices (default: starter)"
	echo "  -p, --path <ruta>          Ruta donde crear el proyecto (default: .)"
	echo "  -h, --help                 Mostrar esta ayuda"
	echo ""
	echo "Ejemplos:"
	echo "  $0 --name mi-app --template starter"
	echo "  $0 -n mi-app -t offline-first -p ./proyectos"
}

# Parsear argumentos
while [[ $# -gt 0 ]]; do
	case $1 in
	-n | --name)
		PROJECT_NAME="$2"
		shift 2
		;;
	-t | --template)
		TEMPLATE="$2"
		shift 2
		;;
	-p | --path)
		PROJECT_PATH="$2"
		shift 2
		;;
	-h | --help)
		show_help
		exit 0
		;;
	*)
		echo -e "${RED}Error: Opción desconocida $1${NC}"
		show_help
		exit 1
		;;
	esac
done

# Validar nombre del proyecto
if [ -z "$PROJECT_NAME" ]; then
	echo -e "${RED}Error: Debes especificar el nombre del proyecto${NC}"
	show_help
	exit 1
fi

# Validar template
if [ ! -d "$TEMPLATES_DIR/$TEMPLATE" ]; then
	echo -e "${RED}Error: Template '$TEMPLATE' no encontrado${NC}"
	echo "Templates disponibles:"
	ls -1 "$TEMPLATES_DIR"
	exit 1
fi

# Crear ruta completa
FULL_PATH="$PROJECT_PATH/$PROJECT_NAME"

# Verificar si ya existe
if [ -d "$FULL_PATH" ]; then
	echo -e "${RED}Error: El directorio $FULL_PATH ya existe${NC}"
	exit 1
fi

echo -e "${BLUE}🚀 Creando proyecto '$PROJECT_NAME' con template '$TEMPLATE'...${NC}"

# Crear directorio
echo -e "${YELLOW}📁 Creando estructura de directorios...${NC}"
mkdir -p "$FULL_PATH"

# Copiar template
echo -e "${YELLOW}📋 Copiando archivos del template...${NC}"
cp -r "$TEMPLATES_DIR/$TEMPLATE/"* "$FULL_PATH/"

# Reemplazar placeholders en archivos
echo -e "${YELLOW}🔧 Configurando proyecto...${NC}"
find "$FULL_PATH" -type f \( -name "*.dart" -o -name "*.yaml" -o -name "*.md" -o -name "*.json" \) -exec sed -i "s/{{PROJECT_NAME}}/$PROJECT_NAME/g" {} \;
find "$FULL_PATH" -type f \( -name "*.dart" -o -name "*.yaml" -o -name "*.md" -o -name "*.json" \) -exec sed -i "s/{{PROJECT_NAME_PASCAL}}/$(echo "$PROJECT_NAME" | sed -r 's/(^|_)([a-z])/\U\2/g')/g" {} \;

# Hacer ejecutables los scripts
echo -e "${YELLOW}⚡ Configurando permisos...${NC}"
chmod +x "$FULL_PATH/scripts/"*.sh 2>/dev/null || true

# Inicializar git
echo -e "${YELLOW}📦 Inicializando repositorio git...${NC}"
cd "$FULL_PATH"
git init -q
git add .
git commit -q -m "Initial commit: Project generated from $TEMPLATE template"

echo ""
echo -e "${GREEN}✅ Proyecto '$PROJECT_NAME' creado exitosamente!${NC}"
echo ""
echo -e "${BLUE}📍 Ubicación:${NC} $FULL_PATH"
echo ""
echo -e "${BLUE}📝 Próximos pasos:${NC}"
echo "  cd $FULL_PATH"
if [ -f "$FULL_PATH/pubspec.yaml" ]; then
	echo "  flutter pub get"
	echo "  flutter run"
elif [ -f "$FULL_PATH/package.json" ]; then
	echo "  npm install"
	echo "  npm run dev"
fi
