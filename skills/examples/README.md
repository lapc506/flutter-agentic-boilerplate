# Ejemplos Prácticos Flutter

Este directorio contiene proyectos de ejemplo completos que demuestran el uso de los diferentes skills disponibles.

## Estructura

```
examples/
├── README.md                 # Este archivo
├── templates/               # Templates de proyecto pre-configurados
│   ├── starter/            # Template básico para nuevos proyectos
│   ├── offline-first/      # Template con arquitectura offline-first
│   └── microservices/      # Template para arquitectura de microservicios
├── projects/               # Proyectos de ejemplo completos
│   ├── todo-app/          # App de tareas con CRUD completo
│   ├── chat-app/          # App de chat con WebSocket
│   └── e-commerce/        # App de comercio electrónico
└── scripts/               # Scripts de generación automática
    ├── create-project.sh  # Script para crear nuevo proyecto
    └── add-feature.sh     # Script para agregar features
```

## Templates Disponibles

### 1. Starter Template
Proyecto base con:
- Clean Architecture configurada
- Riverpod para state management
- Análisis estático configurado
- Estructura de carpetas estándar

### 2. Offline-First Template
Incluye todo lo de Starter más:
- Cache local con Hive
- Sync queue con sqflite
- Detección de conectividad
- Manejo de sincronización

### 3. Microservices Template
Para proyectos backend:
- Estructura de microservicios
- Docker Compose configurado
- API Gateway básico
- Comunicación entre servicios

## Uso Rápido

### Crear nuevo proyecto
```bash
./scripts/create-project.sh --name my-app --template starter
cd my-app
flutter pub get
flutter run
```

### Agregar feature a proyecto existente
```bash
./scripts/add-feature.sh --project ./my-app --feature websocket
cd my-app
flutter pub get
```

## Proyectos de Ejemplo

### Todo App
Aplicación completa de lista de tareas que demuestra:
- CRUD con GraphQL
- Estado offline
- Sincronización
- Testing completo

### Chat App
Aplicación de mensajería que incluye:
- WebSocket para tiempo real
- Persistencia de mensajes
- Notificaciones push
- Chat en grupo

### E-Commerce
Tienda online completa con:
- Catálogo de productos
- Carrito de compras
- Integración de pagos
- Seguimiento de órdenes

## Contribuir

Para agregar un nuevo ejemplo:
1. Crear carpeta en `projects/` o `templates/`
2. Incluir README.md con instrucciones
3. Agregar tests de ejemplo
4. Documentar en este archivo

## Recursos Adicionales

- [Documentación de Skills](../flutter/)
- [Guía de Contribución](../CONTRIBUTING.md)
- [Configuración MCP](../MCP_SETUP.md)
