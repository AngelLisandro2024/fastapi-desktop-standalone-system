<div align="center">

# 🖥️ FastAPI Desktop Standalone System
### **Sistema Web de Escritorio Autónomo para Control de Asistencia e Inventario con PyInstaller**

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi&logoColor=white)
![PyInstaller](https://img.shields.io/badge/PyInstaller-EF4444?style=for-the-badge&logo=python&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-38BDF8?style=for-the-badge&logo=tailwind-css&logoColor=white)
![ReportLab](https://img.shields.io/badge/ReportLab-F43F5E?style=for-the-badge&logo=adobe-acrobat-reader&logoColor=white)

</div>

---

## 📖 Descripción del Proyecto

**FastAPI Desktop Standalone System** es una solución diseñada para empaquetar aplicaciones web basadas en FastAPI como **ejecutables de escritorio portables (`.exe`)**. El sistema integra un hilo de ejecución automático para abrir el navegador predeterminado al iniciar el servidor local, administración de usuarios/estudiantes, control de tiempos e inventario, y exportación de reportes institucionales en PDF mediante **ReportLab**.

<img width="1280" height="720" alt="Captura de pantalla (1497)" src="https://github.com/user-attachments/assets/0c521c23-ea4c-4b79-9f1e-d4a8ff7d9021" />


---

## ✨ Características Principales

* 🚀 **Autoejecutable de Escritorio:** Configurado mediante PyInstaller y `threading.Timer` para iniciar Uvicorn y abrir la interfaz directamente en el navegador sin dependencias previas del usuario final.
* 👥 **Gestión de Personas:** Registro de estudiantes y empleados con diferenciación de roles y marcas temporales.
* 📦 **Control de Inventario y Movimientos:** Seguimiento de activos, responsables y control de entradas/salidas en curso.
* 📄 **Generación Dinámica de PDFs:** Creación de reportes generales estilizados con tablas profesionales utilizando ReportLab.
* 🎨 **UI Moderna (Tailwind CSS):** Interfaz responsiva estructurada mediante herencia de plantillas con Jinja2 y componentes visuales limpios.

---

## 🛠️ Stack Tecnológico

| Categoría | Tecnología |
| :--- | :--- |
| **Backend & Servidor** | Python 3, FastAPI, Uvicorn |
| **Empaquetado (Desktop)** | PyInstaller (`main.spec`) |
| **Frontend & UI** | HTML5, Jinja2, Tailwind CSS, FontAwesome |
| **Generación de Reportes** | ReportLab (Streaming PDF) |
| **Manejo de Formularios** | `python-multipart` |

---

## 📂 Estructura del Proyecto

```text
fastapi-desktop-standalone-system/
├── templates/
│   ├── base.html       # Layout principal con barra de navegación y sidebar
│   ├── index.html      # Dashboard con tarjetas estadísticas y actividad reciente
│   ├── users.html      # Módulo de registro y listado de usuarios/estudiantes
│   └── inventory.html  # Módulo de control de movimientos e inventario
├── main.py             # Servidor FastAPI, gestión en memoria y apertura de navegador
├── main.spec           # Configuración de compilación optimizada para PyInstaller
└── requirements.txt    # Dependencias del proyecto

```
⚡ Instalación y Ejecución Local
Clonar el repositorio:

Bash

git clone [https://github.com/AngelLisandro2024/fastapi-desktop-standalone-system.git](https://github.com/AngelLisandro2024/fastapi-desktop-standalone-system.git)

cd fastapi-desktop-standalone-system

Crear y activar el entorno virtual:

Bash

python3 -m venv venv

# En Windows:

venv\Scripts\activate

# En Linux/macOS:

source venv/bin/activate

Instalar dependencias:

Bash

pip install -r requirements.txt

Ejecutar la aplicación:

Bash

python main.py

Compilar a Ejecutable (.EXE portable):

Bash

pyinstaller main.spec

👨‍💻 Autor
Diseñado y desarrollado por Angel Fernández (@AngelLisandro2024).
