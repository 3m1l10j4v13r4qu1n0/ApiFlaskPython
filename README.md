# ApiFlaskPython

ApiFlaskPython/
├── app/
│   ├── __init__.py         # Inicializa la app y extensiones
│   ├── models.py           # Modelos de base de datos
│   ├── routes/
│   │   ├── __init__.py
│   │   └── main.py         # Rutas (Controladores)
│   ├── templates/
│   │   └── index.html      # Vistas
│   └── forms.py            # Formularios (si usas Flask-WTF)
├── instance/              # Configuración específica de la instancia
│   └── database.db        # Base de datos SQLite
├── config.py               # Configuración
├── run.py                  # Arranca la app
├── migrations/             # Migraciones de base de datos
│   ├── env.py              # Configuración de migraciones
│   ├── README.md           # Documentación de migraciones
│   ├── script.py.mako      # Plantilla de script de migración
│   └── versions/           # Versiones de migraciones
│       └── 20231001_123456_initial.py  # Ejemplo de migración
├── requirements.txt        # Requerimientos y lista de librerías
├── tests/                  # Pruebas unitarias
│   ├── __init__.py
│   ├── test_app.py         # Pruebas de la aplicación
│   └── test_models.py       # Pruebas de modelos
├── .gitignore              # Ignora archivos no deseados en Git
└── .env                    # Variables de entorno


