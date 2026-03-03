# Changelog

Todos los cambios notables en este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto adhiere a [Semantic Versioning](https://semver.org/lang/es/).

## [1.0.0] - 2025-12-17

### Agregado

- ✨ Estructura inicial del proyecto scaffolding
- 📚 Archivo `AGENTS.md` con documentación completa de skills
- 🔧 Configuración del Flutter MCP Server (`.cursor/mcp.json`)
- 📖 README completo con guías de uso e instalación
- 🤝 Guía de contribución (`CONTRIBUTING.md`)
- 📄 Licencia MIT

### Skills Implementados

#### Skill 1: Patrón MVVM
- Documentación completa del patrón Model-View-ViewModel
- Ejemplos de código para Model, View y ViewModel
- Guía de gestión de estado con Provider
- Dependencias recomendadas
- Ejemplos de testing
- Mejores prácticas y principios

#### Skill 2: Clean Architecture
- Documentación completa de Clean Architecture
- Estructura en 3 capas: Domain, Data, Presentation
- Ejemplos de Entities, Use Cases, Repositories
- Implementación con BLoC pattern
- Configuración de Dependency Injection con GetIt
- Uso de Either<Failure, Success> para manejo de errores
- Tests unitarios y de integración
- Principios SOLID aplicados

#### Skill 3: Configuración Inicial
- Checklist de configuración estándar
- Estructura base de proyecto
- Configuración de análisis estático
- Setup de flavors y entornos

#### Skill 4: Testing Comprehensivo
- Estrategias de testing (unit, widget, integration)
- Herramientas recomendadas
- Ejemplos de tests para cada capa

#### Skill 5: CI/CD Pipeline
- Configuración de GitHub Actions
- Pipeline de build y test automatizado
- Generación de builds

### Configuración del Proyecto

- 🔧 MCP Server configurado para Cursor
- 📝 Instrucciones para VS Code, Gemini CLI y Firebase Studio
- 🚀 Comandos útiles para asistentes de IA
- 📦 `.gitignore` configurado para proyectos Flutter

### Documentación

- Guía completa de uso del MCP Server
- Referencias a repositorios de ejemplo
- Enlaces a documentación oficial
- Ejemplos de prompts para IA

### Referencias Integradas

- [Dart MCP Server](https://dart.dev/tools/mcp-server/) - Documentación oficial

---

## [2.0.0] - 2025-12-17

### Agregado

#### Skill 6: State Management con Riverpod
- Documentación completa de Riverpod
- Provider types: Provider, StateProvider, StateNotifierProvider, FutureProvider, StreamProvider
- Modifiers: autoDispose, family, keepAlive
- Dependency Injection con Riverpod
- Testing de providers
- Mejores prácticas y optimización con .select

#### Skill 7: State Management con BLoC Avanzado
- BLoC pattern completo con eventos y estados
- Cubit pattern para lógica simple
- Hydrated BLoC para persistencia automática
- Replay BLoC para undo/redo functionality
- Event transformers (debounce, throttle, restartable)
- BLoC Observer para logging
- Testing exhaustivo con bloc_test

#### Skill 8: Arquitectura Modular
- Estructura de monorepo con paquetes independientes
- Core module con design system y utilities
- Feature modules auto-contenidos
- Dependency Injection con flutter_modular
- Route guards y navegación modular
- Event Bus para comunicación entre módulos
- Gestión con Melos

#### Skill 9: Feature-First Architecture
- Organización por features en lugar de capas técnicas
- Estructura Domain/Data/Presentation por feature
- Barrel files para exports limpios
- Go Router para navegación
- Dependency Injection con GetIt e Injectable
- Clean Architecture dentro de cada feature

#### Skill 10: Internacionalización (i18n)
- Configuración con flutter_localizations
- ARB files para traducciones
- Placeholders y plurales
- Formateo de fechas, números y monedas
- Cambio dinámico de idioma con BLoC
- Widget selector de idioma
- Soporte para múltiples locales

#### Skill 11: Theming Avanzado
- Material 3 con color schemes personalizados
- Design tokens (colores, tipografía, spacing)
- Light mode + Dark mode + System mode
- Temas personalizados por componente
- Google Fonts integration
- Cambio dinámico de tema
- Persistencia de preferencias

#### Skill 12: Offline-First Architecture
- Priorización de almacenamiento local
- Detección de conectividad
- Sync queue para operaciones offline
- Resolución de conflictos
- Cache inteligente con Hive
- Background sync automático
- Indicador de estado de conectividad

#### Skill 13: GraphQL Integration
- Cliente GraphQL con graphql_flutter
- Queries, Mutations y Subscriptions
- Cache automático con políticas configurables
- Optimistic updates
- Manejo de errores
- WebSocket links para real-time
- Code generation con Ferry (opcional)

#### Skill 14: Firebase Integration
- Firebase Core setup multiplataforma
- Firebase Authentication (Email, Google, etc.)
- Cloud Firestore con real-time streams
- Cloud Storage para archivos
- Cloud Messaging (Push Notifications)
- Firebase Analytics
- Crashlytics para error tracking
- Remote Config para A/B testing

#### Skill 15: Performance Optimization
- Reducción de rebuilds con const
- ListView.builder y optimizaciones de listas
- RepaintBoundary para aislar repaints
- Image caching y optimización
- AutomaticKeepAliveClientMixin para tabs
- Slivers optimizados
- Lazy loading y code splitting
- Performance monitoring
- DevTools profiling
- Memory leak prevention

---

## [3.0.0] - 2026-02-18

### Agregado - Ejemplos y Templates

- [x] **Estructura de Ejemplos** en `/examples/`
  - Directorio `templates/` con templates reutilizables
  - Directorio `projects/` con proyectos de ejemplo completos
  - Scripts de generación automática
  - Documentación completa de uso

- [x] **Scripts de Generación**
  - `create-project.sh` - Crea nuevos proyectos desde templates
  - `add-feature.sh` - Agrega features/skills a proyectos existentes
  - Soporte para múltiples templates: starter, offline-first, microservices

### Agregado - Nuevos Skills (16-20)

- [x] **Skill 16: WebSocket Integration** (`skills/flutter/websocket-integration/`)
  - WebSocket y Socket.io para comunicación en tiempo real
  - Auto-reconexión con backoff exponencial
  - Cola de mensajes offline
  - Ejemplos de chat en tiempo real

- [x] **Skill 17: Payment Integration** (`skills/flutter/payment-integration/`)
  - Stripe con Payment Intents
  - PayPal checkout
  - Apple Pay / Google Pay
  - Suscripciones y gestión de pagos
  - Cumplimiento PCI DSS

- [x] **Skill 18: Map Integration** (`skills/flutter/map-integration/`)
  - Google Maps y Mapbox
  - Marcadores y clusters
  - Tracking de ubicación
  - Rutas y direcciones
  - Polígonos y polilíneas

- [x] **Skill 19: Video/Audio Processing** (`skills/flutter/video-audio-processing/`)
  - Reproducción de video (video_player, chewie)
  - Grabación de video con cámara
  - Grabación y reproducción de audio
  - Procesamiento con FFmpeg
  - Compresión y edición de video

- [x] **Skill 20: Machine Learning** (`skills/flutter/machine-learning/`)
  - TensorFlow Lite para clasificación de imágenes
  - ML Kit para OCR, detección de objetos, códigos de barras
  - Face detection
  - Descarga de modelos desde Firebase
  - Inferencia on-device optimizada

### Documentación

- [x] Guías completas para cada nuevo skill
- [x] Ejemplos de código funcionales
- [x] Mejores prácticas y troubleshooting
- [x] Requisitos de backend donde aplica

---

## [Unreleased]

### Planeado para Futuras Versiones

- [ ] Integración con más herramientas MCP
- [ ] Skill 21: Voice Recognition
- [ ] Skill 22: Biometric Authentication
- [ ] Skill 23: Background Processing
- [ ] Skill 24: App Clips/Instant Apps
- [ ] Skill 25: Wearable Integration

---

## Tipos de Cambios

- `Agregado` - para nuevas características
- `Cambiado` - para cambios en funcionalidad existente
- `Obsoleto` - para características que serán removidas
- `Removido` - para características removidas
- `Corregido` - para corrección de bugs
- `Seguridad` - para vulnerabilidades

---

**Nota:** Las fechas siguen el formato YYYY-MM-DD (ISO 8601)
