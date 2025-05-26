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

---

## 🔐 Setup (Safe for Public Use)

### 1. Clone the repo

```bash
git clone https://github.com/ymu4/-EduFileUploader-.git
cd -EduFileUploader-
``` 

### 3. Install dependencies:
```bash
pip install -r requirements.txt
```

### 3.Create a .env file:
```bash

BOT_TOKEN=your-bot-token
CHANNEL_ID=your-channel-id
WEBHOOK_URL=https://your-deployment-url
```
### 4. Run locally:
```bash

python bot.py
Use tools like ngrok for webhook testing.
```



## Deployment
This bot supports 
- Render,
- Railway,
- Fly.io,
- or Heroku via Procfile.

Webhook should point to:
```bash

https://<your-domain>/<BOT_TOKEN>
```
The / endpoint is used by UptimeRobot or similar services to check if the bot is alive.


Example Bot Flow
1- /start
2- Choose department
3- Choose course or search
4- Select year → semester
5- Input professor’s name
6- Upload document
7- Receive animated confirmation


 ## Supported File Types
- ✅ PDF, DOC, DOCX, TXT, ZIP
- ❌ Images, videos, and unsupported media are rejected

## 🛡 License
MIT License — free to use and modify.

## Author
**Sumaya Alhashmi**  
📧 y.mu4ll@gmail.com  
🔗 [GitHub](https://github.com/ymu4)










