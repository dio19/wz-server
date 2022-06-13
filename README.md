# wz-client

### Version deployada en Netlify

```
https://wz-server-dio.herokuapp.com/

```

### Para levantar el servidor

```
gunicorn src.runner:application

```

Automaticamente levantara el servidor en http://127.0.0.1:8000
El BackEnd esta implementado en Python, Flask y los datos persisten en una Base de datos que cree con MongoDB Atlas.

### http://127.0.0.1:8000/tasks

Devuelve todas las tasks que se encuentran en la Colecction tasks de MongoDB atlas, se le pueden pasar como parametros adicionales "completed" y/o "title" para filtar por ambos valores.

### http://127.0.0.1:8000/tasks/id

Devuelve la task que matchea con el id proporcionada. En el caso de que no se encuentre, devuelve el error correspondiente.

### http://127.0.0.1:8000/users

Devuelve todos los usuarios que se encuentran en la Colecction Users de MongoDB atlas

### http://127.0.0.1:8000/users/id

Devuelve el user que matchea con el id proporcionado. En el caso de que no se encuentre, devuelve el error correspondiente.

### http://127.0.0.1:8000/users/user_id/tasks

Devuelve todas las tareas relacionadas con el id de usuario proporcionado. Opcionalmente puede recibir los valores completed y/o title, para filtrar tambien por estos valores.
