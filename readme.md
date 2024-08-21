## Instalación

Solo tienen que montar el contenedor con:

```bash
 docker compose up
```
## Documentación OPENAPI

http://localhost:9090/redoc/    
http://localhost:9090/swagger/

## Autenticación
En el proceso de montaje del contenedor se crea un super usuario con los siguientes datos:
> email: jhocce3022@hotmail.com
 password: 25733034
>

Este usuario es el que servira para iniciar sesión en:
```
http://localhost:9090/user/
```
Degun lo indicado en la documentación enviar por post:
```json
{
    "email":"jhocce3022prueba@hotmail.com",
    "password":"25733034"
}
```
Esto retornaria como respuesta
```json
{
    "status": "success",
    "operacion": "LoginUserAPI",
    "entidad": "login",
    "mensaje_user": [
        {
            "mensaje": "iniciando sesion"
        }
    ],
    "mensaje_server": [],
    "json": [
        {
            "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbiI6ImYzOWZmMzBkLTMwYzUtNGY4My1iZWQ2LTk1NTllZGUxMTM5NSIsInBrX3B1YmxpY2EiOiJlYmVlNWQ2Mi1kNGI0LTQyNDQtOWUwOS1mMTRjOTgxOTkyYmYifQ.lpUaDXhFVeOeO8g2lfKHI0pLFYq_j1plALGikIZePwg"
        }
    ]
}
```
El token generado es un jwt con la informacion necesaria para realziar los procesos de autenticación de la petición este debe ser enviado en el header como:
```json
    "Authorization":"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbiI6ImYzOWZmMzBkLTMwYzUtNGY4My1iZWQ2LTk1NTllZGUxMTM5NSIsInBrX3B1YmxpY2EiOiJlYmVlNWQ2Mi1kNGI0LTQyNDQtOWUwOS1mMTRjOTgxOTkyYmYifQ.lpUaDXhFVeOeO8g2lfKHI0pLFYq_j1plALGikIZePwg"
```
Con este usuario y token se podran realizar las acciones posteriores de gestion de usuario, es decir, hacer CRUD a los user.


## Funcionalidades

La mecanica del proyecto se basa en cuatro partes

1. Gestión de Usuario:
    Documentación: [redoc](http://localhost:9090/redoc/#tag/user "Documentacion en redoc") - [swagger](http://localhost:9090/swagger/ "Documentacion en swagger")
    Además de gestionar un CRUD se puede buscar usuarios por nombre enviando el parametro usuario con el nombre el usuario a buscar


2. Gestión de producto:
    Documentación: [redoc](http://localhost:9090/redoc/#tag/producto "Documentacion en redoc") - [swagger](http://localhost:9090/swagger/ "Documentacion en swagger")
   
    Se crea un producto sobre el se llenan lo campos indicados, entre los campos indicados en la respuesta estara la imagen correspondiente a la url de la imagen del QR.
3. Operaciones de entrada:
    Un operador escanea el QR el cual contendra:
    ```json
    {
		"code":"rg9GiVpTuU45PTZ"
	}
    ```
    Con este codigo puede obtener informacion del producto enviando por get a la gestion de producto el parametros "code" con el codigo escaneado y con la informacion del usuario y la cantidad de producto en cuestion generara una operacion entrada de producto al almacen.

4. Operaciones de salida:
    Un operador escanea el QR el cual contendra:
    ```json
    {
		"code":"rg9GiVpTuU45PTZ"
	}
    ```
    Con este codigo puede obtener informacion del producto enviando por get a la gestion de producto el parametros "code" con el codigo escaneado y con la informacion del usuario y la cantidad de producto en cuestion generara una operacion salida de producto del almacen.
