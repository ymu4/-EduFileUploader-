# 📚 EduFileUploader – Telegram Bot for Academic File Sharing

**EduFileUploader** is a Telegram bot that allows university students to upload course-related documents (PDF, DOC, ZIP, etc.) in a structured flow by selecting the department, course, year, semester, and professor. The files are then automatically sent to a designated Telegram channel.

---

## 🚀 Features

- Department & course selection via inline buttons
- Smart course search (e.g., CSBP119, MATH105)
- Year & semester selection
- Professor name input with validation
- Upload documents (PDF, DOC, DOCX, TXT, ZIP)
- Sends uploaded file to a Telegram channel
- Thank-you animation on successful upload
- Webhook + /ping & / endpoints for health monitoring

---

## 🛠 Built With

- Python 3
- [python-telegram-bot v20+](https://github.com/python-telegram-bot/python-telegram-bot)
- aiohttp (webhook support)
- asyncio for asynchronous logic

---

## 🧾 Project Structure


├── bot.py # Main bot logic

├── requirements.txt # Python dependencies

├── Procfile # For deployment (e.g., Render/Heroku)

└── README.md # You're reading it!


---

## 🔐 Setup (Safe for Public Use)

1. Clone the repo:
   
git clone https://github.com/ymu4/-EduFileUploader-.git
cd -EduFileUploader-


3. Install dependencies:
   
pip install -r requirements.txt


3.Create a .env file:

BOT_TOKEN=your-bot-token
CHANNEL_ID=your-channel-id
WEBHOOK_URL=https://your-deployment-url

4. Run locally:
python bot.py
Use tools like ngrok for webhook testing.



Deployment
This bot supports Render, Railway, Fly.io, or Heroku via Procfile.

Webhook should point to:
https://<your-domain>/<BOT_TOKEN>

The / endpoint is used by UptimeRobot or similar services to check if the bot is alive.


Example Bot Flow
/start

Choose department

Choose course or search

Select year → semester

Input professor’s name

Upload document

Receive animated confirmation


 Supported File Types
✅ PDF, DOC, DOCX, TXT, ZIP

❌ Images, videos, and unsupported media are rejected






