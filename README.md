<h1>🚀 StoreOS</h1>
<h3>Multi-Tenant Inventory, Sales & Restaurant Management Platform</h3>

<p><strong>StoreOS</strong> is a full-featured <strong>SaaS platform</strong> designed for small and medium businesses that need a modern, scalable system to manage inventory, sales, suppliers, payments. 
It supports <strong>multiple companies (multi-tenant architecture)</strong>, allowing each business to operate independently within the same system.</p>

<p>This project demonstrates professional-level Django development, including modular architecture, REST APIs, role-based access control, and production-ready configuration.</p>

<hr>

<h2>🧠 Key Features</h2>

<h3>🔐 Multi-Tenant Architecture</h3>
<ul>
  <li>Each company has isolated data (products, users, sales, suppliers, etc.).</li>
  <li>Centralized administration while maintaining strict data separation.</li>
</ul>

<h3>📦 Inventory Management</h3>
<ul>
  <li>Categories, items, bulk imports (Excel), low-stock alerts.</li>
  <li>Stock movements, item logs, purchase receptions.</li>
</ul>

<h3>💰 Sales & Checkout Module</h3>
<ul>
  <li>Cart system, checkout flow, payment handling.</li>
  <li>Daily summaries and cash register tracking.</li>
</ul>

<h3>📄 Account & Finance Tools</h3>
<ul>
  <li>Current accounts, supplier management, pending payments.</li>
  <li>Customer tracking and activity history.</li>
</ul>

<h3>🧰 Internal Utilities</h3>
<ul>
  <li>PDF generation, device detection, custom admin extensions, internal wiki for customers.</li>
</ul>

<hr>

<h2>🖼️ Screenshots</h2>

<hr>

<h2>🛠️ Tech Stack</h2>

<h3>Backend</h3>
<ul>
  <li><strong>Django</strong> (core framework)</li>
  <li><strong>Django REST Framework</strong> (API)</li>
  <li><strong>MySQL</strong></li>
  <li><strong>JWT Authentication (SimpleJWT)</strong></li>
</ul>

<h3>Utilities & Libraries</h3>
<ul>
  <li>django-cors-headers</li>
  <li>django-ckeditor</li>
  <li>django-widget-tweaks</li>
  <li>django-extensions</li>
  <li>django-user-agents</li>
  <li>xhtml2pdf</li>
  <li>pandas, pillow</li>
  <li>whitenoise</li>
  <li>gunicorn</li>
</ul>

<hr>

<h2>🏗️ Architecture Overview</h2>

<pre>
StoreOS (SaaS)
│
├── Multi-Tenant Core
│   ├── Company model
│   ├── Company-aware middleware
│   └── Tenant data isolation
│
├── Modules
│   ├── Inventory
│   ├── Sales / Checkout
│   ├── Restaurant
│   ├── Suppliers & Payments
│   ├── Receptions
│   ├── Users & Roles
│   └── Internal Tools (PDF, logs, cyber control)
│
└── API Layer (DRF)
    ├── Auth (JWT)
    ├── CRUD endpoints per module
    └── Pagination / filtering utilities
</pre>

<hr>

<h2>📥 Installation</h2>

<h3>1. Clone the Repository</h3>
<pre><code>git clone https://github.com/GastonLevy/StoreOS
cd StoreOS
</code></pre>

<h3>2. Create a Virtual Environment</h3>
<pre><code>python -m venv venv
source venv/bin/activate      # Linux/macOS
venv\Scripts\activate         # Windows
</code></pre>

<h3>3. Install Dependencies</h3>
<pre><code>pip install -r requirements.txt
</code></pre>

<h3>4. Configure Environment Variables</h3>
<pre><code>
SECRET_KEY="your_secret_key"
DEBUG=True
DATABASE_URL="mysql://user:password@localhost/storeos"
</code></pre>

<h3>5. Apply Migrations & Run</h3>
<pre><code>
python manage.py migrate
python manage.py runserver
</code></pre>

<p>Access at: <strong>http://127.0.0.1:8000/</strong></p>

<hr>

<h2>📂 Project Structure</h2>

<pre>
StoreOS/
├── accounts/          # Authentication, roles, profiles
├── cash_register/     # Cash management & daily reports
├── checkout/          # Sales workflow & payments
├── cyber_control/     # Device usage tracking module
├── excel_import/      # Bulk import tools
├── inventory/         # Item, categories, stock logs
├── landing_page/      # Public-facing landing page
├── receptions/        # Goods reception workflow
├── self_logs/         # Internal logs
├── self_wiki/         # Customer documentation
├── storeos/           # Core config (settings, urls)
└── users/             # User accounts & permissions
</pre>

<hr>

<h2>🔒 License</h2>
<p>StoreOS was built as proprietary software for business environments. It is not open-source and is shared for demonstration and portfolio purposes only.</p>
