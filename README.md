# 🚀 Kepler CLI

A custom CLI tool to generate professional monthly work reports from your Git activity using AI.

---

## 📌 Description

Kepler CLI is a command-line tool designed to:

* Navigate your local file system safely
* Detect and work with Git repositories
* Extract commit history
* Transform commits into structured data (JSON)
* Generate monthly reports (future feature)
* Use AI to enhance and summarize development activity (in progress)

---

## ⚙️ Features

### ✅ Implemented

* Interactive CLI interface
* Custom command system
* Safe terminal command execution
* Directory navigation (`cd`, `ls`, `pwd`, etc.)
* Permission control for system access
* Git commit extraction (basic)
* JSON generation from commits

### 🚧 In Progress

* AI prompt generation
* Integration with AI model
* Automatic report generation (Word / PDF)
* Smart summaries of commits

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
├── cli/
│   ├── welcome.py
│   ├── commands.py
│   └── ...
├── utils/
│   └── config.py
├── main.py
├── requirements.txt
└── README.md
```

---

## 🧠 How It Works (Concept)

1. User navigates to a project directory
2. CLI detects Git repository
3. Extracts commit history
4. Converts commits into structured data
5. Sends data to AI model (planned)
6. Generates a professional report

---

## ⚡ Installation

```bash
# Clone repository
git clone https://github.com/Froggap/kepler-cli.git

# Enter project
cd kepler-cli

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

## ▶️ Usage

```bash
python main.py
```

Then use commands like:

```bash
cd your-project
generate
```

---

## 📌 Notes

* The CLI only executes **safe read-only commands**
* No files are modified
* Works best inside a Git repository

---

## 🔮 Future Plans

* AI-powered summaries of commits
* Export reports to Word / PDF
* Multi-language support
* Better terminal UX (autocomplete, history)

---

## 👨‍💻 Author

Built by Froggap 🚀

---

## 📄 License

MIT License
