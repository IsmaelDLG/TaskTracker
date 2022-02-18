# Documentación del proyecto
En este documento encontrarás una descripción general del proyecto.
- [Documentación del proyecto](#documentación-del-proyecto)
  - [Premisas](#premisas)
  - [Funcionalidades](#funcionalidades)
    - [Tareas](#tareas)
    - [Tareas en curso](#tareas-en-curso)
    - [Perfiles](#perfiles)
    - [Exportar y copias de seguridad](#exportar-y-copias-de-seguridad)
    - [Datos](#datos)
  - [Estructura](#estructura)
    - [La interfaz de usuario](#la-interfaz-de-usuario)
    - [Dominio](#dominio)
    - [Persistencia](#persistencia)

## Premisas

1. Una tarea esta compuesta de:
   - Identificador
   - Fecha de creacion
   - Fecha de inicio
   - Fecha de fin
   - Tiempo de pausa
   - Tags
   - Notas

2. Un perfil esta compuesto de:
    - Un nombre
    - Unos tags
    - Unas tareas asociadas

## Funcionalidades

### Tareas
- Se pueden crear tareas proporcionando todos los datos que las componen.
- Se pueden editar tareas existentes.
- Se pueden borrar tareas existentes.
### Tareas en curso
- Se pueden iniciar tareas "en curso", es decir, usando la fecha actual como fecha de inicio.
- Se puede editar tareas "en curso", modificando las propiedades de dicha tarea.
- Se pueden borrar tareas "en curso", o cancelarlas.
- Se puede concluir una tarea en curso, repasando sus propiedas y confirmandola.
### Perfiles
- Se pueden crear perfiles nuevos proporcionando los datos que lo componen.
- Se pueden editar perfiles, modificando los datos que los componen.
- Se pueden borrar perfiles.
### Exportar y copias de seguridad
- Se pueden exportar los datos filtrando por perfil, fechas y tags.
- Se pueden hacer copias de seguridad de los datos.
### Datos
- Se pueden ver los datos guardados en forma de horario/calendario, filtrando por perfil, fechas y tags.
- Se pueden ver los datos guardados en forma de diagrama de sectores por perfil, filtrando por fecha y hora.

## Estructura

La aplicación estará dividida en las siguientes 5 capas, de más externa a más interna:

1. Interfaz de Usuario
2. Dominio
3. Persistencia

### La interfaz de usuario

La interfaz será por ahora una una API Rest. En esta se expondrán los modelos Profile y Task, y se proporcionarán endpoints que, dependiendo del método, llevarán a cabo las diferentes funcionalidades de la aplicación. Se usarán los códigos de estado del propio protocolo HTTP para dar información sobre el resultado de las operaciones. Puede encontrar más detalles sobre la api en la [documentación de la API de Task Tracker](2-Api.md)

### Dominio

El Dominio del programa estará formado de un controlador de dominio y el dominio como tal. El Controlador de Dominio es una capa intermedia que sirve para aislar la parte del programa que tiene que ver con el usuario del funcionamiento interno de este. Este controlador permite hacer funcionar el mismo programa con varias capas externas (API, Aplicación de escritorio, web app,...).

### Persistencia

La Persistencia también estará formada de una capa de persistencia y una persistencia como tal para facilitar el uso de diferentes sistemas de almacenamiento. El proyecto empezará usando una persistencia básica con el modulo [shelve de python](https://docs.python.org/3/library/shelve.html). Y irá evolucionando con el tiempo y las necesidades.