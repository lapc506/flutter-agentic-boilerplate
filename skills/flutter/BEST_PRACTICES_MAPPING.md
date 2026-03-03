# Mapeo de Mejores Prácticas por Skill

Este documento mapea las prácticas del archivo `flutter-best-practices.md` que deberían incluirse en cada skill de Flutter.

## 📋 Resumen Ejecutivo

Las mejores prácticas se organizan en las siguientes categorías:
- **Arquitectura y Estructura** (REQ-FLT-001 a REQ-FLT-043)
- **Rendimiento** (REQ-FLT-011 a REQ-FLT-014, REQ-FLT-066 a REQ-FLT-072, REQ-FLT-114 a REQ-FLT-121)
- **Seguridad** (REQ-FLT-021 a REQ-FLT-023, REQ-FLT-073 a REQ-FLT-077)
- **Testing y CI/CD** (REQ-FLT-020, REQ-FLT-029 a REQ-FLT-031, REQ-FLT-078 a REQ-FLT-081)
- **Conectividad** (REQ-FLT-032 a REQ-FLT-034, REQ-FLT-086 a REQ-FLT-089)
- **Despliegue** (REQ-FLT-035 a REQ-FLT-037, REQ-FLT-090 a REQ-FLT-092)
- **Theming y UI** (REQ-FLT-055 a REQ-FLT-059, REQ-FLT-122 a REQ-FLT-133)
- **Accesibilidad** (REQ-FLT-060 a REQ-FLT-061, REQ-FLT-141 a REQ-FLT-149)
- **Documentación** (REQ-FLT-062 a REQ-FLT-063, REQ-FLT-150 a REQ-FLT-157)
- **Dart Best Practices** (REQ-FLT-102 a REQ-FLT-113)
- **MCP Integration** (REQ-FLT-038 a REQ-FLT-040, REQ-FLT-094 a REQ-FLT-101)

---

## 🎯 Mapeo por Skill

### 1. **accessibility** ♿

**Prácticas Altamente Relevantes:**
- REQ-FLT-060: Labels semánticos obligatorios
- REQ-FLT-061: Contraste mínimo obligatorio
- REQ-FLT-142: Accesibilidad según WCAG 2.1
- REQ-FLT-143: Contraste mínimo para texto (4.5:1)
- REQ-FLT-144: Escalado dinámico de texto
- REQ-FLT-145: Widget Semantics para labels
- REQ-FLT-146: Pruebas con TalkBack y VoiceOver
- REQ-FLT-147: Labels semánticos claros
- REQ-FLT-148: Navegación por teclado
- REQ-FLT-149: Hints y descriptions apropiados

**Prácticas Complementarias:**
- REQ-FLT-122: Material Design 3 o Cupertino (para componentes accesibles)
- REQ-FLT-127: Contraste mínimo 4.5:1 (duplicado pero importante)

---

### 2. **animation-motion** 🎬

**Prácticas Altamente Relevantes:**
- REQ-FLT-066: Constructor const obligatorio (para widgets animados)
- REQ-FLT-068: RepaintBoundary para widgets costosos (animaciones complejas)
- REQ-FLT-069: Perfilado regular con DevTools (para optimizar animaciones)
- REQ-FLT-070: No bloquear hilo principal (animaciones deben ser fluidas)
- REQ-FLT-114: Widgets inmutables (para animaciones eficientes)
- REQ-FLT-118: ListView.builder para listas largas (si hay listas animadas)
- REQ-FLT-119: Compute para cálculos costosos (cálculos en animaciones)
- REQ-FLT-120: Constructores const (optimización de animaciones)
- REQ-FLT-121: No operaciones costosas en build (especialmente en animaciones)

**Prácticas Complementarias:**
- REQ-FLT-011: Fluidez de interfaz (60 FPS)
- REQ-FLT-013: Uso eficiente de memoria

---

### 3. **app-distribution** 📦

**Prácticas Altamente Relevantes:**
- REQ-FLT-035: Feature Flags implementados
- REQ-FLT-036: Monitoreo en producción (Crashlytics y Analytics)
- REQ-FLT-037: Dependencias actualizadas
- REQ-FLT-077: Ofuscación en producción
- REQ-FLT-090: Feature Flags con Firebase Remote Config
- REQ-FLT-091: Crashlytics y Firebase Analytics
- REQ-FLT-092: Dependencias actualizadas mensualmente
- REQ-FLT-082: Commits atómicos
- REQ-FLT-083: Feature branches
- REQ-FLT-084: Tags semánticos
- REQ-FLT-085: Versionado semántico

**Prácticas Complementarias:**
- REQ-FLT-031: Versionado semántico (duplicado)
- REQ-FLT-078: Pipeline con linter y tests

---

### 4. **analytics-tracking** 📊

**Prácticas Altamente Relevantes:**
- REQ-FLT-036: Monitoreo en producción
- REQ-FLT-091: Crashlytics y Firebase Analytics
- REQ-FLT-028: Logging estructurado (debugPrint o logger)
- REQ-FLT-150: Comentarios dartdoc para APIs públicas
- REQ-FLT-151: Documentar clases y métodos

**Prácticas Complementarias:**
- REQ-FLT-021: Protección de datos sensibles (PII en analytics)
- REQ-FLT-140: Evitar nesting profundo (para código de tracking)

---

### 5. **bloc-advanced** 🧩

**Prácticas Altamente Relevantes:**
- REQ-FLT-003: Gestión de estado consistente
- REQ-FLT-017: Inyección de dependencias obligatoria
- REQ-FLT-019: Código autodocumentado
- REQ-FLT-020: Cobertura de testing mínima 80%
- REQ-FLT-027: Inmutabilidad preferida (final)
- REQ-FLT-102: Guías oficiales Effective Dart
- REQ-FLT-103: Null safety consistente
- REQ-FLT-110: Try-catch apropiado
- REQ-FLT-111: Async/await consistente
- REQ-FLT-112: Streams para eventos asíncronos

**Prácticas Complementarias:**
- REQ-FLT-015: Arquitectura de tres capas obligatoria
- REQ-FLT-016: Flujo de dependencias unidireccional

---

### 6. **clean-architecture** 🏗️

**Prácticas Altamente Relevantes:**
- REQ-FLT-001: Estructura de presentación obligatoria
- REQ-FLT-002: Separación de responsabilidades en UI
- REQ-FLT-004: Independencia de framework (Domain layer)
- REQ-FLT-005: Definición de entidades
- REQ-FLT-006: Contratos de repositorio
- REQ-FLT-007: Casos de uso específicos
- REQ-FLT-008: Implementación de repositorios
- REQ-FLT-009: Fuentes de datos separadas
- REQ-FLT-010: Modelos de datos tipados
- REQ-FLT-015: Arquitectura de tres capas obligatoria
- REQ-FLT-016: Flujo de dependencias unidireccional
- REQ-FLT-017: Inyección de dependencias obligatoria
- REQ-FLT-041: Estructura basada en features
- REQ-FLT-042: Separación estricta de capas
- REQ-FLT-043: Flujo de dependencias controlado
- REQ-FLT-044: Nomenclatura consistente

**Prácticas Complementarias:**
- REQ-FLT-019: Código autodocumentado
- REQ-FLT-020: Cobertura de testing mínima 80%
- REQ-FLT-100: MCP para refactoring siguiendo Clean Architecture

---

### 7. **code-generation** ⚙️

**Prácticas Altamente Relevantes:**
- REQ-FLT-051: Build runner obligatorio para generación de código
- REQ-FLT-025: Análisis estático obligatorio (excluir archivos generados)
- REQ-FLT-026: Formateo consistente
- REQ-FLT-102: Guías oficiales Effective Dart
- REQ-FLT-106: Clases relacionadas en mismo archivo
- REQ-FLT-107: Librerías agrupadas por carpeta
- REQ-FLT-108: Documentación de APIs públicas

**Prácticas Complementarias:**
- REQ-FLT-150: Comentarios dartdoc para APIs públicas
- REQ-FLT-101: Validación de código AI (código generado)

---

### 8. **deep-linking** 🔗

**Prácticas Altamente Relevantes:**
- REQ-FLT-052: Routing declarativo obligatorio (GoRouter)
- REQ-FLT-053: Patrones de navegación consistentes
- REQ-FLT-075: Validación de entradas (validar deep links)
- REQ-FLT-018: Manejo de errores robusto (errores en deep links)
- REQ-FLT-150: Comentarios dartdoc para APIs públicas

**Prácticas Complementarias:**
- REQ-FLT-021: Protección de datos sensibles (si deep links contienen datos)
- REQ-FLT-110: Try-catch apropiado (manejo de deep links inválidos)

---

### 9. **error-tracking** 🐛

**Prácticas Altamente Relevantes:**
- REQ-FLT-018: Manejo robusto de errores
- REQ-FLT-028: Logging estructurado
- REQ-FLT-036: Monitoreo en producción
- REQ-FLT-091: Crashlytics y Firebase Analytics
- REQ-FLT-110: Try-catch apropiado
- REQ-FLT-150: Comentarios dartdoc para APIs públicas

**Prácticas Complementarias:**
- REQ-FLT-021: Protección de datos sensibles (no loggear PII)
- REQ-FLT-142: Auditoría completa (trazabilidad de errores)

---

### 10. **feature-flags** 🚩

**Prácticas Altamente Relevantes:**
- REQ-FLT-035: Feature Flags implementados
- REQ-FLT-090: Feature Flags con Firebase Remote Config
- REQ-FLT-018: Manejo robusto de errores (fallback si feature flag falla)
- REQ-FLT-150: Comentarios dartdoc para APIs públicas

**Prácticas Complementarias:**
- REQ-FLT-020: Cobertura de testing mínima 80% (tests con/sin flags)
- REQ-FLT-080: Revisión de pares (cambios en feature flags)

---

### 11. **firebase** 🔥

**Prácticas Altamente Relevantes:**
- REQ-FLT-035: Feature Flags con Firebase Remote Config
- REQ-FLT-036: Monitoreo en producción
- REQ-FLT-090: Feature Flags con Firebase Remote Config
- REQ-FLT-091: Crashlytics y Firebase Analytics
- REQ-FLT-021: Protección de datos sensibles
- REQ-FLT-022: Comunicaciones seguras (HTTPS)
- REQ-FLT-032: Cliente HTTP robusto (Dio)
- REQ-FLT-150: Comentarios dartdoc para APIs públicas

**Prácticas Complementarias:**
- REQ-FLT-074: Almacenamiento seguro (Firebase Storage seguro)
- REQ-FLT-089: Estrategia offline-first (Firebase Firestore offline)

---

### 12. **graphql** 📡

**Prácticas Altamente Relevantes:**
- REQ-FLT-032: Cliente HTTP robusto (Dio con GraphQL)
- REQ-FLT-022: Comunicaciones seguras (HTTPS)
- REQ-FLT-033: Estrategia offline-first (GraphQL cache)
- REQ-FLT-034: Paginación obligatoria
- REQ-FLT-086: Dio como cliente HTTP
- REQ-FLT-087: Paginación para listas
- REQ-FLT-110: Try-catch apropiado
- REQ-FLT-111: Async/await consistente
- REQ-FLT-150: Comentarios dartdoc para APIs públicas

**Prácticas Complementarias:**
- REQ-FLT-010: Modelos de datos tipados (GraphQL types)
- REQ-FLT-075: Validación de entradas (validar queries/mutations)

---

### 13. **i18n** 🌍

**Prácticas Altamente Relevantes:**
- REQ-FLT-144: Escalado dinámico de texto (relacionado con i18n)
- REQ-FLT-128: Google Fonts (para soporte multi-idioma)
- REQ-FLT-150: Comentarios dartdoc para APIs públicas
- REQ-FLT-151: Documentar clases y métodos

**Prácticas Complementarias:**
- REQ-FLT-122: Material Design 3 o Cupertino (adaptación por región)
- REQ-FLT-130: LayoutBuilder o MediaQuery (textos más largos en otros idiomas)

---

### 14. **in-app-purchases** 💳

**Prácticas Altamente Relevantes:**
- REQ-FLT-021: Protección de datos sensibles
- REQ-FLT-022: Comunicaciones seguras (HTTPS obligatorio)
- REQ-FLT-074: Almacenamiento seguro
- REQ-FLT-075: Validación de entradas
- REQ-FLT-076: HTTPS obligatorio
- REQ-FLT-018: Manejo robusto de errores
- REQ-FLT-110: Try-catch apropiado
- REQ-FLT-150: Comentarios dartdoc para APIs públicas

**Prácticas Complementarias:**
- REQ-FLT-142: Auditoría completa (trazabilidad de compras)
- REQ-FLT-020: Cobertura de testing mínima 80% (tests críticos)

---

### 15. **modular-architecture** 🧩

**Prácticas Altamente Relevantes:**
- REQ-FLT-015: Arquitectura de tres capas obligatoria
- REQ-FLT-016: Flujo de dependencias unidireccional
- REQ-FLT-017: Inyección de dependencias obligatoria
- REQ-FLT-041: Estructura basada en features
- REQ-FLT-042: Separación estricta de capas
- REQ-FLT-043: Flujo de dependencias controlado
- REQ-FLT-044: Nomenclatura consistente
- REQ-FLT-106: Clases relacionadas en mismo archivo
- REQ-FLT-107: Librerías agrupadas por carpeta

**Prácticas Complementarias:**
- REQ-FLT-019: Código autodocumentado
- REQ-FLT-020: Cobertura de testing mínima 80%

---

### 16. **mvvm** 📱

**Prácticas Altamente Relevantes:**
- REQ-FLT-001: Estructura de presentación obligatoria
- REQ-FLT-002: Separación de responsabilidades en UI
- REQ-FLT-003: Gestión de estado consistente
- REQ-FLT-017: Inyección de dependencias obligatoria
- REQ-FLT-019: Código autodocumentado
- REQ-FLT-027: Inmutabilidad preferida
- REQ-FLT-102: Guías oficiales Effective Dart
- REQ-FLT-111: Async/await consistente

**Prácticas Complementarias:**
- REQ-FLT-020: Cobertura de testing mínima 80%
- REQ-FLT-114: Widgets inmutables

---

### 17. **native-integration** 🔌

**Prácticas Altamente Relevantes:**
- REQ-FLT-018: Manejo robusto de errores
- REQ-FLT-021: Protección de datos sensibles
- REQ-FLT-024: Compatibilidad multiplataforma
- REQ-FLT-110: Try-catch apropiado
- REQ-FLT-150: Comentarios dartdoc para APIs públicas
- REQ-FLT-151: Documentar clases y métodos

**Prácticas Complementarias:**
- REQ-FLT-071: Isolates para tareas intensivas (si hay procesamiento nativo)
- REQ-FLT-020: Cobertura de testing mínima 80%

---

### 18. **offline-first** 📴

**Prácticas Altamente Relevantes:**
- REQ-FLT-033: Estrategia offline-first
- REQ-FLT-088: Detección de conectividad
- REQ-FLT-089: Estrategia offline-first usando SQLite
- REQ-FLT-018: Manejo robusto de errores (errores de sincronización)
- REQ-FLT-034: Paginación obligatoria
- REQ-FLT-087: Paginación para listas
- REQ-FLT-110: Try-catch apropiado
- REQ-FLT-111: Async/await consistente
- REQ-FLT-150: Comentarios dartdoc para APIs públicas

**Prácticas Complementarias:**
- REQ-FLT-009: Fuentes de datos separadas (remote/local)
- REQ-FLT-013: Uso eficiente de memoria (caché local)

---

### 19. **performance** ⚡

**Prácticas Altamente Relevantes:**
- REQ-FLT-011: Fluidez de interfaz (60 FPS)
- REQ-FLT-012: Tiempo de carga inicial (< 3 segundos)
- REQ-FLT-013: Uso eficiente de memoria
- REQ-FLT-014: Operaciones no bloqueantes
- REQ-FLT-066: Constructor const obligatorio
- REQ-FLT-067: ListView.builder para listas grandes
- REQ-FLT-068: RepaintBoundary para widgets costosos
- REQ-FLT-069: Perfilado regular con DevTools
- REQ-FLT-070: No bloquear hilo principal
- REQ-FLT-071: Isolates para tareas intensivas
- REQ-FLT-072: Async/await consistente
- REQ-FLT-114: Widgets inmutables
- REQ-FLT-118: ListView.builder para listas largas
- REQ-FLT-119: Compute para cálculos costosos
- REQ-FLT-120: Constructores const
- REQ-FLT-121: No operaciones costosas en build
- REQ-FLT-139: RepaintBoundary para aislar widgets

**Prácticas Complementarias:**
- REQ-FLT-115: Composición sobre herencia
- REQ-FLT-116: Clases Widget privadas
- REQ-FLT-117: Dividir métodos build grandes

---

### 20. **platform-channels** 🌉

**Prácticas Altamente Relevantes:**
- REQ-FLT-018: Manejo robusto de errores
- REQ-FLT-024: Compatibilidad multiplataforma
- REQ-FLT-110: Try-catch apropiado
- REQ-FLT-111: Async/await consistente
- REQ-FLT-150: Comentarios dartdoc para APIs públicas
- REQ-FLT-151: Documentar clases y métodos

**Prácticas Complementarias:**
- REQ-FLT-021: Protección de datos sensibles (si se pasan datos sensibles)
- REQ-FLT-071: Isolates para tareas intensivas (si hay procesamiento)

---

### 21. **project-setup** ⚙️

**Prácticas Altamente Relevantes:**
- REQ-FLT-015: Arquitectura de tres capas obligatoria
- REQ-FLT-025: Análisis estático obligatorio
- REQ-FLT-026: Formateo consistente
- REQ-FLT-029: Pipeline automatizado
- REQ-FLT-030: Revisión de código obligatoria
- REQ-FLT-031: Versionado semántico
- REQ-FLT-038: Conexión obligatoria al MCP de Dart/Flutter
- REQ-FLT-039: Configuración MCP en herramientas de desarrollo
- REQ-FLT-040: Aprovechamiento de herramientas MCP
- REQ-FLT-044: Nomenclatura consistente
- REQ-FLT-051: Build runner obligatorio
- REQ-FLT-054: Hooks de validación obligatorios
- REQ-FLT-055: Pipeline completo obligatorio
- REQ-FLT-082: Commits atómicos
- REQ-FLT-083: Feature branches
- REQ-FLT-084: Tags semánticos
- REQ-FLT-085: Versionado semántico
- REQ-FLT-094: Servidor MCP configurado
- REQ-FLT-095: Versión SDK compatible
- REQ-FLT-096: Verificación de conexión MCP

**Prácticas Complementarias:**
- REQ-FLT-037: Dependencias actualizadas
- REQ-FLT-092: Dependencias actualizadas mensualmente

---

### 22. **push-notifications** 🔔

**Prácticas Altamente Relevantes:**
- REQ-FLT-018: Manejo robusto de errores
- REQ-FLT-021: Protección de datos sensibles (tokens)
- REQ-FLT-022: Comunicaciones seguras
- REQ-FLT-074: Almacenamiento seguro (tokens)
- REQ-FLT-110: Try-catch apropiado
- REQ-FLT-111: Async/await consistente
- REQ-FLT-150: Comentarios dartdoc para APIs públicas

**Prácticas Complementarias:**
- REQ-FLT-024: Compatibilidad multiplataforma (iOS/Android)
- REQ-FLT-075: Validación de entradas (validar payloads)

---

### 23. **riverpod** 🏞️

**Prácticas Altamente Relevantes:**
- REQ-FLT-003: Gestión de estado consistente
- REQ-FLT-017: Inyección de dependencias obligatoria
- REQ-FLT-019: Código autodocumentado
- REQ-FLT-020: Cobertura de testing mínima 80%
- REQ-FLT-027: Inmutabilidad preferida
- REQ-FLT-102: Guías oficiales Effective Dart
- REQ-FLT-103: Null safety consistente
- REQ-FLT-111: Async/await consistente
- REQ-FLT-112: Streams para eventos asíncronos

**Prácticas Complementarias:**
- REQ-FLT-015: Arquitectura de tres capas obligatoria
- REQ-FLT-016: Flujo de dependencias unidireccional

---

### 24. **security** 🔒

**Prácticas Altamente Relevantes:**
- REQ-FLT-021: Protección de datos sensibles
- REQ-FLT-022: Comunicaciones seguras
- REQ-FLT-023: Validación de entrada
- REQ-FLT-073: No hardcodear claves
- REQ-FLT-074: Almacenamiento seguro
- REQ-FLT-075: Validación de entradas
- REQ-FLT-076: HTTPS obligatorio
- REQ-FLT-077: Ofuscación en producción
- REQ-FLT-142: Auditoría completa
- REQ-FLT-150: Comentarios dartdoc para APIs públicas

**Prácticas Complementarias:**
- REQ-FLT-018: Manejo robusto de errores (sin exponer información sensible)
- REQ-FLT-028: Logging estructurado (sin PII)

---

### 25. **testing** 🧪

**Prácticas Altamente Relevantes:**
- REQ-FLT-020: Cobertura de testing mínima 80%
- REQ-FLT-029: Pipeline automatizado
- REQ-FLT-030: Revisión de código obligatoria
- REQ-FLT-078: Pipeline con linter y tests
- REQ-FLT-079: PRs deben pasar lint
- REQ-FLT-080: Revisión de pares
- REQ-FLT-081: Cobertura mínima de tests 80%
- REQ-FLT-150: Comentarios dartdoc para APIs públicas

**Prácticas Complementarias:**
- REQ-FLT-019: Código autodocumentado (código testeable)
- REQ-FLT-027: Inmutabilidad preferida (facilita testing)

---

### 26. **theming** 🎨

**Prácticas Altamente Relevantes:**
- REQ-FLT-055: Theming centralizado obligatorio
- REQ-FLT-056: Layouts responsivos obligatorios
- REQ-FLT-057: Esquemas de color accesibles
- REQ-FLT-122: Material Design 3 o Cupertino
- REQ-FLT-123: Soporte para temas claro y oscuro
- REQ-FLT-124: ColorScheme.fromSeed
- REQ-FLT-125: ThemeData centralizado
- REQ-FLT-126: Theme.of(context).textTheme
- REQ-FLT-127: Contraste mínimo 4.5:1
- REQ-FLT-128: Google Fonts
- REQ-FLT-129: Regla 60-30-10 para colores
- REQ-FLT-130: LayoutBuilder o MediaQuery
- REQ-FLT-131: Optimización para diferentes pantallas
- REQ-FLT-132: Flexible y Expanded apropiados
- REQ-FLT-133: Wrap para contenido overflow
- REQ-FLT-150: Comentarios dartdoc para APIs públicas

**Prácticas Complementarias:**
- REQ-FLT-141: Semantics para accesibilidad (temas accesibles)
- REQ-FLT-143: Contraste mínimo para texto

---

### 27. **webview-integration** 🌐

**Prácticas Altamente Relevantes:**
- REQ-FLT-018: Manejo robusto de errores
- REQ-FLT-021: Protección de datos sensibles
- REQ-FLT-022: Comunicaciones seguras
- REQ-FLT-076: HTTPS obligatorio
- REQ-FLT-110: Try-catch apropiado
- REQ-FLT-111: Async/await consistente
- REQ-FLT-150: Comentarios dartdoc para APIs públicas

**Prácticas Complementarias:**
- REQ-FLT-024: Compatibilidad multiplataforma
- REQ-FLT-075: Validación de entradas (validar URLs)

---

### 28. **feature-first** 🎯

**Prácticas Altamente Relevantes:**
- REQ-FLT-015: Arquitectura de tres capas obligatoria
- REQ-FLT-016: Flujo de dependencias unidireccional
- REQ-FLT-017: Inyección de dependencias obligatoria
- REQ-FLT-041: Estructura basada en features
- REQ-FLT-042: Separación estricta de capas
- REQ-FLT-043: Flujo de dependencias controlado
- REQ-FLT-044: Nomenclatura consistente
- REQ-FLT-106: Clases relacionadas en mismo archivo
- REQ-FLT-107: Librerías agrupadas por carpeta

**Prácticas Complementarias:**
- REQ-FLT-019: Código autodocumentado
- REQ-FLT-020: Cobertura de testing mínima 80%

---

## 📝 Notas de Implementación

### Cómo Usar Este Mapeo

**Para Agentes de IA:**

Cuando se invoque un skill de Flutter, los agentes DEBEN:

1. **Consultar este documento** para identificar prácticas relevantes del skill
2. **Aplicar las prácticas "Altamente Relevantes"** como obligatorias
3. **Considerar las prácticas "Complementarias"** según el contexto
4. **Referenciar los códigos REQ-FLT-XXX** en la implementación
5. **Validar que el código generado cumple** con las prácticas identificadas

**Ejemplo de Uso:**

```
Usuario: "Implementa accessibility con semantic widgets"

Agente:
1. Detecta skill: accessibility
2. Consulta BEST_PRACTICES_MAPPING.md → Sección 1 (accessibility)
3. Identifica prácticas relevantes:
   - REQ-FLT-060: Labels semánticos obligatorios
   - REQ-FLT-061: Contraste mínimo obligatorio
   - REQ-FLT-142: Accesibilidad según WCAG 2.1
   - etc.
4. Genera código que cumple con estas prácticas
5. Valida implementación contra REQ-FLT-XXX
```

### Integración con AGENTS.md

Este documento está referenciado en `AGENTS.md` en la sección de Flutter Skills. Los agentes deben consultarlo automáticamente cuando:

- Se invoque cualquier skill de Flutter
- Se necesite validar que el código cumple con mejores prácticas
- Se requiera identificar requisitos específicos para un skill

### Referencias Cruzadas

Cada práctica está identificada con un código `REQ-FLT-XXX` que corresponde a un requisito específico en `flutter-best-practices.md`. Los agentes pueden:

- Consultar el requisito completo en `flutter-best-practices.md`
- Aplicar la práctica en el contexto del skill específico
- Validar el cumplimiento durante la implementación

---

## 🔄 Actualización Continua

Este documento debe actualizarse cuando:
- Se agreguen nuevos requisitos a `flutter-best-practices.md`
- Se creen nuevos skills en la carpeta `flutter/`
- Se identifiquen prácticas adicionales relevantes para skills existentes

---

**Última actualización:** Diciembre 2025
**Versión:** 1.0.0
