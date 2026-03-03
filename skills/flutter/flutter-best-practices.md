# Especificación de Requisitos Software: Buenas Prácticas Flutter con Clean Architecture

## 1. Introducción

Este documento establece la especificación completa de requisitos para el desarrollo de aplicaciones móviles Flutter siguiendo los principios de Clean Architecture, aplicable a todos los proyectos de desarrollo móvil.

### 1.1. Propósito

Este ERS define los estándares obligatorios, reglas arquitectónicas y mejores prácticas para el desarrollo de aplicaciones Flutter de alta calidad, mantenibles y escalables. Está dirigido a:

- Desarrolladores Flutter/Dart
- Arquitectos de software
- Tech leads y líderes de equipo
- Equipos de QA y testing
- DevOps engineers

### 1.2. Ámbito del Sistema

**Sistema:** Framework de desarrollo Flutter con Clean Architecture

**Funcionalidades que incluye:**

- Estructura arquitectónica de tres capas (Presentación, Dominio, Datos)
- Patrones de diseño y organización de código
- Gestión de estado y dependencias
- Estrategias de testing y CI/CD
- Seguridad y rendimiento

**Funcionalidades que NO incluye:**

- Implementaciones específicas de backend
- Configuraciones de infraestructura cloud
- Diseño visual o UX específico

**Beneficios esperados:**

- Código modular y reutilizable
- Facilidad de mantenimiento a largo plazo
- Escalabilidad del proyecto
- Reducción de bugs y mejora en testing
- Desarrollo colaborativo eficiente

### 1.3. Definiciones, Acrónimos y Abreviaturas

- **Clean Architecture**: Arquitectura de software que separa responsabilidades en capas concéntricas
- **DI**: Dependency Injection (Inyección de Dependencias)
- **BLoC**: Business Logic Component
- **CI/CD**: Continuous Integration/Continuous Deployment
- **ERS**: Especificación de Requisitos Software
- **ADR**: Architecture Decision Record
- **SemVer**: Semantic Versioning

### 1.4. Referencias

- Robert C. Martin - Clean Architecture: A Craftsman's Guide to Software Structure and Design
- IEEE Std 830-1998 - IEEE Recommended Practice for Software Requirements Specifications
- Flutter Documentation - https://docs.flutter.dev/
- Dart Language Specification

### 1.5. Visión General del Documento

Este documento se organiza en secciones que cubren desde los fundamentos arquitectónicos hasta los requisitos específicos de implementación, incluyendo estructura de proyecto, reglas de código, testing y despliegue.

## 2. Descripción General

### 2.1. Perspectiva del Producto

El framework de desarrollo Flutter con Clean Architecture es un sistema independiente que define la estructura y patrones para aplicaciones móviles. Se integra con:

- Sistemas de control de versiones (Git)
- Pipelines de CI/CD
- Herramientas de análisis estático
- Plataformas de monitoreo y analytics

### 2.2. Funciones del Producto

**Funciones principales:**

- Organización arquitectónica en tres capas bien definidas
- Gestión de estado centralizada y predecible
- Inyección de dependencias para desacoplamiento
- Testing automatizado y cobertura de código
- Optimización de rendimiento y UI
- Seguridad en manejo de datos sensibles

### 2.3. Características de los Usuarios

**Desarrolladores Flutter:**

- Nivel educacional: Técnico superior o universitario en informática
- Experiencia: Intermedio a avanzado en desarrollo móvil
- Conocimientos técnicos: Dart, Flutter, patrones de diseño, arquitectura de software

**Arquitectos de Software:**

- Nivel educacional: Universitario en informática o ingeniería
- Experiencia: Avanzado en diseño de sistemas
- Conocimientos técnicos: Principios SOLID, Clean Architecture, patrones arquitectónicos

### 2.4. Restricciones

- **Tecnológicas**: Uso obligatorio de Flutter SDK y Dart
- **Arquitectónicas**: Implementación estricta de Clean Architecture
- **Rendimiento**: Aplicaciones deben mantener 60 FPS en dispositivos objetivo
- **Seguridad**: Cumplimiento con estándares de protección de datos
- **Compatibilidad**: Soporte para iOS 12+ y Android API 21+

### 2.5. Suposiciones y Dependencias

- Disponibilidad de Flutter SDK estable
- Acceso a repositorios de paquetes (pub.dev)
- Herramientas de desarrollo (IDE, emuladores)
- Conectividad a internet para dependencias externas
- Sistemas de CI/CD configurados

### 2.6. Requisitos Futuros

- Soporte para Flutter Web y Desktop
- Integración con herramientas de análisis de código avanzadas
- Automatización completa de testing E2E
- Métricas avanzadas de rendimiento en producción

## 3. Requisitos Específicos

### 3.0.1. Convenciones de redacción de requisitos

Para mejorar la legibilidad, cada requisito incluye un código identificador único y título descriptivo:

**Formato:** `REQ-FLT-XXX: Título descriptivo`

Ejemplo:

```
**REQ-FLT-XXX: Título descriptivo del requisito**

CUANDO [condición] ENTONCES el sistema DEBERÁ [acción obligatoria].
```

### 3.1. Interfaces Externas

#### 3.1.1. Interfaz de Usuario

- Las aplicaciones deben seguir Material Design 3 o Cupertino Design
- Soporte para temas claro y oscuro
- Accesibilidad completa según WCAG 2.1

#### 3.1.2. Interfaces de Hardware

- Acceso a cámara, GPS, almacenamiento según permisos
- Optimización para diferentes tamaños de pantalla
- Soporte para gestos nativos de cada plataforma

#### 3.1.3. Interfaces de Software

- APIs REST mediante cliente HTTP configurado
- Bases de datos locales SQLite
- Servicios de autenticación OAuth 2.0

### 3.2. Funciones

Organización por **jerarquía funcional** según Clean Architecture:

#### 3.2.1. Capa de Presentación (Presentation Layer)

**REQ-FLT-001: Estructura de presentación obligatoria**

CUANDO se implemente la capa de presentación ENTONCES el sistema DEBERÁ organizar los componentes en:

- Pages: Pantallas completas de la aplicación
- State Management: Gestión de estado (BLoC, Riverpod, etc.)
- Widgets: Componentes reutilizables de UI

**REQ-FLT-002: Separación de responsabilidades en UI**

CUANDO se desarrollen widgets ENTONCES estos DEBERÁN ser puramente presentacionales, sin lógica de negocio embebida.

**REQ-FLT-003: Gestión de estado consistente**

CUANDO se maneje estado ENTONCES se DEBERÁ usar una única solución de gestión de estado por proyecto (BLoC, Riverpod, Provider, GetX o MobX).

#### 3.2.2. Capa de Dominio (Domain Layer)

**REQ-FLT-004: Independencia de framework**

CUANDO se implemente la capa de dominio ENTONCES esta DEBERÁ contener únicamente código Dart puro, sin dependencias de Flutter.

**REQ-FLT-005: Definición de entidades**

CUANDO se definan entidades ENTONCES estas DEBERÁN representar los objetos de negocio principales con sus propiedades y comportamientos esenciales.

**REQ-FLT-006: Contratos de repositorio**

CUANDO se definan repositorios ENTONCES estos DEBERÁN ser interfaces abstractas que especifiquen los métodos de acceso a datos sin implementación concreta.

**REQ-FLT-007: Casos de uso específicos**

CUANDO se implementen casos de uso ENTONCES cada uno DEBERÁ encapsular una única regla de negocio y actuar como orquestador entre presentación y datos.

#### 3.2.3. Capa de Datos (Data Layer)

**REQ-FLT-008: Implementación de repositorios**

CUANDO se implementen repositorios ENTONCES estos DEBERÁN coordinar entre fuentes de datos remotas y locales según la lógica de negocio.

**REQ-FLT-009: Fuentes de datos separadas**

CUANDO se gestionen datos ENTONCES se DEBERÁN separar las fuentes remotas (APIs) de las locales (caché, base de datos).

**REQ-FLT-010: Modelos de datos tipados**

CUANDO se definan modelos ENTONCES estos DEBERÁN representar la estructura exacta de los datos de las fuentes externas con serialización/deserialización automática.

### 3.3. Requisitos de Rendimiento

**REQ-FLT-011: Fluidez de interfaz**

CUANDO la aplicación esté en uso ENTONCES DEBERÁ mantener 60 FPS constantes en dispositivos objetivo.

**REQ-FLT-012: Tiempo de carga inicial**

CUANDO se inicie la aplicación ENTONCES el tiempo de carga inicial NO DEBERÁ exceder 3 segundos en dispositivos de gama media.

**REQ-FLT-013: Uso eficiente de memoria**

CUANDO se rendericen listas grandes ENTONCES se DEBERÁ usar ListView.builder o equivalentes para renderizado bajo demanda.

**REQ-FLT-014: Operaciones no bloqueantes**

CUANDO se ejecuten tareas intensivas ENTONCES estas DEBERÁN ejecutarse en Isolates o usando compute() para no bloquear el hilo principal.

### 3.4. Restricciones de Diseño

**REQ-FLT-015: Arquitectura de tres capas obligatoria**

CUANDO se desarrolle cualquier feature ENTONCES DEBERÁ implementar estrictamente las tres capas: Presentación, Dominio y Datos.

**REQ-FLT-016: Flujo de dependencias unidireccional**

CUANDO se establezcan dependencias ENTONCES estas DEBERÁN fluir únicamente desde capas externas hacia capas internas (Presentación → Dominio ← Datos).

**REQ-FLT-017: Inyección de dependencias obligatoria**

CUANDO se requieran dependencias ENTONCES estas DEBERÁN inyectarse usando GetIt, Riverpod o sistema equivalente, prohibiendo el hardcoding.

### 3.5. Atributos del Sistema

#### 3.5.1. Fiabilidad

**REQ-FLT-018: Manejo de errores robusto**

CUANDO ocurran errores ENTONCES el sistema DEBERÁ capturarlos, registrarlos y mostrar mensajes apropiados al usuario sin crashear.

#### 3.5.2. Mantenibilidad

**REQ-FLT-019: Código autodocumentado**

CUANDO se escriba código ENTONCES DEBERÁ ser legible y autodocumentado, evitando complejidad innecesaria.

**REQ-FLT-020: Cobertura de testing mínima**

CUANDO se desarrollen features ENTONCES DEBERÁN tener una cobertura de tests unitarios mínima del 80%.

#### 3.5.3. Seguridad

**REQ-FLT-021: Protección de datos sensibles**

CUANDO se manejen datos sensibles ENTONCES estos DEBERÁN almacenarse usando flutter_secure_storage o equivalente con cifrado.

**REQ-FLT-022: Comunicaciones seguras**

CUANDO se realicen comunicaciones de red ENTONCES estas DEBERÁN usar exclusivamente HTTPS con validación de certificados.

**REQ-FLT-023: Validación de entrada**

CUANDO se reciban datos del usuario o APIs ENTONCES estos DEBERÁN validarse tanto en cliente como en servidor.

#### 3.5.4. Portabilidad

**REQ-FLT-024: Compatibilidad multiplataforma**

CUANDO se desarrolle la aplicación ENTONCES DEBERÁ funcionar correctamente en iOS 12+ y Android API 21+ sin modificaciones específicas de plataforma innecesarias.

### 3.6. Otros Requisitos

#### 3.6.1. Requisitos de Calidad de Código

**REQ-FLT-025: Análisis estático obligatorio**

CUANDO se escriba código ENTONCES DEBERÁ pasar las validaciones de flutter_lints con configuración estricta en analysis_options.yaml.

**REQ-FLT-026: Formateo consistente**

CUANDO se realice un commit ENTONCES el código DEBERÁ estar formateado usando flutter format.

**REQ-FLT-027: Inmutabilidad preferida**

CUANDO se declaren variables ENTONCES se DEBERÁ usar final para valores inmutables, evitando var innecesario.

**REQ-FLT-028: Logging estructurado**

CUANDO se requiera logging ENTONCES se DEBERÁ usar debugPrint() o paquete logger, prohibiendo print().

#### 3.6.2. Requisitos de Testing y CI/CD

**REQ-FLT-029: Pipeline automatizado**

CUANDO se integre código ENTONCES DEBERÁ pasar por pipeline CI/CD que incluya linting, testing y build.

**REQ-FLT-030: Revisión de código obligatoria**

CUANDO se cree un Pull Request ENTONCES DEBERÁ ser revisado y aprobado por al menos un desarrollador senior.

**REQ-FLT-031: Versionado semántico**

CUANDO se publique una release ENTONCES DEBERÁ seguir versionado semántico (Major.Minor.Patch).

#### 3.6.3. Requisitos de Conectividad

**REQ-FLT-032: Cliente HTTP robusto**

CUANDO se realicen peticiones HTTP ENTONCES se DEBERÁ usar Dio con interceptores para logging, retry y headers automáticos.

**REQ-FLT-033: Estrategia offline-first**

CUANDO se diseñe la aplicación ENTONCES DEBERÁ funcionar sin conexión usando almacenamiento local SQLite y sincronizar cuando haya conectividad.

**REQ-FLT-034: Paginación obligatoria**

CUANDO se carguen listas de datos ENTONCES se DEBERÁ implementar paginación para optimizar memoria y datos.

#### 3.6.4. Requisitos de Despliegue

**REQ-FLT-035: Feature flags implementados**

CUANDO se despliegue a producción ENTONCES se DEBERÁN usar Feature Flags con Firebase Remote Config para control remoto de funcionalidades.

**REQ-FLT-036: Monitoreo en producción**

CUANDO la aplicación esté en producción ENTONCES DEBERÁ tener Crashlytics y Firebase Analytics configurados para monitoreo.

**REQ-FLT-037: Dependencias actualizadas**

CUANDO se mantenga la aplicación ENTONCES las dependencias DEBERÁN actualizarse mensualmente usando flutter pub outdated y flutter pub upgrade.

#### 3.6.5. Requisitos de Integración con AI/MCP

**REQ-FLT-038: Conexión obligatoria al MCP de Dart/Flutter**

CUANDO se configure el entorno de desarrollo ENTONCES se DEBERÁ conectar al servidor MCP (Model Context Protocol) de Dart/Flutter para habilitar asistencia de AI avanzada.

**REQ-FLT-039: Configuración MCP en herramientas de desarrollo**

CUANDO se use un IDE compatible ENTONCES se DEBERÁ configurar el servidor MCP de Dart/Flutter según la herramienta:

- VS Code: Configurar `dart.mcpServer` en settings
- Cursor: Usar configuración en `.cursor/mcp.json`
- Kiro: Usar configuración en `.kiro/settings/mcp.json` (workspace)
- Gemini CLI: Configurar en `mcpServers` section
- Firebase Studio: Configurar en `.idx/mcp.json`

**REQ-FLT-040: Aprovechamiento de herramientas MCP**

CUANDO se desarrolle con asistencia de AI ENTONCES se DEBERÁN aprovechar las herramientas MCP para:

- Análisis automático de código y detección de issues
- Búsqueda y adición inteligente de paquetes
- Generación de código siguiendo Clean Architecture
- Debugging asistido de layout y runtime errors
- Refactoring automático siguiendo best practices

## 4. Apéndices

### 4.1. Estructura de Proyecto Prescriptiva según Clean Architecture

#### 4.1.1. Organización Principal por Features

**REQ-FLT-041: Estructura basada en features**

CUANDO se organice el proyecto ENTONCES DEBERÁ seguir la estructura basada en features con Clean Architecture:

```
lib/
├── config/                    # Configuraciones globales
│   ├── theme/                # Temas visuales
│   └── routes/               # Rutas de navegación
├── core/                     # Código compartido entre features
│   ├── constants/           # Constantes globales
│   ├── errors/              # Manejo de errores
│   ├── network/             # Configuración de red
│   ├── utils/               # Utilidades compartidas
│   └── use_cases/           # Casos de uso comunes
├── features/                 # Features organizadas por dominio
│   ├── auxilio/             # Feature de auxilio
│   │   ├── presentation/    # Capa de presentación
│   │   │   ├── pages/       # Páginas/pantallas
│   │   │   ├── state_management/ # BLoC/Riverpod/etc
│   │   │   └── widgets/     # Widgets específicos
│   │   ├── domain/          # Capa de dominio
│   │   │   ├── entities/    # Entidades de negocio
│   │   │   ├── repositories/ # Interfaces de repositorio
│   │   │   └── use_cases/   # Casos de uso específicos
│   │   └── data/            # Capa de datos
│   │       ├── models/      # Modelos de datos
│   │       ├── repositories/ # Implementaciones de repositorio
│   │       └── data_sources/ # Fuentes de datos (remote/local)
│   ├── rescate/             # Feature de rescate
│   │   ├── presentation/
│   │   ├── domain/
│   │   └── data/
│   └── adopcion/            # Feature de adopción
│       ├── presentation/
│       ├── domain/
│       └── data/
└── main.dart                # Punto de entrada
```

#### 4.1.2. Principios de Organización

**REQ-FLT-042: Separación estricta de capas**

CUANDO se implemente cada feature ENTONCES DEBERÁ mantener separación estricta entre las tres capas:

1. **Capa de Presentación**: Solo UI y gestión de estado de UI
2. **Capa de Dominio**: Solo lógica de negocio pura en Dart
3. **Capa de Datos**: Solo acceso y transformación de datos

**REQ-FLT-043: Flujo de dependencias controlado**

CUANDO se establezcan dependencias ENTONCES DEBERÁN seguir el flujo:

- Presentación depende de Dominio
- Datos implementa interfaces de Dominio
- Dominio NO depende de ninguna capa externa

#### 4.1.3. Componentes por Capa

**Capa de Presentación:**

- **Pages**: Pantallas completas que actúan como contenedores principales
- **State Management**: Archivos de BLoC, Cubit, Riverpod providers, etc.
- **Widgets**: Componentes reutilizables específicos del feature

**Capa de Dominio:**

- **Entities**: Objetos de negocio con propiedades y comportamientos esenciales
- **Repositories**: Interfaces abstractas que definen contratos de datos
- **Use Cases**: Reglas de negocio específicas, una por funcionalidad

**Capa de Datos:**

- **Models**: Representación de datos de fuentes externas con serialización
- **Repositories**: Implementaciones concretas de las interfaces de dominio
- **Data Sources**: Separación entre fuentes remotas (API) y locales (caché/DB)

### 4.2. Convenciones de Nomenclatura

**REQ-FLT-044: Nomenclatura consistente**

CUANDO se nombren elementos del código ENTONCES se DEBERÁN seguir estas convenciones:

- **Archivos**: `snake_case.dart` (ej: `user_profile_page.dart`)
- **Clases**: `PascalCase` (ej: `UserProfilePage`)
- **Variables y funciones**: `camelCase` (ej: `getUserProfile()`)
- **Constantes**: `SCREAMING_SNAKE_CASE` (ej: `API_BASE_URL`)
- **Interfaces de repositorio**: `I[Nombre]Repository` (ej: `IUserRepository`)
- **Implementaciones**: `[Nombre]RepositoryImpl` (ej: `UserRepositoryImpl`)
- **Casos de uso**: `[Verbo][Objeto]UseCase` (ej: `GetUserProfileUseCase`)
- **Modelos**: `[Nombre]Model` (ej: `UserModel`)
- **Entidades**: `[Nombre]Entity` o simplemente `[Nombre]` (ej: `User`)

### 4.3. Configuración MCP (Model Context Protocol) Obligatoria

#### 4.3.1. Configuración para VS Code

**REQ-FLT-045: Configuración MCP en VS Code**

CUANDO se use VS Code ENTONCES se DEBERÁ configurar el servidor MCP de Dart/Flutter:

```json
// settings.json (User o Workspace)
{
  "dart.mcpServer": true
}
```

#### 4.3.2. Configuración para Cursor

**REQ-FLT-046: Configuración MCP en Cursor**

CUANDO se use Cursor ENTONCES se DEBERÁ configurar el servidor MCP:

```json
// .cursor/mcp.json (local) o ~/.cursor/mcp.json (global)
{
  "mcpServers": {
    "dart": {
      "type": "stdio",
      "command": "dart",
      "args": [
        "mcp-server",
        "--experimental-mcp-server",
        "--force-roots-fallback"
      ]
    }
  }
}
```

#### 4.3.3. Configuración para Kiro

**REQ-FLT-047: Configuración MCP en Kiro**

CUANDO se use Kiro ENTONCES se DEBERÁ configurar el servidor MCP usando el archivo de workspace:

```json
// .kiro/settings/mcp.json (workspace - RECOMENDADO)
{
  "mcpServers": {
    "dart": {
      "command": "dart",
      "args": [
        "mcp-server",
        "--experimental-mcp-server",
        "--force-roots-fallback"
      ],
      "disabled": false,
      "autoApprove": ["dart_analyze", "dart_format", "pub_search", "pub_add"]
    }
  }
}
```

#### 4.3.4. Configuración para Gemini CLI

**REQ-FLT-048: Configuración MCP en Gemini CLI**

CUANDO se use Gemini CLI ENTONCES se DEBERÁ añadir la configuración MCP:

```json
// Gemini config
{
  "mcpServers": {
    "dart": {
      "type": "stdio",
      "command": "dart",
      "args": ["mcp-server", "--experimental-mcp-server"]
    }
  }
}
```

#### 4.3.5. Configuración para Firebase Studio

**REQ-FLT-049: Configuración MCP en Firebase Studio**

CUANDO se use Firebase Studio ENTONCES se DEBERÁ crear `.idx/mcp.json`:

```json
{
  "mcpServers": {
    "dart": {
      "type": "stdio",
      "command": "dart",
      "args": ["mcp-server", "--experimental-mcp-server"]
    }
  }
}
```

#### 4.3.6. Verificación de Configuración MCP

**REQ-FLT-050: Verificación de conexión MCP**

CUANDO se configure MCP ENTONCES se DEBERÁ verificar que:

- El comando `dart mcp-server` esté disponible
- La versión de Dart SDK sea 3.9+ o Flutter 3.35+
- El cliente MCP reconozca el servidor (ej: `/mcp` en Gemini Code Assist)
- Las herramientas MCP estén disponibles para el AI assistant

### 4.4. Configuración de Desarrollo Obligatoria

#### 4.4.1. analysis_options.yaml

**REQ-FLT-051: Build runner obligatorio para generación de código**

CUANDO se use generación de código ENTONCES se DEBERÁ configurar build_runner:

```bash
# Comando para generar código
dart run build_runner build --delete-conflicting-outputs

# Para desarrollo continuo
dart run build_runner watch --delete-conflicting-outputs
```

```yaml
include: package:flutter_lints/flutter.yaml

analyzer:
  exclude:
    - "**/*.g.dart"
    - "**/*.freezed.dart"

linter:
  rules:
    - prefer_const_constructors
    - prefer_const_literals_to_create_immutables
    - avoid_print
    - prefer_final_locals
    - unnecessary_null_checks
```

#### 4.4.2. pubspec.yaml - Dependencias Aprobadas para Clean Architecture

```yaml
dependencies:
  # Clean Architecture - Inyección de Dependencias
  get_it: ^7.6.0 # Service locator para DI
  injectable: ^2.3.0 # Generación automática de DI

  # Clean Architecture - Gestión de Estado
  flutter_bloc: ^8.1.0 # BLoC pattern (recomendado)
  # O alternativamente:
  # riverpod: ^2.4.0          # Riverpod (alternativa)

  # Clean Architecture - Casos de Uso
  dartz: ^0.10.1 # Either para manejo de errores funcional
  equatable: ^2.0.5 # Comparación de objetos inmutables

  # Capa de Datos - Red y almacenamiento
  dio: ^5.3.0 # Cliente HTTP robusto
  retrofit: ^4.0.0 # Generación de clientes API
  connectivity_plus: ^5.0.0 # Detección de conectividad
  flutter_secure_storage: ^9.0.0 # Almacenamiento seguro
  sqflite: ^2.3.0 # Base de datos local
  hive: ^2.2.3 # Alternativa NoSQL local

  # Serialización JSON
  json_annotation: ^4.8.0 # Anotaciones para JSON
  freezed_annotation: ^2.4.0 # Inmutabilidad y serialización

  # UI y utilidades
  go_router: ^12.0.0 # Navegación declarativa
  cached_network_image: ^3.3.0 # Caché de imágenes

dev_dependencies:
  # Análisis y calidad
  flutter_lints: ^3.0.0 # Linting estricto
  very_good_analysis: ^5.1.0 # Reglas adicionales de calidad

  # Testing
  mockito: ^5.4.0 # Mocking para tests
  bloc_test: ^9.1.0 # Testing específico para BLoC

  # Generación de código
  build_runner: ^2.4.0 # Ejecutor de generadores
  injectable_generator: ^2.4.0 # Generador de DI
  json_serializable: ^6.7.0 # Generador de serialización JSON
  retrofit_generator: ^8.0.0 # Generador de clientes API
  freezed: ^2.4.0 # Generador de clases inmutables

  # Testing adicional
  integration_test: # Testing E2E (SDK Flutter)
    sdk: flutter
  checks: ^0.3.0 # Assertions más expresivas
```

### 4.5. Routing y Navigation

#### 4.5.1. GoRouter Configuration

**REQ-FLT-052: Routing declarativo obligatorio**

CUANDO se implemente navegación ENTONCES se DEBERÁ usar GoRouter:

```dart
// Configuración básica de GoRouter
final GoRouter _router = GoRouter(
  routes: <RouteBase>[
    GoRoute(
      path: '/',
      builder: (context, state) => const HomeScreen(),
      routes: <RouteBase>[
        GoRoute(
          path: 'profile/:userId',
          builder: (context, state) {
            final userId = state.pathParameters['userId']!;
            return ProfileScreen(userId: userId);
          },
        ),
        GoRoute(
          path: 'settings',
          builder: (context, state) => const SettingsScreen(),
        ),
      ],
    ),
  ],
  // Manejo de autenticación
  redirect: (context, state) {
    final isLoggedIn = AuthService.instance.isLoggedIn;
    final isLoggingIn = state.matchedLocation == '/login';

    if (!isLoggedIn && !isLoggingIn) {
      return '/login';
    }
    if (isLoggedIn && isLoggingIn) {
      return '/';
    }
    return null;
  },
);

// Uso en MaterialApp
MaterialApp.router(
  routerConfig: _router,
  title: '{{PROJECT_NAME}}',
)
```

#### 4.5.2. Navigation Patterns

**REQ-FLT-053: Patrones de navegación consistentes**

CUANDO se navegue ENTONCES se DEBERÁN usar patrones consistentes:

```dart
// Navegación programática con GoRouter
void navigateToProfile(String userId) {
  context.go('/profile/$userId');
}

// Navegación con parámetros de query
void navigateToSearch({String? query}) {
  context.go('/search${query != null ? '?q=$query' : ''}');
}

// Navegación modal para pantallas temporales
void showUserDialog() {
  showDialog(
    context: context,
    builder: (context) => const UserDialog(),
  );
}

// Bottom sheets para acciones contextuales
void showActionSheet() {
  showModalBottomSheet(
    context: context,
    builder: (context) => const ActionSheet(),
  );
}
```

### 4.6. Validaciones Automáticas

#### 4.6.1. Pre-commit Hooks

**REQ-FLT-054: Hooks de validación obligatorios**

CUANDO se configure el proyecto ENTONCES se DEBERÁN establecer pre-commit hooks que ejecuten:

- `flutter analyze` - Análisis estático
- `flutter format --set-exit-if-changed` - Formateo consistente
- `flutter test` - Ejecución de tests unitarios
- `dart run build_runner build` - Generación de código

#### 4.6.2. Pipeline CI/CD

**REQ-FLT-055: Pipeline completo obligatorio**

CUANDO se configure CI/CD ENTONCES el pipeline DEBERÁ incluir:

- Análisis estático con flutter_lints
- Ejecución completa de test suite
- Verificación de cobertura mínima (80%)
- Build de APK/IPA para validación
- Análisis de seguridad de dependencias

### 4.7. Guías de Visual Design y Theming

#### 4.7.1. Implementación de Material Design 3

**REQ-FLT-055: Theming centralizado obligatorio**

CUANDO se implemente theming ENTONCES se DEBERÁ definir un ThemeData centralizado:

```dart
// Configuración de tema recomendada
final ThemeData lightTheme = ThemeData(
  colorScheme: ColorScheme.fromSeed(
    seedColor: Colors.deepPurple,
    brightness: Brightness.light,
  ),
  textTheme: GoogleFonts.robotoTextTheme(),
  elevatedButtonTheme: ElevatedButtonThemeData(
    style: ElevatedButton.styleFrom(
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(12),
      ),
    ),
  ),
);

final ThemeData darkTheme = ThemeData(
  colorScheme: ColorScheme.fromSeed(
    seedColor: Colors.deepPurple,
    brightness: Brightness.dark,
  ),
  textTheme: GoogleFonts.robotoTextTheme(ThemeData.dark().textTheme),
);
```

#### 4.7.2. Responsive Design Patterns

**REQ-FLT-056: Layouts responsivos obligatorios**

CUANDO se diseñen layouts ENTONCES se DEBERÁN usar patrones responsivos:

```dart
// Ejemplo de layout responsivo
class ResponsiveLayout extends StatelessWidget {
  const ResponsiveLayout({super.key});

  @override
  Widget build(BuildContext context) {
    return LayoutBuilder(
      builder: (context, constraints) {
        if (constraints.maxWidth > 1200) {
          return const DesktopLayout();
        } else if (constraints.maxWidth > 800) {
          return const TabletLayout();
        } else {
          return const MobileLayout();
        }
      },
    );
  }
}

// Uso de MediaQuery para información de pantalla
Widget buildResponsiveWidget(BuildContext context) {
  final screenSize = MediaQuery.of(context).size;
  final isLargeScreen = screenSize.width > 600;

  return Container(
    padding: EdgeInsets.all(isLargeScreen ? 24.0 : 16.0),
    child: isLargeScreen
      ? const WideScreenContent()
      : const NarrowScreenContent(),
  );
}
```

#### 4.7.3. Color Scheme Best Practices

**REQ-FLT-057: Esquemas de color accesibles**

CUANDO se definan colores ENTONCES se DEBERÁ asegurar accesibilidad:

```dart
// Ejemplo de extensión de tema personalizada
@immutable
class CustomColors extends ThemeExtension<CustomColors> {
  const CustomColors({
    required this.success,
    required this.warning,
    required this.danger,
  });

  final Color? success;
  final Color? warning;
  final Color? danger;

  @override
  ThemeExtension<CustomColors> copyWith({
    Color? success,
    Color? warning,
    Color? danger,
  }) {
    return CustomColors(
      success: success ?? this.success,
      warning: warning ?? this.warning,
      danger: danger ?? this.danger,
    );
  }

  @override
  ThemeExtension<CustomColors> lerp(
    ThemeExtension<CustomColors>? other,
    double t,
  ) {
    if (other is! CustomColors) return this;
    return CustomColors(
      success: Color.lerp(success, other.success, t),
      warning: Color.lerp(warning, other.warning, t),
      danger: Color.lerp(danger, other.danger, t),
    );
  }
}

// Uso en ThemeData
theme: ThemeData(
  extensions: const <ThemeExtension<dynamic>>[
    CustomColors(
      success: Color(0xFF4CAF50), // Verde accesible
      warning: Color(0xFFFF9800), // Naranja accesible
      danger: Color(0xFFF44336),  // Rojo accesible
    ),
  ],
),
```

### 4.8. Layout Best Practices

#### 4.8.1. Prevención de Overflow

**REQ-FLT-058: Manejo de overflow obligatorio**

CUANDO se construyan layouts ENTONCES se DEBERÁ prevenir overflow:

```dart
// Uso correcto de Flexible y Expanded
Row(
  children: [
    const Icon(Icons.star),
    Expanded(
      child: Text(
        'Este texto se expandirá y truncará si es necesario',
        overflow: TextOverflow.ellipsis,
      ),
    ),
    const Icon(Icons.more_vert),
  ],
)

// Uso de Wrap para contenido que puede overflow
Wrap(
  spacing: 8.0,
  runSpacing: 4.0,
  children: tags.map((tag) => Chip(label: Text(tag))).toList(),
)

// SingleChildScrollView para contenido fijo grande
SingleChildScrollView(
  child: Column(
    children: [
      // Contenido que puede ser más grande que la pantalla
    ],
  ),
)
```

#### 4.8.2. Stack y Positioning

**REQ-FLT-059: Uso correcto de Stack**

CUANDO se use Stack ENTONCES se DEBERÁ posicionar correctamente:

```dart
// Ejemplo de Stack con Positioned
Stack(
  children: [
    Container(
      width: 200,
      height: 200,
      color: Colors.blue,
    ),
    Positioned(
      top: 10,
      right: 10,
      child: IconButton(
        icon: const Icon(Icons.close),
        onPressed: () {},
      ),
    ),
    const Align(
      alignment: Alignment.center,
      child: Text('Centrado'),
    ),
  ],
)
```

### 4.9. Accessibility Implementation

#### 4.9.1. Semantic Labels

**REQ-FLT-060: Labels semánticos obligatorios**

CUANDO se implementen widgets ENTONCES se DEBERÁN añadir labels semánticos:

```dart
// Ejemplo de Semantics widget
Semantics(
  label: 'Botón de favoritos',
  hint: 'Toca para añadir a favoritos',
  child: IconButton(
    icon: Icon(isFavorite ? Icons.favorite : Icons.favorite_border),
    onPressed: toggleFavorite,
  ),
)

// Ejemplo de imagen con semántica
Semantics(
  label: 'Foto de perfil del usuario',
  child: CircleAvatar(
    backgroundImage: NetworkImage(user.profileImageUrl),
  ),
)

// Exclusión de elementos decorativos
ExcludeSemantics(
  child: Container(
    decoration: const BoxDecoration(
      // Decoración puramente visual
    ),
  ),
)
```

#### 4.9.2. Contrast y Readability

**REQ-FLT-061: Contraste mínimo obligatorio**

CUANDO se definan colores ENTONCES se DEBERÁ asegurar contraste adecuado:

```dart
// Función helper para verificar contraste
double calculateContrastRatio(Color foreground, Color background) {
  final fgLuminance = foreground.computeLuminance();
  final bgLuminance = background.computeLuminance();

  final lighter = math.max(fgLuminance, bgLuminance);
  final darker = math.min(fgLuminance, bgLuminance);

  return (lighter + 0.05) / (darker + 0.05);
}

// Uso en validación de colores
bool isAccessibleContrast(Color foreground, Color background) {
  return calculateContrastRatio(foreground, background) >= 4.5;
}
```

### 4.10. Documentation Standards

#### 4.10.1. Dartdoc Comments

**REQ-FLT-062: Documentación dartdoc obligatoria**

CUANDO se documenten APIs ENTONCES se DEBERÁ usar formato dartdoc:

````dart
/// Manages user authentication and session state.
///
/// This class provides methods for logging in, logging out, and checking
/// authentication status. It integrates with Firebase Auth and maintains
/// local session state.
///
/// Example usage:
/// ```dart
/// final authService = AuthService();
/// final user = await authService.signIn(email, password);
/// if (user != null) {
///   print('Signed in as ${user.displayName}');
/// }
/// ```
class AuthService {
  /// Signs in a user with email and password.
  ///
  /// Returns the [User] object if successful, or `null` if authentication
  /// fails. Throws [AuthException] if there's a network error.
  ///
  /// The [email] must be a valid email address and [password] must be
  /// at least 6 characters long.
  Future<User?> signIn(String email, String password) async {
    // Implementation
  }

  /// The currently authenticated user, or `null` if not signed in.
  User? get currentUser => _currentUser;
}
````

#### 4.10.2. Code Comments

**REQ-FLT-063: Comentarios de código apropiados**

CUANDO se escriban comentarios ENTONCES se DEBERÁ explicar el "por qué", no el "qué":

```dart
// ❌ Mal: Comenta lo obvio
// Incrementa el contador
counter++;

// ✅ Bien: Explica el razonamiento
// Incrementamos el contador aquí porque el usuario completó
// una acción válida y necesitamos trackear el progreso
counter++;

// ✅ Bien: Explica lógica compleja
// Usamos un debounce de 300ms para evitar múltiples llamadas
// a la API mientras el usuario está escribiendo
Timer.periodic(const Duration(milliseconds: 300), (timer) {
  if (_searchQuery != _lastQuery) {
    _performSearch(_searchQuery);
    _lastQuery = _searchQuery;
  }
});
```

### 4.11. Proceso de Excepción y Revisión

#### 4.11.1. Excepciones a las Reglas

**REQ-FLT-064: Proceso de excepción documentado**

CUANDO se requiera una excepción a estas reglas ENTONCES se DEBERÁ:

1. Documentar justificación técnica detallada
2. Obtener aprobación del tech lead o arquitecto
3. Crear ADR (Architecture Decision Record)
4. Establecer plan de migración futura si aplica

#### 4.11.2. Revisión Periódica

**REQ-FLT-065: Revisión trimestral obligatoria**

CUANDO transcurran 3 meses ENTONCES se DEBERÁ revisar:

- Efectividad de las reglas implementadas
- Nuevas mejores prácticas de la comunidad Flutter
- Actualizaciones de dependencias y herramientas
- Feedback del equipo de desarrollo

## Reglas de Rendimiento

### Optimización de UI

**REQ-FLT-066: Constructor const obligatorio**

OBLIGATORIO usar constructor `const` siempre que sea posible

**REQ-FLT-067: ListView.builder para listas grandes**

OBLIGATORIO usar `ListView.builder` para listas grandes (>20 elementos)

**REQ-FLT-068: RepaintBoundary para widgets costosos**

OBLIGATORIO usar `RepaintBoundary` para widgets costosos

**REQ-FLT-069: Perfilado regular con DevTools**

OBLIGATORIO perfilar regularmente con Flutter DevTools

### Concurrencia y Asincronía

**REQ-FLT-070: No bloquear hilo principal**

PROHIBIDO bloquear el hilo principal de UI

**REQ-FLT-071: Isolates para tareas intensivas**

OBLIGATORIO usar `Isolates` o `compute()` para tareas intensivas

**REQ-FLT-072: Async/await consistente**

OBLIGATORIO usar `async`/`await` consistentemente

## Reglas de Seguridad

### Protección de Datos Sensibles

**REQ-FLT-073: No hardcodear claves**

PROHIBIDO hardcodear claves de API o tokens en el código

**REQ-FLT-074: Almacenamiento seguro**

OBLIGATORIO usar `flutter_secure_storage` para datos sensibles

**REQ-FLT-075: Validación de entradas**

OBLIGATORIO validar todas las entradas tanto en cliente como servidor

**REQ-FLT-076: HTTPS obligatorio**

OBLIGATORIO usar HTTPS para todas las comunicaciones de red

**REQ-FLT-077: Ofuscación en producción**

OBLIGATORIO ofuscar builds de producción

## Reglas de Testing y CI/CD

### Automatización de Calidad

**REQ-FLT-078: Pipeline con linter y tests**

OBLIGATORIO integrar linter y tests en pipeline CI/CD

**REQ-FLT-079: PRs deben pasar lint**

OBLIGATORIO que PRs fallen si violan reglas de lint

**REQ-FLT-080: Revisión de pares**

OBLIGATORIO revisión de pares (peer review) para todos los PRs

**REQ-FLT-081: Cobertura mínima de tests**

OBLIGATORIO mantener cobertura mínima de tests del 80%

### Control de Versiones

**REQ-FLT-082: Commits atómicos**

OBLIGATORIO commits atómicos y descriptivos

**REQ-FLT-083: Feature branches**

OBLIGATORIO usar feature branches, mantener main/master limpio

**REQ-FLT-084: Tags semánticos**

OBLIGATORIO etiquetar releases con tags semánticos

**REQ-FLT-085: Versionado semántico**

OBLIGATORIO seguir versionado semántico (SemVer)

## Reglas de Conectividad

### Manejo de Red

**REQ-FLT-086: Dio como cliente HTTP**

OBLIGATORIO usar `Dio` como cliente HTTP con interceptores

**REQ-FLT-087: Paginación para listas**

OBLIGATORIO implementar paginación para listas de datos

**REQ-FLT-088: Detección de conectividad**

OBLIGATORIO usar `connectivity_plus` para detectar cambios de red

**REQ-FLT-089: Estrategia offline-first**

OBLIGATORIO diseñar con estrategia "offline-first" usando SQLite

## Reglas de Despliegue

### Producción y Monitoreo

**REQ-FLT-090: Feature Flags**

OBLIGATORIO implementar Feature Flags con Firebase Remote Config

**REQ-FLT-091: Crashlytics y Analytics**

OBLIGATORIO usar Crashlytics y Firebase Analytics

**REQ-FLT-092: Dependencias actualizadas**

OBLIGATORIO mantener dependencias actualizadas mensualmente

**REQ-FLT-093: Documentación con Dart Doc**

OBLIGATORIO documentar APIs con Dart Doc

## Reglas de Integración MCP (Model Context Protocol)

### Configuración MCP Obligatoria

**REQ-FLT-094: Servidor MCP configurado**

OBLIGATORIO configurar el servidor MCP de Dart/Flutter en el entorno de desarrollo

**REQ-FLT-095: Versión SDK compatible**

OBLIGATORIO usar Dart SDK 3.9+ o Flutter 3.35+ para compatibilidad MCP

**REQ-FLT-096: Verificación de conexión MCP**

OBLIGATORIO verificar la conexión MCP antes de iniciar desarrollo

**REQ-FLT-097: Herramientas MCP para análisis**

RECOMENDADO usar herramientas MCP para análisis automático de código

### Uso de AI-Assisted Development

**REQ-FLT-098: MCP para detección de issues**

RECOMENDADO aprovechar MCP para detección automática de issues

**REQ-FLT-099: MCP para gestión de paquetes**

RECOMENDADO usar MCP para búsqueda y adición inteligente de paquetes

**REQ-FLT-100: MCP para refactoring**

RECOMENDADO usar MCP para refactoring siguiendo Clean Architecture

**REQ-FLT-101: Validación de código AI**

OBLIGATORIO validar código generado por AI antes de commit

## Reglas de Dart Best Practices

### Effective Dart Guidelines

**REQ-FLT-102: Guías oficiales Effective Dart**

OBLIGATORIO seguir las guías oficiales de Effective Dart

**REQ-FLT-103: Null safety consistente**

OBLIGATORIO usar null safety de forma consistente, evitar `!` innecesario

**REQ-FLT-104: Pattern matching apropiado**

OBLIGATORIO usar pattern matching donde simplifique el código

**REQ-FLT-105: Records para múltiples tipos**

OBLIGATORIO usar records para retornar múltiples tipos cuando sea apropiado

### Organización de Código Dart

**REQ-FLT-106: Clases relacionadas en mismo archivo**

OBLIGATORIO definir clases relacionadas en el mismo archivo de librería

**REQ-FLT-107: Librerías agrupadas por carpeta**

OBLIGATORIO agrupar librerías relacionadas en la misma carpeta

**REQ-FLT-108: Documentación de APIs públicas**

OBLIGATORIO documentar todas las APIs públicas con dartdoc

**REQ-FLT-109: Switch statements exhaustivos**

OBLIGATORIO usar switch statements exhaustivos sin break

### Manejo de Excepciones y Async

**REQ-FLT-110: Try-catch apropiado**

OBLIGATORIO usar try-catch para manejo de excepciones apropiadas

**REQ-FLT-111: Async/await consistente**

OBLIGATORIO usar async/await consistentemente para operaciones asíncronas

**REQ-FLT-112: Streams para eventos asíncronos**

OBLIGATORIO usar Streams para secuencias de eventos asíncronos

**REQ-FLT-113: Arrow syntax para funciones simples**

OBLIGATORIO usar arrow syntax para funciones simples de una línea

## Reglas de Flutter Best Practices

### Widget Development

**REQ-FLT-114: Widgets inmutables**

OBLIGATORIO usar widgets inmutables (especialmente StatelessWidget)

**REQ-FLT-115: Composición sobre herencia**

OBLIGATORIO preferir composición sobre herencia para widgets complejos

**REQ-FLT-116: Clases Widget privadas**

OBLIGATORIO usar clases Widget privadas pequeñas en lugar de métodos helper

**REQ-FLT-117: Dividir métodos build grandes**

OBLIGATORIO dividir métodos build() grandes en widgets reutilizables

### Performance Optimization

**REQ-FLT-118: ListView.builder para listas largas**

OBLIGATORIO usar ListView.builder para listas largas (lazy loading)

**REQ-FLT-119: Compute para cálculos costosos**

OBLIGATORIO usar compute() para cálculos costosos (evitar bloqueo UI)

**REQ-FLT-120: Constructores const**

OBLIGATORIO usar constructores const siempre que sea posible

**REQ-FLT-121: No operaciones costosas en build**

PROHIBIDO realizar operaciones costosas directamente en build()

## Reglas de Visual Design & Theming

### Material Design Implementation

**REQ-FLT-122: Material Design 3 o Cupertino**

OBLIGATORIO seguir Material Design 3 o Cupertino Design

**REQ-FLT-123: Soporte para temas claro y oscuro**

OBLIGATORIO implementar soporte para temas claro y oscuro

**REQ-FLT-124: ColorScheme.fromSeed**

OBLIGATORIO usar ColorScheme.fromSeed() para paletas armoniosas

**REQ-FLT-125: ThemeData centralizado**

OBLIGATORIO definir ThemeData centralizado para consistencia

### Typography and Colors

**REQ-FLT-126: Theme.of(context).textTheme**

OBLIGATORIO usar Theme.of(context).textTheme para estilos de texto

**REQ-FLT-127: Contraste mínimo 4.5:1**

OBLIGATORIO mantener contraste mínimo 4.5:1 para texto normal

**REQ-FLT-128: Google Fonts**

OBLIGATORIO usar google_fonts para fuentes personalizadas

**REQ-FLT-129: Regla 60-30-10 para colores**

OBLIGATORIO seguir regla 60-30-10 para esquemas de color

### Responsive Design

**REQ-FLT-130: LayoutBuilder o MediaQuery**

OBLIGATORIO usar LayoutBuilder o MediaQuery para UIs responsivas

**REQ-FLT-131: Optimización para diferentes pantallas**

OBLIGATORIO optimizar para diferentes tamaños de pantalla

**REQ-FLT-132: Flexible y Expanded apropiados**

OBLIGATORIO usar Flexible y Expanded apropiadamente en Row/Column

**REQ-FLT-133: Wrap para contenido overflow**

OBLIGATORIO usar Wrap para contenido que puede overflow

## Reglas de Layout Best Practices

### Overflow Prevention

**REQ-FLT-134: SingleChildScrollView para contenido grande**

OBLIGATORIO usar SingleChildScrollView para contenido fijo grande

**REQ-FLT-135: ListView/GridView.builder para listas dinámicas**

OBLIGATORIO usar ListView/GridView.builder para listas dinámicas

**REQ-FLT-136: FittedBox para escalar widgets**

OBLIGATORIO usar FittedBox para escalar widgets dentro de contenedores

**REQ-FLT-137: Stack con Positioned/Align**

OBLIGATORIO usar Stack con Positioned/Align para layering

### Advanced Layout

**REQ-FLT-138: OverlayPortal para elementos on top**

RECOMENDADO usar OverlayPortal para elementos UI "on top"

**REQ-FLT-139: RepaintBoundary para aislar widgets**

OBLIGATORIO usar RepaintBoundary para aislar widgets costosos

**REQ-FLT-140: Evitar nesting profundo**

OBLIGATORIO evitar nesting profundo de widgets

**REQ-FLT-141: Semantics para accesibilidad**

OBLIGATORIO usar Semantics para accesibilidad

## Reglas de Accessibility (A11Y)

### Accessibility Compliance

**REQ-FLT-142: Accesibilidad según WCAG 2.1**

OBLIGATORIO implementar accesibilidad según WCAG 2.1

**REQ-FLT-143: Contraste mínimo para texto**

OBLIGATORIO asegurar contraste mínimo 4.5:1 para texto

**REQ-FLT-144: Escalado dinámico de texto**

OBLIGATORIO soportar escalado dinámico de texto

**REQ-FLT-145: Widget Semantics para labels**

OBLIGATORIO usar widget Semantics para labels descriptivos

### Screen Reader Support

**REQ-FLT-146: Pruebas con TalkBack y VoiceOver**

OBLIGATORIO probar regularmente con TalkBack (Android) y VoiceOver (iOS)

**REQ-FLT-147: Labels semánticos claros**

OBLIGATORIO proporcionar labels semánticos claros

**REQ-FLT-148: Navegación por teclado**

OBLIGATORIO asegurar navegación por teclado funcional

**REQ-FLT-149: Hints y descriptions apropiados**

OBLIGATORIO implementar hints y descriptions apropiados

## Reglas de Documentation

### Code Documentation

**REQ-FLT-150: Comentarios dartdoc para APIs públicas**

OBLIGATORIO usar comentarios dartdoc (///) para APIs públicas

**REQ-FLT-151: Documentar clases y métodos**

OBLIGATORIO documentar clases, constructores, métodos y funciones top-level

**REQ-FLT-152: Documentación pensando en el usuario**

OBLIGATORIO escribir documentación pensando en el usuario

**REQ-FLT-153: No documentación redundante**

PROHIBIDO documentación redundante que solo restate el código

### Documentation Style

**REQ-FLT-154: Resumen de una oración**

OBLIGATORIO comenzar con resumen de una oración terminada en punto

**REQ-FLT-155: Separar resumen con línea en blanco**

OBLIGATORIO separar resumen con línea en blanco

**REQ-FLT-156: Backticks para código**

OBLIGATORIO usar backticks para código y especificar lenguaje

**REQ-FLT-157: Ejemplos de código apropiados**

OBLIGATORIO incluir ejemplos de código donde sea apropiado

### 4.12. Uso Efectivo del MCP de Dart/Flutter

#### 4.12.1. Casos de Uso Recomendados con MCP

**Análisis y Corrección Automática de Código:**

```
Prompt sugerido: "Check for and fix static and runtime analysis issues. Check for and fix any layout issues."
```

El MCP permite al AI assistant:

- Ejecutar `flutter analyze` automáticamente
- Identificar y corregir RenderFlex overflow errors
- Sugerir mejoras de rendimiento
- Aplicar fixes automáticos siguiendo Clean Architecture

**Búsqueda y Adición Inteligente de Paquetes:**

```
Prompt sugerido: "Find a suitable package to add a line chart that maps data over time following Clean Architecture patterns."
```

El MCP habilita al AI assistant para:

- Buscar paquetes apropiados en pub.dev
- Añadir dependencias al pubspec.yaml
- Generar código de implementación en las capas correctas
- Crear casos de uso y repositorios necesarios

**Refactoring Arquitectónico:**

```
Prompt sugerido: "Refactor this widget to follow Clean Architecture with proper separation of concerns."
```

El MCP permite:

- Analizar la estructura actual del código
- Identificar violaciones arquitectónicas
- Generar la estructura de capas correcta
- Mover código a las capas apropiadas

#### 4.12.2. Comandos MCP Disponibles

El servidor MCP de Dart/Flutter proporciona herramientas para:

- **Análisis de código**: Detección de issues estáticos y runtime
- **Gestión de dependencias**: Búsqueda, adición y actualización de paquetes
- **Navegación de proyecto**: Exploración inteligente de la estructura
- **Testing**: Ejecución y análisis de tests
- **Build y deployment**: Gestión de builds para diferentes plataformas
- **Debugging**: Asistencia en resolución de problemas

### 4.13. Ejemplo de Implementación Clean Architecture

#### 4.13.1. Estructura de Feature Completa

```dart
// features/user_profile/domain/entities/user.dart
class User extends Equatable {
  final String id;
  final String name;
  final String email;

  const User({required this.id, required this.name, required this.email});

  @override
  List<Object> get props => [id, name, email];
}

// features/user_profile/domain/repositories/i_user_repository.dart
abstract class IUserRepository {
  Future<Either<Failure, User>> getUserProfile(String userId);
  Future<Either<Failure, void>> updateUserProfile(User user);
}

// features/user_profile/domain/use_cases/get_user_profile_use_case.dart
class GetUserProfileUseCase {
  final IUserRepository repository;

  GetUserProfileUseCase(this.repository);

  Future<Either<Failure, User>> call(String userId) {
    return repository.getUserProfile(userId);
  }
}

// features/user_profile/data/models/user_model.dart
@freezed
class UserModel with _$UserModel {
  const factory UserModel({
    required String id,
    required String name,
    required String email,
  }) = _UserModel;

  factory UserModel.fromJson(Map<String, dynamic> json) =>
      _$UserModelFromJson(json);
}

extension UserModelX on UserModel {
  User toEntity() => User(id: id, name: name, email: email);
}

// features/user_profile/data/repositories/user_repository_impl.dart
@Injectable(as: IUserRepository)
class UserRepositoryImpl implements IUserRepository {
  final UserRemoteDataSource remoteDataSource;
  final UserLocalDataSource localDataSource;

  UserRepositoryImpl(this.remoteDataSource, this.localDataSource);

  @override
  Future<Either<Failure, User>> getUserProfile(String userId) async {
    try {
      final userModel = await remoteDataSource.getUserProfile(userId);
      await localDataSource.cacheUser(userModel);
      return Right(userModel.toEntity());
    } catch (e) {
      try {
        final cachedUser = await localDataSource.getCachedUser(userId);
        return Right(cachedUser.toEntity());
      } catch (e) {
        return Left(CacheFailure());
      }
    }
  }
}

// features/user_profile/presentation/bloc/user_profile_bloc.dart
class UserProfileBloc extends Bloc<UserProfileEvent, UserProfileState> {
  final GetUserProfileUseCase getUserProfileUseCase;

  UserProfileBloc(this.getUserProfileUseCase) : super(UserProfileInitial()) {
    on<GetUserProfile>(_onGetUserProfile);
  }

  Future<void> _onGetUserProfile(
    GetUserProfile event,
    Emitter<UserProfileState> emit,
  ) async {
    emit(UserProfileLoading());

    final result = await getUserProfileUseCase(event.userId);

    result.fold(
      (failure) => emit(UserProfileError(failure.message)),
      (user) => emit(UserProfileLoaded(user)),
    );
  }
}
```

### 4.14. Beneficios de la Implementación

#### 4.14.1. Escalabilidad

- **Modularidad**: Cada feature es independiente y puede desarrollarse por equipos separados
- **Reutilización**: Componentes de core pueden reutilizarse entre features
- **Crecimiento**: Nuevas features siguen el mismo patrón establecido

#### 4.14.2. Mantenibilidad

- **Separación clara**: Cada capa tiene responsabilidades bien definidas
- **Testing simplificado**: Cada componente puede probarse de forma aislada
- **Refactoring seguro**: Cambios en una capa no afectan otras

#### 4.14.3. Calidad

- **Código predecible**: Estructura consistente en todo el proyecto
- **Menos bugs**: Separación de responsabilidades reduce errores
- **Documentación implícita**: La arquitectura documenta la intención del código

#### 4.14.4. Productividad con AI-Assisted Development

- **Desarrollo acelerado**: MCP permite generar código siguiendo Clean Architecture automáticamente
- **Debugging inteligente**: AI assistant puede identificar y corregir issues complejos
- **Refactoring asistido**: Transformaciones arquitectónicas guiadas por AI
- **Aprendizaje continuo**: El AI assistant aprende los patrones del proyecto

---

_Esta especificación de requisitos es de cumplimiento obligatorio para garantizar aplicaciones Flutter de alta calidad, mantenibles y escalables siguiendo los principios de Clean Architecture._
