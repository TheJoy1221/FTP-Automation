# 🔐 FTP Automation & Verification Script

This automation tool handles SFTP file transfers with full upload verification, logging, and credential management via environment variables.

---

## 🚀 Features

- 📦 Uploads files to SFTP servers securely.
- 🔑 Credentials loaded safely from environment variables (.env file).
- 🧾 Verifies uploaded files exist on remote server.
- 📊 Logs all upload attempts and statuses.
- 📂 Simple configuration via `.env.example`.

---

## 📂 Project Structure

```bash
ftp-automation/
│
├── src/
│   └── ftp_automation.py
│
├── .env.example
├── requirements.txt
├── README.md
├── LICENSE
└── .gitignore
