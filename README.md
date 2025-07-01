# TiendaYaca

**TiendaYaca** es un sistema de gestión de inventario y ventas diseñado para pequeñas y medianas empresas. Además de administrar productos y transacciones, ofrece:

*   Gestión de cuentas corrientes, proveedores y pagos.
*   Módulo especializado para restaurantes con administración de menús, platos, mesas y cocina.

---

## Requisitos

Antes de instalar TiendaYaca, asegúrate de tener los siguientes requisitos:

### Software necesario

*   Python **3.8 o superior** → [Descargar aquí](https://www.python.org/downloads/)
*   MySQL (u otro gestor de base de datos de tu elección)
*   Git (opcional, si vas a clonar el repositorio) → [Descargar aquí](https://git-scm.com/)

### Paquetes de Python utilizados

TiendaYaca usa los siguientes paquetes principales:

*   **Django** (framework web principal)
*   **mysqlclient** (conector para MySQL)
*   **Django REST Framework** (para API)
*   **djangorestframework-simplejwt** (autenticación con tokens JWT)
*   **django-cors-headers** (manejo de CORS)
*   **django-ckeditor** (editor de texto enriquecido)
*   **django-widget-tweaks** (personalización de formularios)
*   **gunicorn** (servidor WSGI para producción)
*   **pandas** (manejo de datos)
*   **pillow** (procesamiento de imágenes)
*   **whitenoise** (gestión de archivos estáticos en producción)
*   **django-user-agents** (detección de dispositivos y navegadores)
*   **django-extensions** (herramientas adicionales para Django)
*   **xhtml2pdf** (generación de documentos PDF en Django)

Puedes ver todas las dependencias en el archivo `requirements.txt`.

---

## Instalación

### 1. Clonar el repositorio

Si usas Git:

git clone [No pongo la URL ya que no está disponible publicamente.]
cd tiendayaca

Si no usas Git, puedes descargar el código manualmente.

### 2. Crear y activar un entorno virtual

#### Windows (CMD)

python -m venv venv_clear
venv_clear\Scripts\activate


#### Windows (PowerShell)

python -m venv venv_clear
.\venv_clear\Scripts\Activate


#### Linux/macOS

python3 -m venv venv_clear
source venv_clear/bin/activate


### 3. Instalar las dependencias

pip install -r requirements.txt


### 4. Configurar variables de entorno

Crea un archivo `.env` en la raíz del proyecto con el siguiente contenido:

### ini
SECRET_KEY='tu_clave_secreta'
DEBUG=True
DATABASE_URL='mysql://usuario:contraseña@localhost/tiendayaca'
Ajusta la variable DATABASE_URL según el gestor de base de datos que utilices.

5. Aplicar migraciones y ejecutar el servidor
python manage.py migrate
python manage.py runserver
El proyecto estará disponible en http://127.0.0.1:8000/.

Estructura del Proyecto
TiendaYaca/
├── accounts/       # Gestión de cuentas, formularios, modelos y vistas relacionadas.
├── cash_register/  # Funcionalidades relacionadas con la caja registradora.
├── checkout/       # Procesamiento de pagos y gestión del carrito de compras.
├── cyber_control/  # Módulo de control de dispositivos o monitoreo.
├── excel_import/   # Funcionalidades para importar datos desde Excel.
├── inventory/      # Gestión del inventario (categorías, ítems, etc.).
├── landing_page/   # Vistas y plantillas para la página de inicio.
├── receptions/     # Gestión de recepciones de mercancías o servicios.
├── self_logs/      # Registro y monitoreo de acciones internas.
├── self_wiki/      # Documentación interna o wiki del sistema.
├── storeos/        # Configuración principal de Django (settings, urls, wsgi, etc.).
├── templates/      # Plantillas generales del proyecto.
└── users/          # Gestión de usuarios, perfiles y autenticación.
Cada uno de estos directorios contiene subcarpetas y archivos específicos que implementan la funcionalidad correspondiente.

Licencia
El código de TiendaYaca fue desarrollado a medida y entregado a una empresa que lo utiliza internamente. No cuenta con una licencia de código abierto ni está disponible para distribución pública.
