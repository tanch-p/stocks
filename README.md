# 📈 Stock Tracker & Alert System

A simple hobby project to track stock prices and send alerts when conditions are met.  
Built for personal learning and experimentation with [Python, FastAPI, Vue].

---

## 🚀 Features
- 🔍 **Track stocks** in real-time or with scheduled updates  
- 🔔 **Custom alerts** (price thresholds, percentage changes, moving averages, etc.)  
- 📊 **Dashboard/CLI view** to see current prices and performance  
- 💾 **Persistence** of watchlist and alert settings  
- 📩 **Notifications** via [email, Telegram, or other medium you used]  

---

## 🔑 Authentication & Login
- **User Accounts**: Each user can register with an email and password  
- **Authentication Method**: [e.g., JWT-based tokens / Session cookies]  
- **Password Security**: Passwords are hashed using [bcrypt/argon2/other] before storage  
- **Login Flow**:
  1. User enters email + password  
  2. Server validates credentials and issues an auth token/session  
  3. Token/session is required for protected routes (e.g., managing watchlists, creating alerts)  

- **Optional Features** (if implemented):
  - OAuth login (Google, GitHub, etc.)  
  - Multi-factor authentication (2FA)  
  - Rate limiting on login attempts to prevent brute-force  

---

## 🛠️ Tech Stack
- **Frontend**: [e.g., SvelteKit, React, or None if CLI only]  
- **Backend**: [e.g., Python (FastAPI/Flask)]  
- **Database/Storage**: [e.g., SQLite/Postgres/JSON file]  
- **APIs**: [e.g., Yahoo Finance API, Alpha Vantage]  

---

## 📂 Project Structure
project-root/
│── src/ # Source code
│── docs/ # Documentation files
│── config/ # Configurations (API keys, settings)
│── tests/ # Unit tests
│── README.md # Main documentation


---

## ⚡ How It Works
1. Add stocks to your **watchlist**  
2. Configure **alert rules** (e.g., notify me if AAPL < $150)  
3. Script/service fetches latest prices at intervals  
4. Notifications sent if conditions are triggered  

---

## 📸 Screenshots / Demo
*(Add images, GIFs, or console screenshots here)*

---

## 🙋 About
A personal hobby project to explore stock APIs, automation, and notification systems.
