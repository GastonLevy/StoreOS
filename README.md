# TiendaYaca

**TiendaYaca** is an inventory and sales management system designed for small and medium-sized businesses. In addition to managing products and transactions, it offers:

* Management of current accounts, suppliers, and payments.  
* A specialized module for restaurants with menu, dish, table, and kitchen management.

---

## Requirements

Before installing TiendaYaca, make sure you have the following requirements:

### Required Software

* Python **3.8 or higher** → [Download here](https://www.python.org/downloads/)
* MySQL (or another database manager of your choice)
* Git (optional, if you plan to clone the repository) → [Download here](https://git-scm.com/)

### Python Packages Used

TiendaYaca uses the following main packages:

* **Django** (main web framework)  
* **mysqlclient** (MySQL connector)  
* **Django REST Framework** (for API)  
* **djangorestframework-simplejwt** (JWT token authentication)  
* **django-cors-headers** (CORS handling)  
* **django-ckeditor** (rich text editor)  
* **django-widget-tweaks** (form customization)  
* **gunicorn** (WSGI server for production)  
* **pandas** (data management)  
* **pillow** (image processing)  
* **whitenoise** (static file management in production)  
* **django-user-agents** (device and browser detection)  
* **django-extensions** (extra Django tools)  
* **xhtml2pdf** (PDF document generation in Django)

You can view all dependencies in the `requirements.txt` file.

---

## Installation

### 1. Clone the Repository

If you use Git:

```bash
git clone [URL not provided since it's private.]
cd tiendayaca
```

If you don't use Git, you can download the code manually.

### 2. Create and Activate a Virtual Environment

#### Windows (CMD)

```bash
python -m venv venv_clear
venv_clear\Scripts\activate
```

#### Windows (PowerShell)

```bash
python -m venv venv_clear
.\venv_clear\Scripts\Activate
```

#### Linux/macOS

```bash
python3 -m venv venv_clear
source venv_clear/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file at the project root with the following content:

```env
SECRET_KEY='your_secret_key'
DEBUG=True
DATABASE_URL='mysql://user:password@localhost/tiendayaca'
```

Adjust the `DATABASE_URL` variable according to the database manager you use.

### 5. Apply Migrations and Run the Server

```bash
python manage.py migrate
python manage.py runserver
```

The project will be available at [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

---

## Project Structure

```bash
TiendaYaca/
├── accounts/       # Account management, forms, models, and related views.
├── cash_register/  # Cash register functionalities.
├── checkout/       # Payment processing and shopping cart management.
├── cyber_control/  # Device control or monitoring module.
├── excel_import/   # Excel data import functionalities.
├── inventory/      # Inventory management (categories, items, etc.).
├── landing_page/   # Views and templates for the landing page.
├── receptions/     # Goods or services reception management.
├── self_logs/      # Internal logging and monitoring.
├── self_wiki/      # Internal documentation or wiki system.
├── storeos/        # Main Django configuration (settings, urls, wsgi, etc.).
├── templates/      # General project templates.
└── users/          # User management, profiles, and authentication.
```

Each directory contains specific subfolders and files implementing its corresponding functionality.

---

## License

TiendaYaca is proprietary software delivered to a company for internal use.  
It is not publicly available or distributed under an open-source license.
