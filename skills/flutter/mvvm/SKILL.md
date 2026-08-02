---
name: flutter-mvvm-pattern
description: "Implements the MVVM (Model-View-ViewModel) pattern in Flutter using Provider and ChangeNotifier. Use when building medium-scale Flutter apps that need clear UI/logic separation, reactive state management with provider, changenotifier, or mvvm pattern."
---

# MVVM Pattern

El patrón MVVM proporciona separación clara entre lógica de negocio e interfaz de usuario, facilitando el testing, mantenimiento y escalabilidad.

**Importante:** Ejecutar comandos desde la raíz del proyecto (donde existe el directorio `mobile/`).

## Cuándo usar

- Proyectos medianos con lógica de negocio moderada
- Necesitas separación clara entre UI y lógica
- Quieres testear la lógica de presentación fácilmente
- Necesitas gestión de estado reactiva con Provider

## Cuándo NO usar

- Proyectos muy pequeños (usa `setState`)
- Aplicaciones enterprise complejas (considera Clean Architecture)

## Estructura del Proyecto

```
lib/
├── models/entities/     # Entidades de dominio (freezed)
├── views/screens/       # Widgets de UI
├── views/widgets/       # Widgets reutilizables
├── viewmodels/          # ViewModels con ChangeNotifier
├── services/api/        # Servicios HTTP
└── main.dart
```

## Componentes Principales

### Model — datos inmutables con freezed

```dart
// models/entities/user.dart
@freezed
class User with _$User {
  const factory User({
    required String id,
    required String name,
    required String email,
    String? avatar,
  }) = _User;

  factory User.fromJson(Map<String, dynamic> json) => _$UserFromJson(json);
}
```

### ViewModel — lógica de presentación

```dart
// viewmodels/user_viewmodel.dart
class UserViewModel extends ChangeNotifier {
  final UserService _userService;
  UserViewModel(this._userService);

  List<User> _users = [];
  List<User> get users => List.unmodifiable(_users);

  bool _isLoading = false;
  bool get isLoading => _isLoading;

  String? _error;
  String? get error => _error;

  Future<void> fetchUsers() async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      _users = await _userService.getUsers();
    } catch (e) {
      _error = 'Error al cargar usuarios: ${e.toString()}';
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  @override
  void dispose() {
    // Limpiar recursos si es necesario
    super.dispose();
  }
}
```

### View — UI reactiva con Consumer

```dart
// views/screens/user_list_screen.dart
class UserListScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Usuarios')),
      body: Consumer<UserViewModel>(
        builder: (context, vm, child) {
          if (vm.isLoading) return const Center(child: CircularProgressIndicator());
          if (vm.error != null) return Center(child: Text(vm.error!));
          return ListView.builder(
            itemCount: vm.users.length,
            itemBuilder: (_, i) => ListTile(
              title: Text(vm.users[i].name),
              subtitle: Text(vm.users[i].email),
            ),
          );
        },
      ),
    );
  }
}
```

## Dependencias

```yaml
dependencies:
  provider: ^6.1.1
  freezed_annotation: ^2.4.1
  json_annotation: ^4.8.1
  http: ^1.1.0

dev_dependencies:
  build_runner: ^2.4.6
  freezed: ^2.4.5
  json_serializable: ^6.7.1
  mockito: ^5.4.4
```

## Mejores Prácticas

- **Dependency Injection:** inyectar servicios via constructor del ViewModel
- **Selector sobre Consumer** cuando solo se necesita parte del estado:
  ```dart
  Selector<UserViewModel, bool>(
    selector: (_, vm) => vm.isLoading,
    builder: (_, isLoading, child) => isLoading ? CircularProgressIndicator() : child!,
    child: UserList(),
  )
  ```
- **Single Responsibility:** cada ViewModel maneja una pantalla/funcionalidad
- **Dispose resources:** cancelar streams y controllers en `dispose()`

## Testing del ViewModel

```dart
@GenerateMocks([UserService])
void main() {
  late UserViewModel viewModel;
  late MockUserService mockService;

  setUp(() {
    mockService = MockUserService();
    viewModel = UserViewModel(mockService);
  });

  tearDown(() => viewModel.dispose());

  test('fetchUsers actualiza la lista cuando es exitoso', () async {
    final users = [User(id: '1', name: 'John', email: 'john@test.com')];
    when(mockService.getUsers()).thenAnswer((_) async => users);

    await viewModel.fetchUsers();

    expect(viewModel.users, users);
    expect(viewModel.isLoading, false);
    expect(viewModel.error, null);
  });
}
```

## Flujo de Datos

```
User Interaction → View (Consumer) → ViewModel (notifyListeners) → Service → Model
```

## Recursos

- [Provider Documentation](https://pub.dev/packages/provider)
- [Freezed Package](https://pub.dev/packages/freezed)
