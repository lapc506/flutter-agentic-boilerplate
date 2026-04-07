---
name: flutter-clean-architecture
description: "Scaffolds Clean Architecture folder structure, generates BLoC classes, creates repository interfaces, and wires get_it dependency injection for Flutter apps. Use when building enterprise Flutter apps that need layered architecture with clean-architecture, bloc, usecase, repository-pattern, or ddd approach for maximum testability and maintainability."
---

# Clean Architecture

## Workflow para nueva feature

1. Crear entity en `domain/entities/` (extends Equatable)
2. Definir repository interface en `domain/repositories/`
3. Implementar use cases en `domain/usecases/`
4. Crear model en `data/models/` (extends entity, añade fromJson/toJson)
5. Implementar datasources en `data/datasources/`
6. Implementar repository en `data/repositories/`
7. Crear BLoC (event, state, bloc) en `presentation/bloc/`
8. Registrar todo en `injection_container.dart`
9. Verificar con tests unitarios por capa

## Estructura del Proyecto

```
lib/
├── core/
│   ├── error/
│   │   ├── exceptions.dart
│   │   └── failures.dart
│   ├── usecases/
│   │   └── usecase.dart
│   └── network/
│       └── network_info.dart
│
├── features/
│   └── [feature_name]/
│       ├── data/
│       │   ├── datasources/
│       │   │   ├── feature_remote_datasource.dart
│       │   │   └── feature_local_datasource.dart
│       │   ├── models/
│       │   │   └── feature_model.dart
│       │   └── repositories/
│       │       └── feature_repository_impl.dart
│       ├── domain/
│       │   ├── entities/
│       │   │   └── feature_entity.dart
│       │   ├── repositories/
│       │   │   └── feature_repository.dart
│       │   └── usecases/
│       │       └── get_feature.dart
│       └── presentation/
│           ├── bloc/
│           │   ├── feature_bloc.dart
│           │   ├── feature_event.dart
│           │   └── feature_state.dart
│           └── pages/
│               └── feature_page.dart
│
└── injection_container.dart
```

## Capas de la Arquitectura

### Domain Layer

La capa más interna, independiente del framework. Contiene la lógica de negocio pura.

```dart
// domain/entities/user_entity.dart
class UserEntity extends Equatable {
  final String id;
  final String name;
  final String email;

  const UserEntity({required this.id, required this.name, required this.email});

  @override
  List<Object?> get props => [id, name, email];
}

// domain/repositories/user_repository.dart
abstract class UserRepository {
  Future<Either<Failure, UserEntity>> getUser(String id);
  Future<Either<Failure, List<UserEntity>>> getUsers();
}

// core/usecases/usecase.dart
abstract class UseCase<Type, Params> {
  Future<Either<Failure, Type>> call(Params params);
}
class NoParams {}

// domain/usecases/get_user.dart
class GetUser implements UseCase<UserEntity, String> {
  final UserRepository repository;
  GetUser(this.repository);

  @override
  Future<Either<Failure, UserEntity>> call(String userId) =>
      repository.getUser(userId);
}
```

### Data Layer

Implementa las interfaces del dominio. Los modelos extienden entidades para serialización.

```dart
// data/models/user_model.dart
class UserModel extends UserEntity {
  const UserModel({required String id, required String name, required String email})
      : super(id: id, name: name, email: email);

  factory UserModel.fromJson(Map<String, dynamic> json) =>
      UserModel(id: json['id'], name: json['name'], email: json['email']);

  Map<String, dynamic> toJson() => {'id': id, 'name': name, 'email': email};
}

// data/repositories/user_repository_impl.dart
class UserRepositoryImpl implements UserRepository {
  final UserRemoteDataSource remoteDataSource;
  final UserLocalDataSource localDataSource;
  final NetworkInfo networkInfo;

  UserRepositoryImpl({
    required this.remoteDataSource,
    required this.localDataSource,
    required this.networkInfo,
  });

  @override
  Future<Either<Failure, UserEntity>> getUser(String id) async {
    if (await networkInfo.isConnected) {
      try {
        final user = await remoteDataSource.getUser(id);
        await localDataSource.cacheUser(user);
        return Right(user);
      } on ServerException {
        return Left(ServerFailure());
      }
    } else {
      try {
        return Right(await localDataSource.getCachedUser(id));
      } on CacheException {
        return Left(CacheFailure());
      }
    }
  }
}
```

### Presentation Layer (BLoC)

```dart
// presentation/bloc/user_event.dart
abstract class UserEvent extends Equatable {
  const UserEvent();
  @override List<Object?> get props => [];
}
class GetUsersEvent extends UserEvent {}
class GetUserEvent extends UserEvent {
  final String userId;
  const GetUserEvent(this.userId);
  @override List<Object> get props => [userId];
}

// presentation/bloc/user_state.dart
abstract class UserState extends Equatable {
  const UserState();
  @override List<Object?> get props => [];
}
class UserInitial extends UserState {}
class UserLoading extends UserState {}
class UsersLoaded extends UserState {
  final List<UserEntity> users;
  const UsersLoaded(this.users);
  @override List<Object> get props => [users];
}
class UserError extends UserState {
  final String message;
  const UserError(this.message);
  @override List<Object> get props => [message];
}

// presentation/bloc/user_bloc.dart
class UserBloc extends Bloc<UserEvent, UserState> {
  final GetUser getUser;
  final GetUsers getUsers;

  UserBloc({required this.getUser, required this.getUsers}) : super(UserInitial()) {
    on<GetUsersEvent>(_onGetUsers);
    on<GetUserEvent>(_onGetUser);
  }

  Future<void> _onGetUsers(GetUsersEvent event, Emitter<UserState> emit) async {
    emit(UserLoading());
    final result = await getUsers(NoParams());
    result.fold(
      (failure) => emit(UserError(_mapFailureToMessage(failure))),
      (users) => emit(UsersLoaded(users)),
    );
  }

  Future<void> _onGetUser(GetUserEvent event, Emitter<UserState> emit) async {
    emit(UserLoading());
    final result = await getUser(event.userId);
    result.fold(
      (failure) => emit(UserError(_mapFailureToMessage(failure))),
      (user) => emit(UserLoaded(user)),
    );
  }

  String _mapFailureToMessage(Failure failure) {
    switch (failure.runtimeType) {
      case ServerFailure: return 'Error del servidor.';
      case CacheFailure: return 'Error al cargar datos locales.';
      case NetworkFailure: return 'Sin conexión a internet.';
      default: return 'Error inesperado.';
    }
  }
}
```

## Dependency Injection (get_it)

```dart
// injection_container.dart
final sl = GetIt.instance;

Future<void> init() async {
  // BLoC
  sl.registerFactory(() => UserBloc(getUser: sl(), getUsers: sl()));

  // Use cases
  sl.registerLazySingleton(() => GetUser(sl()));
  sl.registerLazySingleton(() => GetUsers(sl()));

  // Repository
  sl.registerLazySingleton<UserRepository>(
    () => UserRepositoryImpl(
      remoteDataSource: sl(),
      localDataSource: sl(),
      networkInfo: sl(),
    ),
  );

  // Data sources
  sl.registerLazySingleton<UserRemoteDataSource>(
    () => UserRemoteDataSourceImpl(client: sl(), baseUrl: 'https://api.example.com'),
  );
  sl.registerLazySingleton<UserLocalDataSource>(
    () => UserLocalDataSourceImpl(sharedPreferences: sl()),
  );

  // Core
  sl.registerLazySingleton<NetworkInfo>(() => NetworkInfoImpl(sl()));

  // External
  final sharedPreferences = await SharedPreferences.getInstance();
  sl.registerLazySingleton(() => sharedPreferences);
  sl.registerLazySingleton(() => http.Client());
  sl.registerLazySingleton(() => InternetConnectionChecker());
}
```

## Dependencias

```yaml
dependencies:
  flutter_bloc: ^8.1.3
  get_it: ^7.6.4
  dartz: ^0.10.1
  equatable: ^2.0.5
  http: ^1.1.0
  shared_preferences: ^2.2.2
  internet_connection_checker: ^1.0.0+1

dev_dependencies:
  mockito: ^5.4.4
  bloc_test: ^9.1.5
```

## Verificación

- Dependencias unidireccionales: Presentation → Domain ← Data
- Capa Domain no importa Flutter, http, ni paquetes externos
- Cada feature es un módulo independiente con sus tres capas
- Repository impl maneja fallback local cuando no hay red
