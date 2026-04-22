 ![demo](.github/assets/image.png)    

# 🚀 Kepler CLI

A custom CLI tool to generate professional monthly work reports from your Git activity using AI.

---

## 📌 Description

Kepler CLI is a command-line tool designed to:

* Navigate your local file system safely
* Detect and work with Git repositories
* Extract commit history
* Transform commits into structured data (JSON) using AI
* Generate monthly reports in Word (`.docx`)
* Use AI to enhance and summarize development activity

---

## ⚙️ Features

### ✅ Implemented

* Interactive CLI interface
* Custom command system
* Safe terminal command execution
* Directory navigation (`cd`, `ls`, `pwd`, etc.)
* Permission control for system access
* Git commit extraction
* AI integration for commit analysis and summarizing
* **Monthly report generation in Word (`.docx`)**

### 🚧 In Progress

* Smart filtering of commits

---

## 🛠️ Environment Setup

Before running the CLI, you can set environment variables in a `.env` file in the root directory:

```env
# Google Gemini API Key (Required)
GEMINI_API_KEY=your_api_key_here

# AI Model Configuration (Optional, defaults to gemini-2.5-flash)
GEMINI_MODEL=gemini-2.5-flash

# Report Information (Optional)
COMPANY_NAME=Your Company
PROJECT_NAME=Project Name
EMPLOYEE_NAME=Your Name
```

---

## 📝 Configuration & Prompts

### ⚙️ System Config
The project uses a structured configuration system located in `config/`. It handles API authentication, model selection, and report settings. Environment variables are supported for development, and persistent configuration support is available through `config_impl.py`.

### 🧠 AI Prompts
The core logic for report generation relies on Markdown templates.
* **Custom Prompt:** If present, the CLI reads `prompts/generate_summary.md`.
* **Fallback Template:** If that file does not exist, Kepler uses `prompts/generate_summary.example.md`.
* **Customization:** Create your own `prompts/generate_summary.md` following the structure of the example file.
* **Variables:** The prompt template supports placeholders like `{commits_data}`, `{period_month}`, `{company_name}`, `{employee_name}`, and `{project_name}`.

---

## 🖥️ CLI Commands

| Command  | Description                  |
| -------- | ---------------------------- |
| generate | Generate report from commits |
| config   | Show current configuration   |
| version  | Show CLI version             |
| help     | Show help menu               |

---

## 📂 Project Structure

```
cli-kepler/
├── cli/                # CLI logic and interface
│   ├── app_info.py     # Version and app metadata
│   ├── commands.py     # Command definitions
│   ├── entrypoint.py   # Main CLI execution flow
│   └── welcome.py      # Welcome messages and UI
├── config/             # Configuration management
│   ├── config.py       # Config interfaces
│   ├── config_impl.py  # Implementation of persistent config
│   └── prompt_config.py # AI prompt loading logic
├── prompts/            # AI Prompt templates
│   ├── generate_summary.example.md
│   └── generate_summary.md (optional, user-defined)
├── service/            # Core business logic
│   ├── ai_service.py   # Gemini AI integration
│   └── word_service.py # Word report (.docx) generation
├── utils/              # Helper functions
│   ├── date_util.py
│   ├── git_util.py
│   └── write_markdown.py
├── main.py             # Entry point script
├── pyproject.toml      # Project dependencies and packaging
└── README.md
```

---

## 🧠 How It Works

1. User navigates to a project directory.
2. CLI detects Git repository.
3. Extracts commit history from the specified period.
4. Processes commits and sends them to Gemini AI using the template in `prompts/generate_summary.md`.
5. AI generates a structured summary (JSON).
6. CLI converts the data into a professional Word report (`.docx`) using the `word_service`.

---

## ⚡ Guía de Instalación (Usuario Final)

Si no eres desarrollador y solo quieres usar Kepler para tus reportes, sigue estos pasos:

### 1. Requisitos Previos
*   **Python 3.10 o superior:** [Descárgalo aquí](https://www.python.org/downloads/). **IMPORTANTE:** Durante la instalación en Windows, marca la casilla que dice **"Add Python to PATH"**.
*   **Git:** [Descárgalo aquí](https://git-scm.com/downloads). Es necesario para que Kepler pueda leer tus commits.

### 2. Instalación de Kepler
Abre una terminal (PowerShell o CMD en Windows) y ejecuta:

```bash
pip install git+https://github.com/Froggap/kepler-cli.git
```

### 3. Configuración Inicial (Obligatorio)
Para que Kepler pueda usar la IA de Google Gemini, necesitas configurar tu API Key:

1.  Obtén una API Key gratuita en [Google AI Studio](https://aistudio.google.com/app/apikey).
2.  En tu terminal, ejecuta:
    ```bash
    kepler config --set-key
    ```
3.  Pega tu clave cuando se te solicite (no se verá mientras escribes por seguridad).

---

## 🛠️ Solución de Problemas y Notas Importantes

### 1. "kepler" no se reconoce como comando interno
Si tras instalarlo el comando falla, es porque la carpeta de Scripts de Python no esté en tus variables de entorno.
*   **Solución:** Busca donde se instaló Python (usualmente `C:\Users\TU_USUARIO\AppData\Roaming\Python\Python3x\Scripts`) y añade esa ruta al PATH de tu sistema.

### 2. Conflictos con OneDrive y carpetas sincronizadas
Si trabajas dentro de carpetas de **OneDrive**, **Dropbox** o **Google Drive**:
*   **Bloqueo de archivos:** Estas herramientas pueden bloquear el archivo `.docx` mientras intentan sincronizarlo, causando que Kepler falle al guardar el reporte.
*   **Rutas demasiado largas:** OneDrive tiende a crear rutas muy largas que superan el límite de Windows (260 caracteres).
*   **Recomendación:** Ejecuta Kepler en proyectos ubicados en rutas locales directas como `C:\Proyectos\mi-repo`.

### 3. Error de Almacenamiento Seguro (Keyring)
Kepler guarda tu API Key en el "Administrador de Credenciales" de Windows para que no tengas que escribirla siempre.
*   Si recibes un error relacionado con `keyring` o `backend`, asegúrate de tener permisos de administrador o intenta definir la clave directamente en un archivo `.env` en la carpeta donde ejecutas el comando:
    ```env
    GEMINI_API_KEY=tu_clave_aqui
    ```

### 4. Ejecución en Repositorios Git
Kepler **debe** ejecutarse dentro de la carpeta de un repositorio Git. Si la carpeta no tiene un `.git`, el comando `generate` fallará porque no encontrará historial que analizar.

---

## 🛠️ Para Desarrolladores (Instalación Local)
Si deseas contribuir o personalizar el comportamiento:

```bash
git clone https://github.com/Froggap/kepler-cli.git
cd kepler-cli
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

pip install -e .
```

---

## ▶️ Uso

```bash
kepler
```

Then use commands like:

```bash
cd your-project
generate
```

You can also run configuration directly:

```bash
kepler config --set-key
kepler config --output-path C:\Users\YourUser\Documents\Reports
```

Generated artifacts:

```bash
commits.json
reporte_<mes>_<año>.docx
```

Current additions related to report generation:

* `config/config_impl.py`
* `service/word_service.py`

---

## 📌 Notes

* The CLI only executes **safe read-only commands**
* No source files are modified
* Works best inside a Git repository

---

## 🔮 Future Plans

* Multi-language support
* Better terminal UX (autocomplete, history)
* Switch IA models
* Generate and send reports by email

---

## 👨‍💻 Author

Built by Froggap 🚀

---

## 📄 License

MIT License © 2026 Froggap

Free to use, modify and distribute with attribution.
