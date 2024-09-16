## WebAPP para el CNEISI FRLP-UTN

### CNEISI

Congreso Nacional de Estudiantes de Ingenieria en Sistemas de Informacion.

### Descripción del Proyecto

Este proyecto, desarrollado con Django, es una plataforma web diseñada para gestionar las inscripciones al CNEISI La Plata. Permite a los usuarios realizar y administrar sus registros de manera eficiente.

### Tecnologías Utilizadas

* **Framework:** Django 5.1.1
* **Librerías:**
  * django-bootstrap5: Para integrar el framework Bootstrap 5 y mejorar la apariencia visual.
  * django-bootstrap-icons: Para utilizar los iconos de Bootstrap.
  * django-environ: Para gestionar las variables de entorno.
  * django-import-export: Para importar y exportar datos.
  * django-phonenumber-field: Para manejar números de teléfono.
  * phonenumbers: Librería de Python para la validación y manipulación de números de teléfono.
  * pillow: Para el procesamiento de imágenes.

### Requisitos Previos

* **Python:** Asegúrate de tener instalado Python 3.x.
* **Virtualenv:** Recomendado para aislar las dependencias del proyecto.

### Instalación

1. **Clonar el repositorio:**

   ```bash
   git clone https://tu-repositorio.git
   ```

2. **Crear un entorno virtual:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # En Linux/macOS
   venv\Scripts\activate  # En Windows
   ```

3. **Instalar las dependencias:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar la base de datos:**
   * Crea una base de datos en tu sistema de gestión de bases de datos.
   * Configura las variables de entorno en un archivo `.env` (ejemplo):

    ```python
    # El sistema usa sqlite en desarrollo y MariaDB en produccion
    # Para MariaDB se debe instalar
    #pip install mysql-connector-python

     DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': env('DATABASE_NAME'),
            'USER': env('DATABASE_USER'),
            'PASSWORD': env('DATABASE_PASS'),
            'HOST': env('DATABASE_HOST'),
            'PORT': env('DATABASE_PORT'),
            'OPTIONS': {
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
            },
        }
    }
    ```

5. **Ejecutar las migraciones:**

   ```bash
   python manage.py migrate
   ```

6. **Iniciar el servidor de desarrollo:**

   ```bash
   python manage.py runserver
   ```

### Estructura del Proyecto

* **urls.py:** Define las URL del proyecto y redireccion a 'urls.py' de core.
* **core/urls.py:** Define las URL del proyecto, que necesitan al usuario autenticado.
* **core/urls_publics.py:** Define las URL del proyecto, que no necesitan de un usuario autenticado.
* **settings.py:** Configuraciones del proyecto.
* **wsgi.py:** Punto de entrada para servidores WSGI.
* **static/:** Archivos estáticos (CSS, JavaScript, imágenes).
* **templates/:** Plantillas Base HTML.

### Uso

Esta plataforma permite a los coordinadores administrar de manera eficiente las inscripciones de sus estudiantes al congreso. Los asistentes, por su parte, pueden realizar su inscripción de forma individual y consultar el horario de las actividades. El sistema contara con un mecanismo de control de cupos para garantizar una organización óptima del evento.

Además, en el futuro, se generan reportes detallados que facilitan la toma de decisiones y el seguimiento de las inscripciones.

### Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue para discutir nuevas características o mejoras.

### Licencia

Este proyecto está licenciado bajo la MIT License. Consulta el archivo [LICENSE](LICENSE) para obtener más información.

