# ⚡ ZENITH — Elite Campus Collaboration Network

> *Reach Your Zenith. Build Together.*

ZENITH is a full-stack, AI-assisted campus collaboration platform built for GLA University students. Discover projects, join teams, propose initiatives, and connect with skill-matched collaborators — all in one dark, glassmorphic web app.

---

## 🚀 Features

- 🔐 **Real Authentication** — bcrypt-hashed passwords, session-based login/logout
- 🌍 **Worlds Directory** — Browse projects by domain: Tech Hub, Creative Studio, Research Lab, Economy & Trade
- 🤖 **AI-Powered Matching** — Smart project taglines, skill tags, and collaborator vibe-match scores
- 📊 **XP & Levelling System** — Earn XP by joining projects, connecting with collaborators, and completing missions
- 🗂️ **Full Project Lifecycle** — Create → Join → Track Progress → Archive
- 📡 **Live Pulse Feed** — Real-time activity log of platform actions
- 🏆 **Hall of Fame Archive** — Completed projects with CONQUERED ribbon

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3, Flask |
| Database | SQLite via Flask-SQLAlchemy |
| Auth | Werkzeug (bcrypt) |
| Frontend | Jinja2, Bootstrap 5.3, Custom CSS |
| Icons | Lucide Icons (CDN) |
| Fonts | Plus Jakarta Sans, Space Grotesk |
| Deployment | Gunicorn, Render |

---

## 📁 Project Structure

```
zenith_upgraded/
├── app.py                    # Flask app — all routes, models, AI helpers
├── requirements.txt          # Python dependencies
├── Procfile                  # Gunicorn deployment config
├── instance/
│   └── zenith.db             # SQLite database (auto-created)
├── static/
│   ├── style.css             # Glassmorphic shared styles
│   ├── script.js             # Landing page & dashboard JS
│   ├── bg.mp4                # Background video
│   └── narration.mp3         # Audio asset
└── templates/
    ├── index.html            # Landing page
    ├── overview.html         # Platform intro
    ├── login.html            # Login
    ├── register.html         # Registration
    ├── niche.html            # Niche onboarding
    ├── dashboard.html        # User dashboard
    ├── worlds.html           # Worlds directory
    ├── project_hub.html      # Per-world project listing
    ├── projects.html         # Per-niche project browser
    ├── project_overview.html # Project detail + join
    ├── propose_project.html  # Create new project
    ├── my_projects.html      # Authored & joined projects
    ├── collaborators.html    # AI-matched collaborators
    ├── archive.html          # Completed projects
    └── messages.html         # Pulse activity feed
```

---

## ⚙️ Local Setup

```bash
# 1. Clone the repo
git clone https://github.com/your-username/zenith.git
cd zenith

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate      # Mac/Linux
venv\Scripts\activate         # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
python app.py
```

Open **http://localhost:5000** in your browser. The SQLite database is created automatically on first run.

---

## 🌐 Deployment on Render

1. Push your code to GitHub
2. Go to [render.com](https://render.com) → **New Web Service** → connect your repo
3. Set the following:

| Field | Value |
|---|---|
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn app:app` |
| **Environment** | Python 3 |

4. Add these environment variables in the Render dashboard:

| Variable | Description |
|---|---|
| `SECRET_KEY` | Any long random string for Flask sessions |
| `GROQ_API_KEY` | Required for AI features (taglines, match scores) |

5. Hit **Deploy** — Render handles the rest.

---

## 👥 Team

| Name 
| Aditya Srivastava 
| Nandini Saraswat 
| Shatakshi Shukla
| Shrangika Agnihotri 

**Under the guidance of:** Faculty Mentor, Department of CSE
**Institution:** GLA University, Mathura
**Academic Year:** 2025–2026

---

<p align="center">Built with 💜 by Team ZENITH — GLA University</p>
