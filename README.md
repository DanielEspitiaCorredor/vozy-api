# Vozy API

API utilizada para listar las publicaciones que realizan los usuarios en Vozy

# Prerequisites

- Docker >=20.10.7
- Docker compose >=1.29.2

# Getting started

La API está dividida en dos modulos, la sección de manejo de usuarios, que contiene los endpoints que se encargan del registro y autenticación y el modulo app, que se encarga manejar el CRUD de las publicaciones.

Para manejar las dependencias, este proyecto utiliza Poetry, el cual permite llevar la trazabilidad de las librerías que son instaladas en el proyecto.

# Installation

Para instalar el proyecto, ejecute en la carpeta del proyecto el siguiente comando

```
docker-compose up -d --build
```

Por último, si los contenedores iniciaron correctamente. La API de vozy estará expuesta en `http://localhost:5000`

# Unit test

Para ejecutar las pruebas unitarias, dentro del contenedor `vozy-app` ejecute `python -m unittest --verbose`. Hasta este momento se encuentran implementadas 11 pruebas que validan el funcionamiento de la aplicación

```
# python -m unittest --verbose
test_create_post_fail (tests.test_vozy_api.VozyAPITest) ... ok
test_create_posts (tests.test_vozy_api.VozyAPITest) ... ok
test_delete_post (tests.test_vozy_api.VozyAPITest) ... ok
test_list_posts (tests.test_vozy_api.VozyAPITest) ...
ok
test_login_fail (tests.test_vozy_api.VozyAPITest) ... User object
ok
test_login_succeeded (tests.test_vozy_api.VozyAPITest) ... User object
ok
test_register_fail (tests.test_vozy_api.VozyAPITest) ... ok
test_register_succeeded (tests.test_vozy_api.VozyAPITest) ... ok
test_update_post (tests.test_vozy_api.VozyAPITest) ... [<Post 61d5189d3fc16c76d09d2b97>]
ok
test_update_post_fail (tests.test_vozy_api.VozyAPITest) ... ok
test_user_already_exist (tests.test_vozy_api.VozyAPITest) ... ok

----------------------------------------------------------------------
Ran 11 tests in 1.200s

OK
```
# Postman collections

Para facilitar la interacción con el proyecto, se adjuntan la coleccion de postman de la API. Para importarla siga los siguientes pasos:

1. En postman, importar la colección vozy_api `Vozy API.postman_collection.json` y el entorno de desarrollo `Vozyapi.postman_environment.json`
2. Seleccionar el entorno desde la aplicación de postman
3. Verificar que las variables de entorno hayan quedado configuradas