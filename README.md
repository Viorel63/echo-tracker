# 📌 Echo Tracker

A lightweight, self-hosted issue tracking system built with **Flask**, **SQLAlchemy**, and a clean HTML interface.

---

## 🚀 Features

- 🐞 Create, view, and filter issues  
- 👤 Assign users by ID  
- 🔍 Sort by status, priority, or creation date  
- 📅 Filter by date range  
- 🧭 REST API + HTML interface  
- 📦 Pagination and direction control  

---

* 📁 Project Structure
* echo-tracker/
* ├── app/
* │     ├── models.py
* │     ├── routes/
* │     ├── templates/
* │     └── extensions.py
* ├── migrations/
* ├── config.py
* ├── run.py
* ├── requirements.txt
* ├── README.md
* └── .gitignore

🧠 Notes

Default status: Open

Default priority: Low

Assignee ID is optional

Filters persist across sessions

## ⚙️ Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Run the app
flask --app run.py run
