![demo](.github/assets/image.png)

# 🚀 Kepler CLI

Una herramienta CLI personalizada para generar informes mensuales profesionales de trabajo a partir de tu actividad de Git usando IA.

---

## 📌 Descripción

Kepler CLI es una herramienta de línea de comandos diseñada para:

- Navegar tu sistema de archivos local de forma segura
- Detectar y trabajar con repositorios Git
- Extraer el historial de commits
- Transformar commits en datos estructurados (JSON) usando IA
- Generar informes mensuales en Word (`.docx`)
- Usar IA para mejorar y resumir la actividad de desarrollo

---

## ⚙️ Funcionalidades

### ✅ Implementadas

- Interfaz CLI interactiva
- Sistema de comandos personalizado
- Ejecución segura de comandos de terminal
- Navegación de directorios (`cd`, `ls`, `pwd`, etc.)
- Control de permisos para acceso al sistema
- Extracción de commits de Git
- Integración con IA para análisis y resumen
- **Generación de informes mensuales en Word (`.docx`)**

### 🚧 En progreso

- Filtrado inteligente de commits

---

## 🛠️ Preparación del Entorno

Antes de ejecutar la CLI, puedes configurar variables de entorno en un archivo `.env` en la raíz del proyecto:

```env
# Clave API de Google Gemini (Obligatoria)
GEMINI_API_KEY=tu_api_key_aqui

# Configuración del modelo de IA (Opcional, por defecto gemini-2.5-flash)
GEMINI_MODEL=gemini-2.5-flash

# Información del informe (Opcional)
COMPANY_NAME=Nombre de la Empresa
PROJECT_NAME=Nombre del Proyecto
EMPLOYEE_NAME=Tu Nombre
```

---

## 📝 Configuración y Prompts

### ⚙️ Configuración del Sistema
El proyecto usa un sistema de configuración localizado en `config/`. Maneja la autenticación de la API, selección de modelo y ajustes del informe. Se admiten variables de entorno para desarrollo y hay soporte de configuración persistente en `config_impl.py`.

### 🧠 Prompts de IA
La lógica principal para la generación del informe se basa en plantillas Markdown.
- **Prompt personalizado:** Si existe, la CLI leerá `prompts/generate_summary.md`.
- **Plantilla de fallback:** Si ese archivo no existe, Kepler usa `prompts/generate_summary.example.md`.
- **Personalización:** Crea tu propio `prompts/generate_summary.md` siguiendo la estructura del ejemplo.
- **Variables:** La plantilla soporta marcadores como `{commits_data}`, `{period_month}`, `{company_name}`, `{employee_name}`, y `{project_name}`.

---

## 🖥️ Comandos CLI

| Comando  | Descripción                  |
| -------- | ---------------------------- |
| generate | Generar informe a partir de commits |
| config   | Mostrar configuración actual |
| version  | Mostrar versión de la CLI    |
| help     | Mostrar ayuda                |
| uninstall | Eliminar configuración local y desinstalar paquete |

---

## 📂 Estructura del Proyecto

```
cli-kepler/
├── cli/                # Lógica e interfaz del CLI
│   ├── app_info.py     # Versión y metadatos
│   ├── commands.py     # Definición de comandos
│   ├── entrypoint.py   # Flujo principal de ejecución
│   └── welcome.py      # Mensajes de bienvenida y UI
├── config/             # Gestión de configuración
│   ├── config.py       # Interfaces de configuración
│   ├── config_impl.py  # Implementación de configuración persistente
│   └── prompt_config.py # Carga de prompts de IA
├── prompts/            # Plantillas de prompts de IA
│   ├── generate_summary.example.md
│   └── generate_summary.md (opcional, definido por el usuario)
├── service/            # Lógica de negocio
│   ├── ai_service.py   # Integración con Gemini AI
│   └── word_service.py # Generación de informes Word (.docx)
├── utils/              # Funciones auxiliares
│   ├── date_util.py
│   ├── git_util.py
│   └── write_markdown.py
├── main.py             # Script de entrada
├── pyproject.toml      # Dependencias y empaquetado
└── README.md
```

---

## 🧠 Cómo Funciona

1. El usuario navega al directorio del proyecto.
2. La CLI detecta el repositorio Git.
3. Extrae el historial de commits del período solicitado.
4. Procesa los commits y los envía a Gemini AI usando la plantilla en `prompts/generate_summary.md`.
5. La IA genera un resumen estructurado (JSON).
6. La CLI convierte los datos en un informe profesional Word (`.docx`) usando `word_service`.

---

## ⚡ Guía de Instalación (Usuario Final)

Si no eres desarrollador y solo quieres usar Kepler para tus informes, sigue estos pasos:

### 1. Requisitos Previos
- **Python 3.10 o superior:** https://www.python.org/downloads/. IMPORTANTE: en Windows marca "Add Python to PATH" durante la instalación.
- **Git:** https://git-scm.com/downloads. Necesario para que Kepler lea tus commits.

### 2. Instalación de Kepler
Abre una terminal (PowerShell o CMD en Windows) y ejecuta:

```bash
pip install git+https://github.com/Froggap/kepler-cli.git
```

### 3. Configuración Inicial (Obligatorio)
Para que Kepler use la IA de Google Gemini, necesitas configurar tu API Key:

1. Obtén una API Key en Google AI Studio: https://aistudio.google.com/app/apikey.
2. En tu terminal ejecuta:
    ```bash
    kepler config --set-key
    ```
3. Pega la clave cuando se te solicite (la entrada está oculta por seguridad).

### 4. Actualización
Para actualizar Kepler sin perder tu configuración, ejecuta:

```bash
kepler update
```

---

## 🛠️ Solución de Problemas y Notas Importantes

### 1. "kepler" no se reconoce como comando
Si después de instalarlo el comando no se encuentra, la carpeta Scripts de Python puede no estar en tu PATH.
- **Solución:** Localiza la carpeta de scripts de Python (por ejemplo `C:\Users\TU_USUARIO\AppData\Roaming\Python\Python3x\Scripts`) y añádela al PATH.

### 2. Conflictos con OneDrive y carpetas sincronizadas
Si trabajas dentro de OneDrive, Dropbox o Google Drive:
- **Bloqueo de archivos:** Estos servicios pueden bloquear el `.docx` durante la sincronización y provocar fallos al guardar.
- **Rutas largas:** OneDrive puede generar rutas demasiado largas que excedan el límite de Windows (260 caracteres).
- **Recomendación:** Ejecuta Kepler en proyectos ubicados en rutas locales como `C:\Proyectos\mi-repo`.

### 3. Error de almacenamiento seguro (Keyring)
Kepler guarda tu API Key en el Administrador de Credenciales de Windows para que no tengas que introducirla siempre.
- Si obtienes un error relacionado con `keyring`, asegúrate de tener permisos adecuados o define la clave en un archivo `.env` local:
    ```env
    GEMINI_API_KEY=tu_clave_aqui
    ```

### 4. Ejecución dentro de repositorios Git
Kepler debe ejecutarse dentro de un repositorio Git. Si la carpeta actual no contiene `.git`, el comando `generate` fallará porque no hay historial de commits que analizar.

---

## 🛠️ Para Desarrolladores (Instalación Local)
Si quieres contribuir o personalizar el comportamiento:

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

Luego usa comandos como:

```bash
cd tu-proyecto
generate
```

También puedes ejecutar configuraciones directamente:

```bash
kepler config --set-key
kepler config --output-path C:\Users\TuUsuario\Documents\Reports
```

Artefactos generados:

```bash
commits.json
reporte_<mes>_<año>.docx
```

Adiciones actuales relacionadas con la generación de informes:

- `config/config_impl.py`
- `service/word_service.py`

---

## 🔧 Desinstalación
Si deseas eliminar la configuración local y desinstalar el paquete, tienes dos opciones:

1. Usar el comando interactivo dentro del CLI:

```bash
kepler uninstall
```

Este comando ofrece opciones para eliminar la API key guardada, la caché de commits (`~/.kepler/commits.json`), los reportes generados y, opcionalmente, ejecutar `pip uninstall kepler-cli`.

2. Desinstalación manual:

```bash
pip uninstall kepler-cli
# y, si deseas limpiar la configuración local:
rm -rf ~/.kepler
```

Ten cuidado al eliminar `~/.kepler`, ya que contiene las opciones persistentes y la caché de commits.

## 📌 Notas

- La CLI solo ejecuta **comandos seguros de solo lectura**
- No se modifican archivos fuente
- Funciona mejor dentro de un repositorio Git

---

## 🔮 Planes Futuros

- Soporte multilenguaje
- Mejor UX en terminal (autocompletado, historial)
- Cambiar modelos de IA
- Generar y enviar informes por correo

---

## 👨‍💻 Autor

Creado por Froggap 🚀

---

## 📄 Licencia

MIT License © 2026 Froggap

Libre para usar, modificar y distribuir con atribución.
