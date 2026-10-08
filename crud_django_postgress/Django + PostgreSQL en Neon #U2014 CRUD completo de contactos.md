
# DJANGO + POSTGRESQL EN NEON
## CRUD completo de contactos

## ¿Qué vamos a construir?

Una aplicación para administrar contactos:

```text
CREAR
CONSULTAR
EDITAR
ELIMINAR
```

La aplicación estará hecha con:

```text
Python
Django
PostgreSQL
Neon
```

---

# 1. CREAR EL PROYECTO

Abrir una terminal:

```bash
mkdir django_contactos
cd django_contactos
```

Crear el entorno virtual:

```bash
python -m venv venv
```

Activarlo:

```bash
venv\Scripts\activate
```

Instalar Django:

```bash
pip install django
```

Crear el proyecto:

```bash
django-admin startproject config .
```

Crear la aplicación:

```bash
python manage.py startapp contactos
```

---

# 2. CREAR LA BASE DE DATOS EN NEON

Entrar a:

```text
https://neon.tech
```

Crear una cuenta o iniciar sesión.

Crear un proyecto nuevo.

Por ejemplo:

```text
Nombre: django_contactos
```

Neon creará una base de datos PostgreSQL.

En el panel de Neon buscar la opción:

**Connect**

Allí aparecerá una cadena parecida a:

```text
postgresql://usuario:contraseña@host.neon.tech/nombre_bd?sslmode=require
```

Vamos a utilizar esa conexión.

---

# 3. INSTALAR EL CONECTOR DE POSTGRESQL

Con el entorno virtual activado:

```bash
pip install psycopg[binary] dj-database-url python-dotenv
```

### ¿Para qué sirve cada uno?

```text
Django
   ↓
dj-database-url
   ↓
PostgreSQL
   ↓
Neon
```

`psycopg` permite que Python se comunique con PostgreSQL.

`dj-database-url` permite utilizar fácilmente la cadena de conexión de Neon.

`python-dotenv` permite guardar la conexión en un archivo `.env`.

---

# 4. CREAR EL ARCHIVO .ENV

En la carpeta principal del proyecto crear:

```text
.env
```

Debe quedar:

```text
django_contactos/
│
├── .env
├── manage.py
├── config/
└── contactos/
```

Dentro de `.env` colocar la cadena que entrega Neon:

```text
DATABASE_URL=postgresql://usuario:contraseña@host.neon.tech/nombre_bd?sslmode=require
```

### IMPORTANTE

Cada estudiante debe colocar **su propia cadena de conexión de Neon**.

No compartirla ni subirla a GitHub.

---

# 5. CONFIGURAR DJANGO PARA USAR NEON

Abrir:

```text
config/settings.py
```

Buscar al comienzo:

```python
from pathlib import Path
```

Agregar:

```python
import os
from dotenv import load_dotenv
import dj_database_url
```

Después de:

```python
BASE_DIR = Path(__file__).resolve().parent.parent
```

agregar:

```python
load_dotenv(BASE_DIR / ".env")
```

Ahora buscar:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

Eliminarlo y colocar:

```python
DATABASES = {
    "default": dj_database_url.parse(
        os.environ.get("DATABASE_URL")
    )
}
```

Ahora Django utilizará PostgreSQL de Neon.

---

# 6. ¿QUÉ CAMBIÓ?

Antes:

```text
Django
   ↓
SQLite
```

Ahora:

```text
Django
   ↓
PostgreSQL
   ↓
Neon
```

Nuestro código Python prácticamente **no cambia**.

Esto es importante:

> El CRUD sigue siendo el mismo. Lo que cambia es dónde se almacenan los datos.

---

# 7. REGISTRAR LA APLICACIÓN

En:

```text
config/settings.py
```

buscar:

```python
INSTALLED_APPS = [
```

Agregar:

```python
"contactos",
```

Por ejemplo:

```python
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "contactos",
]
```

---

# 8. CREAR EL MODELO

Abrir:

```text
contactos/models.py
```

Copiar:

```python
from django.db import models


class Contacto(models.Model):

    nombre = models.CharField(max_length=100)

    correo = models.EmailField()

    telefono = models.CharField(max_length=20)

    mensaje = models.TextField()

    def __str__(self):
        return self.nombre
```

---

# 9. RELACIÓN CON POO

Esto ya lo conocemos de Python:

```python
class Contacto:
```

Estamos creando una clase.

En Django:

```python
class Contacto(models.Model):
```

Creamos un modelo.

Django utilizará ese modelo para crear una tabla en PostgreSQL.

```text
CLASE
  ↓
MODELO DJANGO
  ↓
TABLA POSTGRESQL
  ↓
NEON
```

---

# 10. CREAR LA TABLA EN NEON

Ejecutar:

```bash
python manage.py makemigrations
```

Después:

```bash
python manage.py migrate
```

Django enviará las instrucciones a PostgreSQL.

La tabla será creada en la base de datos de Neon.

---

# 11. VERIFICAR NEON

Volver al panel de Neon.

Entrar al explorador de datos.

Allí podremos encontrar las tablas creadas por Django.

Entre ellas estará nuestra tabla:

```text
contactos_contacto
```

Django creó la tabla a partir de:

```python
class Contacto(models.Model):
```

---

# 12. CREAR LAS VISTAS CRUD

Abrir:

```text
contactos/views.py
```

Copiar:

```python
from django.shortcuts import render
from .models import Contacto


# CREAR
def crear(request):

    if request.method == "POST":

        contacto = Contacto(
            nombre=request.POST["nombre"],
            correo=request.POST["correo"],
            telefono=request.POST["telefono"],
            mensaje=request.POST["mensaje"]
        )

        contacto.save()

    return render(
        request,
        "contactos/formulario.html"
    )


# LISTAR
def listar(request):

    contactos = Contacto.objects.all()

    return render(
        request,
        "contactos/lista.html",
        {"contactos": contactos}
    )


# VER
def detalle(request, id):

    contacto = Contacto.objects.get(id=id)

    return render(
        request,
        "contactos/detalle.html",
        {"contacto": contacto}
    )


# EDITAR
def editar(request, id):

    contacto = Contacto.objects.get(id=id)

    if request.method == "POST":

        contacto.nombre = request.POST["nombre"]
        contacto.correo = request.POST["correo"]
        contacto.telefono = request.POST["telefono"]
        contacto.mensaje = request.POST["mensaje"]

        contacto.save()

        return render(
            request,
            "contactos/detalle.html",
            {"contacto": contacto}
        )

    return render(
        request,
        "contactos/formulario.html",
        {"contacto": contacto}
    )


# ELIMINAR
def eliminar(request, id):

    contacto = Contacto.objects.get(id=id)

    contacto.delete()

    contactos = Contacto.objects.all()

    return render(
        request,
        "contactos/lista.html",
        {"contactos": contactos}
    )
```

---

# 13. ¿DÓNDE ESTÁ EL CRUD?

## Crear

```python
contacto = Contacto(...)
```

Creamos el objeto.

Después:

```python
contacto.save()
```

Lo guardamos en PostgreSQL.

---

## Consultar

```python
Contacto.objects.all()
```

Obtiene todos los contactos.

---

## Ver uno

```python
Contacto.objects.get(id=id)
```

Busca un contacto específico.

---

## Editar

```python
contacto.nombre = ...
```

Modificamos el objeto.

Después:

```python
contacto.save()
```

Guardamos los cambios.

---

## Eliminar

```python
contacto.delete()
```

Eliminamos el registro.

---

# 14. CREAR LAS URL

Crear:

```text
contactos/urls.py
```

Copiar:

```python
from django.urls import path
from . import views


urlpatterns = [

    path("", views.crear),

    path("lista/", views.listar),

    path("detalle/<int:id>/", views.detalle),

    path("editar/<int:id>/", views.editar),

    path("eliminar/<int:id>/"),

]
```

### Corrección importante

La última URL debe quedar así:

```python
path(
    "eliminar/<int:id>/",
    views.eliminar
),
```

Por tanto, el archivo completo queda:

```python
from django.urls import path
from . import views


urlpatterns = [

    path("", views.crear),

    path("lista/", views.listar),

    path(
        "detalle/<int:id>/",
        views.detalle
    ),

    path(
        "editar/<int:id>/",
        views.editar
    ),

    path(
        "eliminar/<int:id>/",
        views.eliminar
    ),

]
```

---

# 15. CONECTAR LAS URLS

Abrir:

```text
config/urls.py
```

Copiar:

```python
from django.contrib import admin
from django.urls import path, include


urlpatterns = [

    path(
        "admin/",
        admin.site.urls
    ),

    path(
        "contactos/",
        include("contactos.urls")
    ),

]
```

---

# 16. CREAR LOS HTML

Crear las carpetas:

```text
contactos/
└── templates/
    └── contactos/
```

Vamos a utilizar solamente tres páginas:

```text
formulario.html
lista.html
detalle.html
```

---

# 17. FORMULARIO

Crear:

```text
contactos/templates/contactos/formulario.html
```

Copiar:

```html
<!DOCTYPE html>
<html lang="es">

<head>

    <meta charset="UTF-8">

    <title>Contacto</title>

</head>

<body>

<h1>Contacto</h1>

<form method="POST">

    {% csrf_token %}

    <p>
        <label>Nombre:</label><br>

        <input
            type="text"
            name="nombre"
            value="{{ contacto.nombre|default:'' }}"
            required
        >
    </p>

    <p>
        <label>Correo:</label><br>

        <input
            type="email"
            name="correo"
            value="{{ contacto.correo|default:'' }}"
            required
        >
    </p>

    <p>
        <label>Teléfono:</label><br>

        <input
            type="text"
            name="telefono"
            value="{{ contacto.telefono|default:'' }}"
            required
        >
    </p>

    <p>
        <label>Mensaje:</label><br>

        <textarea
            name="mensaje"
            required
        >{{ contacto.mensaje|default:'' }}</textarea>
    </p>

    <button type="submit">
        Guardar
    </button>

</form>

<br>

<a href="/contactos/lista/">
    Ver contactos
</a>

</body>

</html>
```

---

# 18. LISTAR

Crear:

```text
contactos/templates/contactos/lista.html
```

Copiar:

```html
<!DOCTYPE html>
<html lang="es">

<head>

    <meta charset="UTF-8">

    <title>Contactos</title>

</head>

<body>

<h1>Lista de contactos</h1>

<a href="/contactos/">
    Nuevo contacto
</a>

<hr>

{% for contacto in contactos %}

    <h3>
        {{ contacto.nombre }}
    </h3>

    <p>
        {{ contacto.correo }}
    </p>

    <p>
        {{ contacto.telefono }}
    </p>

    <a href="/contactos/detalle/{{ contacto.id }}/">
        Ver
    </a>

    |

    <a href="/contactos/editar/{{ contacto.id }}/">
        Editar
    </a>

    |

    <a href="/contactos/eliminar/{{ contacto.id }}/">
        Eliminar
    </a>

    <hr>

{% empty %}

    <p>
        No hay contactos.
    </p>

{% endfor %}

</body>

</html>
```

---

# 19. VER UN CONTACTO

Crear:

```text
contactos/templates/contactos/detalle.html
```

Copiar:

```html
<!DOCTYPE html>
<html lang="es">

<head>

    <meta charset="UTF-8">

    <title>Detalle</title>

</head>

<body>

<h1>Detalle del contacto</h1>

<p>
    <strong>Nombre:</strong>
    {{ contacto.nombre }}
</p>

<p>
    <strong>Correo:</strong>
    {{ contacto.correo }}
</p>

<p>
    <strong>Teléfono:</strong>
    {{ contacto.telefono }}
</p>

<p>
    <strong>Mensaje:</strong>
    {{ contacto.mensaje }}
</p>

<br>

<a href="/contactos/editar/{{ contacto.id }}/">
    Editar
</a>

<br><br>

<a href="/contactos/lista/">
    Volver
</a>

</body>

</html>
```

---

# 20. PROBAR

Ejecutar:

```bash
python manage.py runserver
```

Abrir:

```text
http://127.0.0.1:8000/contactos/
```

---

# 21. PROBAR EL CRUD

### Crear

Ingresar:

```text
Nombre
Correo
Teléfono
Mensaje
```

Pulsar:

**Guardar**

---

### Consultar

Pulsar:

**Ver contactos**

---

### Ver

Pulsar:

**Ver**

---

### Editar

Pulsar:

**Editar**

Cambiar algún dato y guardar.

---

### Eliminar

Pulsar:

**Eliminar**

El registro desaparecerá.

---

# 22. COMPROBAR EN NEON

Después de crear algunos contactos, ir a Neon y abrir el explorador de datos.

La información que vimos en Django ahora estará almacenada en PostgreSQL.

```text
FORMULARIO
     ↓
DJANGO
     ↓
MODELO
     ↓
POSTGRESQL
     ↓
NEON
```

Por ejemplo:

```text
id | nombre | correo          | telefono
---|--------|-----------------|---------
1  | Juan   | juan@gmail.com  | 3001111111
2  | Ana    | ana@gmail.com   | 3012222222
```

---

# 23. ¿QUÉ APRENDIMOS?

Ya conocíamos Python y POO.

Ahora agregamos Django:

```text
Python
   ↓
POO
   ↓
Django
   ↓
CRUD
```

Y agregamos una base de datos real:

```text
Django
   ↓
PostgreSQL
   ↓
Neon
```

El CRUD completo queda:

```text
CREATE
Contacto(...)
save()

READ
objects.all()
objects.get()

UPDATE
contacto.nombre = ...
save()

DELETE
contacto.delete()
```

La idea principal es:

> **Django utiliza nuestras clases de Python para trabajar con datos almacenados en PostgreSQL.**

---

# RETO

Agregar un campo:

```text
empresa
```

Debe funcionar en:

```text
✓ Crear
✓ Consultar
✓ Ver
✓ Editar
```

Después ejecutar:

```bash
python manage.py makemigrations
python manage.py migrate
```

Finalmente comprobar en Neon que la nueva columna apareció en la tabla.