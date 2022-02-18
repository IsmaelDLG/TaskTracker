# Documentación de la API
- [Documentación de la API](#documentación-de-la-api)
  - [Task](#task)
    - [Create Task](#create-task)
    - [Get Task](#get-task)
    - [Edit Task](#edit-task)
    - [Delete Task](#delete-task)
  - [Profile](#profile)
    - [Create Profile](#create-profile)
    - [Get Profile](#get-profile)
    - [Edit Profile](#edit-profile)
    - [Delete Profile](#delete-profile)

La url base de la api es `/api/v1/`. 
La respuesta a cualquier petición tendrá la siguiente estructura:

```json
{
    "code": 200 /*An http code*/,
    "message" : "Ok" /*A short description of the result of the operation*/,
    "data" : {} /*An object filled with the data returned*/
}
```

Para simplificar, a partir de aqui se obviara la parte exterior de la respuesta y solo se especificará el campo `data` en los ejemplos.

A continuación, se describen los endpoints de la API:

## Task

### Create Task

**Endpoint:**

`POST /api/v1/task/` 

**Parámetros de la URL:**

Ninguno

**Parámetros del cuerpo:**

| Parámetro  | Opcional | Tipo         | Descripción                      |
|------------|----------|--------------|----------------------------------|
| profile    | No       | integer      | Perfil al que pertenece la tarea |
| start_time | No       | integer      | Timestamp de inicio de la tarea  |
| end_time   | Sí       | integer      | Timestamp de fin de la tarea     |
| tags       | Sí       | list(string) | Lista de tags de la tarea        |
| notes      | Sí       | string       | Notas de la tarea                |

**Respuesta:**

| Parámetro  | Tipo         | Descripción                      |
|------------|--------------|----------------------------------|
| id         | integer      | Identificador de la tarea creada |

**Códigos de respuesta:**

| Código | Descripción                                          |
|--------|------------------------------------------------------|
| 200    | Tarea creada                                         |
| 400    | Error en el parámetro {parámetro}. Motivo: {motivo}  |

**Ejemplo de petición:**

`POST /api/v1/task/` 

```json
{
    "profile": 1,
    "start_time" : 0,
    "end_time" : 1,
    "tags": [
        "work",
        "dev"
    ],
    "notes": "A very cool note for this task"
}
```
**Ejemplo de respuesta:**

```json
{
    "id": 1
}
```

### Get Task

**Endpoint:**

`GET /api/v1/task/{id}` 

**Parámetros de la URL:**

| Parámetro  | Opcional | Tipo         | Descripción                      |
|------------|----------|--------------|----------------------------------|
| id         | No       | integer      | Id de la tarea                   |

**Parámetros del cuerpo:**

Ninguno

**Respuesta:**

| Parámetro  | Tipo         | Descripción                      |
|------------|--------------|----------------------------------|
| id         | integer      | Identificador de la tarea        |
| profile    | integer      | Perfil al que pertenece la tarea |
| start_time | integer      | Timestamp de inicio de la tarea  |
| end_time   | integer      | Timestamp de fin de la tarea     |
| tags       | list(string) | Lista de tags de la tarea        |
| notes      | string       | Notas de la tarea                |

**Códigos de respuesta:**

| Código | Descripción                                          |
|--------|------------------------------------------------------|
| 200    | Tarea creada                                         |
| 404    | Tarea no encontrada                                  |

**Ejemplo de petición:**

`GET /api/v1/task/1` 

**Ejemplo de respuesta:**

```json
{
    "id": 1,
    "profile": 1,
    "start_time" : 0,
    "end_time" : 1,
    "tags": [
        "work",
        "dev"
    ],
    "notes": "A very cool note for this task"
}
```

### Edit Task

**Endpoint:**

`PUT /api/v1/task/{id}` 

**Parámetros de la URL:**

| Parámetro  | Opcional | Tipo         | Descripción                      |
|------------|----------|--------------|----------------------------------|
| id         | No       | integer      | ID de la tarea a actualizar      |

**Parámetros del cuerpo:**

| Parámetro  | Opcional | Tipo         | Descripción                      |
|------------|----------|--------------|----------------------------------|
| profile    | Sí       | integer      | Perfil al que pertenece la tarea |
| start_time | Sí       | integer      | Timestamp de inicio de la tarea  |
| end_time   | Sí       | integer      | Timestamp de fin de la tarea     |
| tags       | Sí       | list(string) | Lista de tags de la tarea        |
| notes      | Sí       | string       | Notas de la tarea                |

**Respuesta:**

| Parámetro  | Tipo         | Descripción                           |
|------------|--------------|---------------------------------------|
| id         | integer      | Identificador de la tarea actualizada |

**Códigos de respuesta:**

| Código | Descripción                                          |
|--------|------------------------------------------------------|
| 200    | Tarea actualizada                                    |
| 400    | Error en el parámetro {parámetro}. Motivo: {motivo}  |
| 404    | La Tarea {id} no existe                              |

**Ejemplo de petición:**

`PUT /api/v1/task/1` 

```json
{
    "notes": "A not so cool note for this task"
}
```
**Ejemplo de respuesta:**

```json
{
    "id": 1
}
```

### Delete Task

**Endpoint:**

`DELETE /api/v1/task/{id}` 

**Parámetros de la URL:**

| Parámetro  | Opcional | Tipo         | Descripción                      |
|------------|----------|--------------|----------------------------------|
| id         | No       | integer      | ID de la tarea a actualizar      |

**Parámetros del cuerpo:**

| Parámetro  | Opcional | Tipo         | Descripción                      |
|------------|----------|--------------|----------------------------------|


**Respuesta:**

| Parámetro  | Tipo         | Descripción                      |
|------------|--------------|----------------------------------|
| id         | integer      | Identificador de la tarea        |
| profile    | integer      | Perfil al que pertenece la tarea |
| start_time | integer      | Timestamp de inicio de la tarea  |
| end_time   | integer      | Timestamp de fin de la tarea     |
| tags       | list(string) | Lista de tags de la tarea        |
| notes      | string       | Notas de la tarea                |

**Códigos de respuesta:**

| Código | Descripción                                          |
|--------|------------------------------------------------------|
| 200    | Tarea actualizada                                    |
| 400    | Error en el parámetro {parámetro}. Motivo: {motivo}  |
| 404    | La Tarea {id} no existe                              |

**Ejemplo de petición:**

`DELETE /api/v1/task/1` 

**Ejemplo de respuesta:**

```json
{
    "id": 1,
    "profile": 1,
    "start_time" : 0,
    "end_time" : 1,
    "tags": [
        "work",
        "dev"
    ],
    "notes": "A not so cool note for this task"
}
```
## Profile

### Create Profile

**Endpoint:**

`POST /api/v1/profile/` 

**Parámetros de la URL:**

Ninguno

**Parámetros del cuerpo:**

| Parámetro  | Opcional | Tipo         | Descripción                            |
|------------|----------|--------------|----------------------------------------|
| name       | No       | integer      | Nombre del perfil                      |
| tags       | Sí       | list(string) | Lista de tags que pertenecen al perfil |

**Respuesta:**

| Parámetro  | Tipo         | Descripción                      |
|------------|--------------|----------------------------------|
| id         | integer      | Identificador del perfil creado  |

**Códigos de respuesta:**

| Código | Descripción                                          |
|--------|------------------------------------------------------|
| 200    | Perfil creada                                        |
| 400    | Error en el parámetro {parámetro}. Motivo: {motivo}  |

**Ejemplo de petición:**

`POST /api/v1/profile/` 

```json
{
    "name": "Profile_one",
    "tags": [
        "work",
        "dev"
    ]
}
```
**Ejemplo de respuesta:**

```json
{
    "id": 1
}
```

### Get Profile

**Endpoint:**

`GET /api/v1/profile/{id}` 

**Parámetros de la URL:**

| Parámetro  | Opcional | Tipo         | Descripción                      |
|------------|----------|--------------|----------------------------------|
| id         | No       | integer      | Id del perfil                    |

**Parámetros del cuerpo:**

Ninguno

**Respuesta:**

| Parámetro  | Tipo         | Descripción                      |
|------------|--------------|----------------------------------|
| id         | integer      | Identificador del perfil         |
| name       | integer      | Nombre del perfil                |
| tags       | list(string) | Lista de tags del perfil         |

**Códigos de respuesta:**

| Código | Descripción                                          |
|--------|------------------------------------------------------|
| 200    | Ok                                                   |
| 404    | Perfil no encontrada                                 |

**Ejemplo de petición:**

`GET /api/v1/profile/1` 

**Ejemplo de respuesta:**

```json
{
    "id": 1,
    "profile": 1,
    "start_time" : 0,
    "end_time" : 1,
    "tags": [
        "work",
        "dev"
    ],
    "notes": "A very cool note for this task"
}
```

### Edit Profile

**Endpoint:**

`PUT /api/v1/profile/{id}` 

**Parámetros de la URL:**

| Parámetro  | Opcional | Tipo         | Descripción                      |
|------------|----------|--------------|----------------------------------|
| id         | No       | integer      | ID del perfil a actualizar       |

**Parámetros del cuerpo:**

| Parámetro  | Opcional | Tipo         | Descripción                            |
|------------|----------|--------------|----------------------------------------|
| name       | Sí       | integer      | Nombre del perfil                      |
| tags       | Sí       | list(string) | Lista de tags que pertenecen al perfil |

**Respuesta:**

| Parámetro  | Tipo         | Descripción                           |
|------------|--------------|---------------------------------------|
| id         | integer      | Identificador del perfil actualizado  |

**Códigos de respuesta:**

| Código | Descripción                                          |
|--------|------------------------------------------------------|
| 200    | Perfil actualizado                                   |
| 400    | Error en el parámetro {parámetro}. Motivo: {motivo}  |
| 404    | El perfil {id} no existe                             |

**Ejemplo de petición:**

`PUT /api/v1/profile/1` 

```json
{
    "name": "Profile_two"
}
```
**Ejemplo de respuesta:**

```json
{
    "id": 1
}
```

### Delete Profile

**Endpoint:**

`DELETE /api/v1/profile/{id}` 

**Parámetros de la URL:**

| Parámetro  | Opcional | Tipo         | Descripción                      |
|------------|----------|--------------|----------------------------------|
| id         | No       | integer      | ID del perfil a borrar           |

**Parámetros del cuerpo:**

Ninguno

**Respuesta:**

| Parámetro  | Tipo         | Descripción                      |
|------------|--------------|----------------------------------|
| id         | integer      | Identificador de la tarea        |
| profile    | integer      | Perfil al que pertenece la tarea |
| start_time | integer      | Timestamp de inicio de la tarea  |
| end_time   | integer      | Timestamp de fin de la tarea     |
| tags       | list(string) | Lista de tags de la tarea        |
| notes      | string       | Notas de la tarea                |

**Códigos de respuesta:**

| Código | Descripción                                          |
|--------|------------------------------------------------------|
| 200    | Tarea actualizada                                    |
| 400    | Error en el parámetro {parámetro}. Motivo: {motivo}  |
| 404    | La Tarea {id} no existe                              |

**Ejemplo de petición:**

`DELETE /api/v1/task/1` 

**Ejemplo de respuesta:**

```json
{
    "id": 1,
    "start_time" : 0,
    "end_time" : 1,
    "tags": [
        "work",
        "dev"
    ],
    "notes": "A not so cool note for this task"
}
```