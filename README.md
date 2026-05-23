# 🧾 POS System 

A Point of Sale (POS) and Inventory Management System built with Python, designed with a modular architecture inspired by MVC principles.

---

## ✨ Key Features

- 📦 Inventory management (products, categories, stock control)
- 🛒 Fast POS sales system
- 📥 Purchases management
- 📊 Stock movement tracking
- 👥 Supplier management
- 🧠 Layered architecture (Controllers, Services, DAO, Models)
- 🖥️ Desktop GUI built with PySide6

---

## 🏗️ Project Structure

project/
├── controller/      # Application controllers
├── services/        # Business logic layer
├── dao/             # Data Access Layer
├── models/          # Database entities
├── ui/              # PySide6 user interface
├── database/        # DB connection & setup
├── main.py          # Application entry point

---

## 🛠️ Tech Stack

- Python 3.11+
- PySide6 (Desktop GUI)
- PostgreSQL
- python-dotenv

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/your_username/pos-system.git
cd pos-system
```
### 2. Create virtual environment
python -m venv venv
venv\Scripts\activate   # Windows

### 3. Install dependencies
pip install -r requirements.txt

## 🔐 Environment Variables

Create a .env file based on this example:

DB_HOST=localhost
DB_PORT=5432
DB_USER=your_user
DB_PASSWORD=your_password
DB_NAME=pos_database

## ▶️ Run the Application
python project/main.py

## 📦 Build Executable (.exe)

You can package the application using PyInstaller:

pyinstaller main.spec

## 👨‍💻 Author

Developed by Sebasthian Saldaña Pérez

Focused on:

Software architecture
Real-world inventory systems
Desktop application development

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

