# Guía de Contribución

¡Gracias por tu interés en contribuir al proyecto Flutter Agent Skills! 🎉

## 🤝 Cómo Contribuir

### Agregar un Nuevo Skill

Si deseas agregar un nuevo skill arquitectónico o patrón a `AGENTS.md`, sigue esta estructura:

```markdown
### Skill [N]: [Nombre del Skill]

**ID:** `flutter-[identificador]`
**Nivel:** [Básico/Intermedio/Avanzado]
**Referencia:** [URL opcional]

#### Descripción

[Explicación breve del skill y cuándo usarlo]

#### Estructura del Proyecto

[Árbol de directorios]

#### Componentes Principales

[Descripción de los componentes clave con ejemplos de código]

#### Dependencias Recomendadas

[Bloque YAML con dependencias]

#### Flujo de Datos

[Diagrama o descripción del flujo]

#### Testing

[Ejemplos de tests]

#### Mejores Prácticas

[Lista de mejores prácticas]
```

### Tipos de Contribuciones Bienvenidas

1. **Nuevos Skills Arquitectónicos**
   - State Management patterns (Redux, MobX, GetX)
   - Feature-first architecture
   - Modular architecture
   - Micro-frontends

2. **Mejoras a Skills Existentes**
   - Ejemplos de código adicionales
   - Casos de uso específicos
   - Optimizaciones

3. **Documentación**
   - Traducciones
   - Tutoriales paso a paso
   - Videos explicativos

4. **Ejemplos Prácticos**
   - Proyectos de ejemplo completos
   - Mini-apps demostrativas

## 📝 Proceso de Contribución

1. **Fork el Repositorio**
   ```bash
   git clone https://github.com/tu-usuario/flutter-agent-skills.git
   cd flutter-agent-skills
   ```

2. **Crea una Rama**
   ```bash
   git checkout -b feature/nombre-del-skill
   ```

3. **Realiza tus Cambios**
   - Edita `AGENTS.md` para agregar tu skill
   - Asegúrate de incluir ejemplos de código funcionales
   - Agrega referencias y recursos útiles

4. **Verifica tu Contribución**
   - [ ] Los ejemplos de código son correctos
   - [ ] La documentación es clara y concisa
   - [ ] Incluiste dependencias necesarias
   - [ ] Agregaste ejemplos de testing
   - [ ] Documentaste mejores prácticas

5. **Commit y Push**
   ```bash
   git add .
   git commit -m "feat: agrega skill para [nombre]"
   git push origin feature/nombre-del-skill
   ```

6. **Abre un Pull Request**
   - Describe claramente qué agrega tu contribución
   - Menciona cualquier issue relacionado
   - Espera feedback y realiza ajustes si es necesario

## 🎨 Estilo de Código

### Para Ejemplos Dart/Flutter

- Sigue las [Effective Dart guidelines](https://dart.dev/guides/language/effective-dart)
- Usa `dart format` antes de commitear
- Incluye comentarios explicativos en código complejo

### Para Documentación

- Usa Markdown estándar
- Mantén líneas de máximo 100 caracteres cuando sea posible
- Usa bloques de código con sintaxis highlighting:
  ````markdown
  ```dart
  // Tu código aquí
  ```
  ````

## ✅ Checklist para Pull Requests

Antes de enviar tu PR, asegúrate de:

- [ ] Tu código sigue el estilo del proyecto
- [ ] Has actualizado la documentación necesaria
- [ ] Has agregado tests si aplica
- [ ] Todos los tests existentes pasan
- [ ] Has actualizado el CHANGELOG.md si aplica
- [ ] Tu commit message es descriptivo

## 🐛 Reportar Bugs

Si encuentras un error:

1. Verifica que no exista un issue similar
2. Crea un nuevo issue con:
   - Descripción clara del problema
   - Pasos para reproducirlo
   - Comportamiento esperado vs actual
   - Screenshots si aplica
   - Versión de Flutter/Dart

## 💡 Sugerir Mejoras

Para sugerencias de nuevas características:

1. Abre un issue con la etiqueta "enhancement"
2. Describe claramente la mejora propuesta
3. Explica el caso de uso y beneficios
4. Si es posible, sugiere una implementación

## 📚 Recursos para Contribuidores

- [Flutter Documentation](https://docs.flutter.dev)
- [Dart Language Tour](https://dart.dev/guides/language/language-tour)
- [Effective Dart](https://dart.dev/guides/language/effective-dart)
- [Flutter Architecture Samples](https://github.com/brianegan/flutter_architecture_samples)

## 🌟 Reconocimiento

Todos los contribuidores serán agregados a la lista de reconocimientos en el README.

## 📧 Contacto

Si tienes preguntas sobre cómo contribuir, abre un issue con la etiqueta "question".

---

¡Gracias por hacer de Flutter Agent Skills un mejor recurso para la comunidad! 🚀
