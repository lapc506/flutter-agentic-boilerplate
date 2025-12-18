# Flutter Agentic Boilerplate

Plantilla de inicio para aplicaciones Flutter listas para producción con backend REST.

El objetivo principal de esta plantilla es que puedas comenzar a trabajar rápidamente en tu próximo proyecto Flutter listo para producción sin toda la molestia de la configuración inicial del proyecto.

## ¿Qué es esto?

Esta es una plantilla de boilerplate simple para crear una aplicación Flutter lista para producción con generación de iconos/splash screen, boilerplate REST, y reportes (analytics, performance y crash reporting) todo configurado para ti.

**Además, este proyecto incluye un sistema de Agent Skills** que proporciona conocimiento contextual y capacidades especializadas a los asistentes de IA. Los skills agénticos cubren desde patrones arquitectónicos (MVVM, Clean Architecture) hasta integraciones avanzadas (Firebase, GraphQL, CI/CD) y pueden invocarse automáticamente o explícitamente durante el desarrollo.

Puedes usar este boilerplate como base y aprovechar los skills agénticos para guiar la implementación de features específicas, arquitecturas complejas o integraciones con servicios externos. Los skills se cargan progresivamente solo cuando se necesitan, manteniendo la eficiencia y reduciendo la carga cognitiva.

## ¿Qué NO es esto?

Dado que todos tienen opiniones muy fuertes sobre State Management y Arquitectura de Apps, esta plantilla no toma ninguna postura sobre estos temas por defecto.

Por lo tanto, esto NO es tu plantilla de state management y arquitectura de app pre-configurada. Sin embargo, **los skills agénticos sí incluyen guías detalladas** para implementar diferentes patrones arquitectónicos (MVVM, Clean Architecture, Feature-First, Modular) y sistemas de gestión de estado (BLoC, Riverpod, Provider), permitiéndote elegir e implementar el enfoque que prefieras con la ayuda de los agentes de IA.

O haz fork del repo, personaliza la plantilla a tu gusto y hazla tuya.

Dicho esto, los skills agénticos están diseñados para evolucionar y pueden combinarse según tus necesidades específicas.

## Estructura del Proyecto

Este proyecto está organizado como un monorepo con la siguiente estructura:

```
proyecto/
├── backend/          # Backend REST API
│   └── ...
├── mobile/           # Aplicación Flutter (raíz del proyecto Flutter)
│   ├── android/
│   ├── ios/
│   ├── lib/
│   ├── test/
│   └── pubspec.yaml
└── README.md
```

## Comenzando

### Prerrequisitos

- Flutter SDK instalado (versión estable recomendada)
- Dart SDK (incluido con Flutter)
- Android Studio / Xcode para desarrollo móvil
- Git

### Inicialización Rápida

#### Windows (PowerShell)

```powershell
.\scripts\setup.ps1
```

#### Linux/macOS (Bash)

```bash
chmod +x scripts/setup.sh
./scripts/setup.sh
```

Los scripts de setup realizarán automáticamente:
1. Creación de la estructura del monorepo
2. Inicialización del proyecto Flutter en `mobile/`
3. Instalación de dependencias
4. Configuración básica del proyecto

### Configuración Manual

Si prefieres configurar el proyecto manualmente:

1. **Obtener la plantilla**
   - Clona este repositorio a tu máquina local
   - O usa el botón "Use this template" en GitHub

2. **Instalar dependencias**
   ```bash
   cd mobile
   flutter pub get
   ```

3. **Nombre del Bundle de la Aplicación**
   Para cambiar el nombre del paquete/bundle identifier en los manifiestos de Android e iOS, ejecuta:
   ```bash
   flutter pub run change_app_package_name:main <com.nuevo.paquete.nombre>
   ```
   - Este paso usa `change_app_package_name`, dale un poco de amor al paquete.

4. **Nombre de la Aplicación**
   A continuación, necesitarás cambiar la etiqueta legible de tu app - el `CFBundleName` y/o `CFBundleDisplayName` dentro del `Info.plist` (para iOS) y el campo `android:label` en el nodo de aplicación en `AndroidManifest.xml` (para Android).
   
   Lamentablemente, este paso es manual; sería genial si `change_app_package_name` pudiera hacer esto por ti.
   
   **NOTA**: También necesitarás cambiar el `name` y `description` del paquete dentro de `pubspec.yaml`

5. **Iconos de la App**
   Luego generaremos automáticamente los iconos del launcher de tu app usando el paquete `flutter_launcher_icons`.
   - Copia la imagen que quieres usar como iconos del launcher a `mobile/assets/icon/icon.png`.
   - Ahora ejecuta `flutter pub run flutter_launcher_icons`. Este comando generará automáticamente los iconos del launcher de Android e iOS desde el archivo PNG para los diferentes DPIs y los colocará en sus respectivos directorios de recursos.
   
   **NOTA**: Consulta la documentación del paquete para más opciones de configuración sobre la generación de iconos del launcher actualizando tu `pubspec.yaml` en consecuencia. Por ejemplo, puedes querer diferentes iconos para diferentes plataformas ya que Android te permite usar un icono transparente e iOS no. Sin embargo, la configuración predeterminada incluida en esta plantilla será suficiente en la mayoría de los casos.

6. **Splash Screen**
   Luego generaremos splash screens nativos para ambas plataformas que tu app mostrará antes de que la carga se complete, y para esto usaremos `flutter_native_splash`.
   - Copia la imagen que quieres que se muestre en el centro de tu splash screen a `mobile/assets/splash/splash.png`.
   - Para cambiar el color de fondo de tu splash screen, ve a tu `pubspec.yaml` bajo `flutter_native_splash -> color` y pon tu código de color preferido. El predeterminado es blanco.
   - Finalmente, ejecuta `flutter pub run flutter_native_splash:create` para generar tus recursos desde la imagen del splash y actualizar tus archivos de manifiesto.

7. **Variables de Entorno**
   Haremos uso del paquete `envied` para cargar la configuración de la app desde archivos `.env`. Esto nos permitirá cambiar fácilmente entre diferentes configuraciones de app cuando ejecutemos la app bajo diferentes entornos como producción, staging o modos de debug.
   
   Todos los archivos `.env` pueden colocarse en el directorio raíz de tu proyecto. Para configurar un nuevo entorno, crea un nuevo archivo con extensión `.env` (ej. `.env` o `debug.env` o `staging.env`), luego copia el contenido de `.env-sample` y complétalo según sea necesario.
   
   El archivo `mobile/lib/env.dart` importa las variables de entorno a la app. Consulta la documentación para entender cómo usar el paquete `envied`.
   
   Para ofuscar y ocultar variables ENV sensibles usa el atributo `obfuscate` así: `@EnviedField(obfuscate: true)`.
   
   **NOTA:** Todos los archivos `.env` (y el archivo `env.g.dart` de `envied`) están `.gitignored` por defecto ya que pueden contener información sensible como rutas, claves, etc. Para especificar nuevas claves de env agrégalas al archivo `.env-sample`, que será copiado por otros desarrolladores y se proporcionará la configuración correspondiente.

8. **Firebase Reporting**
   En este paso, vamos a integrar diferentes herramientas de reporte de Firebase en tu app, incluyendo Firebase Analytics, Firebase Performance y Crashlytics.
   - Crea tu proyecto de Firebase en la Firebase Console
   - Descarga tu `GoogleService-Info.plist` y `google-services.json` y colócalos en sus carpetas correspondientes para iOS y Android. He `.gitignore'd` estos archivos para que no los tengas, por casualidad, en tu VCS por error.
   - Bueno, eso es todo. ¡Ya terminaste! No se necesita más configuración; ya lo he hecho por ti.
   
   **NOTAS:**
   - Todos los servicios de Firebase que estamos usando en este proyecto son gratuitos - al menos al momento de escribir esto - por lo que no generarán ningún cargo.
   - Con este paso, también habremos integrado Firebase Performance Monitoring en tu Cliente HTTP usando `dio_firebase_performance` que es un Interceptor de Dio que medirá el rendimiento de todas tus llamadas HTTP y reportará las estadísticas a Firebase.

9. **TODOs**
   Localiza cualquier `TODO` dentro de la carpeta `mobile/lib` y resuélvelos.

10. **¡A trabajar!**

Ahora ve a trabajar en tu app. ¡Feliz hacking!

## Despliegue

Antes de lanzar tu app de Android, asegúrate de firmarla:

1. Genera un archivo Keystore si aún no tienes uno. Si tienes uno, ignora este paso y ve al siguiente.
2. Ve a `mobile/android/key.properties` e incluye la ruta de tu Keystore, alias y contraseña.

## Paquetes Utilizados

* `change_app_package_name` - Cambia el nombre del paquete de la app con un solo comando. Hace el proceso muy fácil y rápido.
* `dio` - El mejor Cliente HTTP para Flutter en mi opinión. Interceptores reutilizables, ¿verdad?
* `dio_http_cache` - Interceptor de Dio para cachear requests. Intercepta requests para responder con datos cacheados o intercepta nuevas respuestas remotas para ser cacheadas. Muy configurable.
* `dio_log` - Es un Interceptor de Dio que presenta tus logs de request y response dentro de la UI de tu app
* `envied` - Carga configuración desde un archivo `.env`.
* `firebase_analytics` - Plugin de Flutter para Google Analytics for Firebase, una solución de medición de apps que proporciona información sobre el uso de la app y el compromiso del usuario en Android e iOS.
* `firebase_crashlytics` - Plugin de Flutter para Firebase Crashlytics. Reporta errores no capturados a la consola de Firebase.
* `firebase_performance` - Plugin de Flutter para Google Performance Monitoring for Firebase, una solución de medición que monitorea trazas y requests de red HTTP/S en Android e iOS.
* `firebase_performance_dio` - Implementación del Interceptor de Dio que envía datos de métricas de requests HTTP a Firebase.
* `flutter_launcher_icons` - Una herramienta de línea de comandos que simplifica la tarea de actualizar el icono del launcher de tu app Flutter.
* `flutter_native_splash` - Genera automáticamente código nativo para agregar splash screens en Android e iOS. Personaliza con una plataforma específica, color de fondo e imagen de splash.
* `freezed` - Generador de código simple pero poderoso para clases inmutables con todas las cosas buenas como unions/pattern-matching/copy etc. Hecho por Remi Rousselet, el creador y mantenedor de Provider. Puede trabajar con `json_serializable` para todas tus necesidades de `fromJson()` y `toJson()`.
* `go_router` - Este paquete se construye sobre la API de Router del framework de Flutter y proporciona APIs convenientes basadas en URL para navegar entre diferentes pantallas.
* `screenshots` - Screenshots es una utilidad de línea de comandos independiente y paquete para capturar imágenes de screenshot para Flutter.
* `pretty_dio_logger` - Interceptor de Dio que imprime de manera bonita a la consola los requests y responses HTTP que pasan por Dio

## Skills Agénticos Disponibles

Este proyecto incluye un sistema de **Agent Skills** que proporciona conocimiento contextual y capacidades especializadas a los asistentes de IA. Los skills se invocan automáticamente basándose en keywords en tus prompts o explícitamente usando la sintaxis `@skill:`.

Para más detalles sobre cada skill, consulta [AGENTS.md](AGENTS.md).

### 🎨 Flutter Skills (28)

1. MVVM
2. Clean Architecture
3. Project Setup
4. Testing Strategy
5. BLoC Avanzado
6. Riverpod
7. Feature-First Architecture
8. Arquitectura Modular
9. Code Generation
10. Performance Optimization
11. Accessibility (a11y)
12. Animation & Motion Design
13. Theming Avanzado
14. Internacionalización (i18n)
15. Firebase Integration
16. GraphQL Integration
17. Offline-First Architecture
18. Deep Linking & Universal Links
19. Push Notifications
20. Analytics & Tracking
21. Error Tracking & Crash Reporting
22. Feature Flags & Remote Config
23. In-App Purchases (IAP)
24. App Distribution & Deployment
25. Platform Channels & Native Integration
26. Native Integration (Swift/Kotlin)
27. WebView Integration
28. Security Best Practices

### 🚀 CI/CD Skills (9)

1. GitHub Actions
2. ArgoCD
3. Terraform
4. AWS
5. Google Cloud Platform (GCP)
6. Microsoft Azure
7. OVHCloud
8. Ansible AWX
9. Crossplane

### 🎨 Design Integration Skills (1)

1. Figma Dev Mode

### 🔍 Static Analysis Skills (1)

1. Static Analysis

## Estructura del Monorepo

```
proyecto/
├── backend/              # Backend REST API
│   ├── src/
│   ├── tests/
│   └── package.json
├── mobile/               # Aplicación Flutter
│   ├── android/
│   ├── ios/
│   ├── lib/
│   │   ├── core/
│   │   ├── features/
│   │   ├── shared/
│   │   └── main.dart
│   ├── test/
│   ├── assets/
│   │   ├── icon/
│   │   └── splash/
│   ├── pubspec.yaml
│   └── .env-sample
├── scripts/              # Scripts de utilidad
│   ├── setup.sh
│   └── setup.ps1
└── README.md
```

## Desarrollo

### Ejecutar la App

```bash
cd mobile
flutter run
```

### Ejecutar Tests

```bash
cd mobile
flutter test
```

### Generar Builds

```bash
# Android
cd mobile
flutter build apk --release

# iOS
cd mobile
flutter build ios --release
```

## Contribuir

Las contribuciones son bienvenidas. Por favor:

1. Haz fork del proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## Soporte

Si encuentras algún problema o tienes preguntas, por favor abre un issue en el repositorio.

---

**¡Feliz desarrollo!** 🚀

