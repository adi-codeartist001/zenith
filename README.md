<div align="center">

# ⚡ ZENITH
### Elite Campus Collaboration Network

[![Live](https://img.shields.io/badge/🚀_Live-zenith--hca5.onrender.com-6366f1?style=for-the-badge)](https://zenith-hca5.onrender.com)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.1-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![Groq](https://img.shields.io/badge/Groq-LLaMA_3-FF6B35?style=for-the-badge)](https://groq.com)
[![Render](https://img.shields.io/badge/Deployed_on-Render-46E3B7?style=for-the-badge&logo=render&logoColor=white)](https://render.com)

*The AI-powered campus collaboration engine for the next generation of builders.*

**[🌐 Visit Live App](https://zenith-hca5.onrender.com)** · **[📋 Report Bug](https://github.com/adi-codeartist001/zenith/issues)** · **[✨ Request Feature](https://github.com/adi-codeartist001/zenith/issues)**

</div>

---

## 🎯 What is ZENITH?

ZENITH is a full-stack, AI-powered campus collaboration platform built exclusively for **GLA University** students. It replaces random group formation with an intelligent discovery engine — matching students to projects and collaborators based on skills, niche, and AI-computed compatibility scores.

Students explore themed **Worlds**, discover open projects with **AI match scores**, join or propose initiatives, connect with **AI vibe-matched collaborators**, and track their growth through an **XP & levelling system**.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🌍 **Themed Worlds** | Navigate projects by domain — Tech Hub, Creative Studio, Research Lab, Economy & Trade |
| 🤖 **AI Project Matching** | Groq LLaMA 3 computes a 60-99% match score between your skills and each project |
| ✨ **AI Project DNA** | Auto-generates punchy taglines and skill tags when you propose a project |
| 🎯 **Vibe Match** | AI scores collaborator compatibility with a 2-word descriptor (Tech Twins, Creative Sync) |
| ⚡ **XP & Levelling** | Earn XP for joining (+50), proposing (+150), completing (+200), connecting (+20) |
| 🏆 **Rank System** | Progress from Initiate → Scholar → Innovator → Zenith Elite |
| 📡 **Pulse Feed** | Real-time activity feed showing live platform actions from all users |
| 🎙️ **Voice Narration** | ElevenLabs AI-generated voice narration on the landing page |
| 🎬 **Cinematic Landing** | Looping background video, cursor glow, animated floating icon stickers |
| 🏛️ **Archive Hall** | Completed projects showcased with a CONQUERED ribbon and XP earned |

---

## 🛠️ Tech Stack

### Backend
- **Python 3.11** — Core language
- **Flask 3.1** — Web framework for routing, sessions, and template rendering
- **SQLAlchemy** — ORM for database models and queries
- **SQLite** — File-based persistent database (development)
- **Werkzeug** — PBKDF2 password hashing for secure authentication
- **Flask Sessions** — Cookie-based login state management

### AI Layer
- **Groq API** — LLaMA 3 8B model for all three AI features
- **Project DNA** — Auto-generates tagline + tags on project proposal
- **Match Scoring** — 60-99% skill-based project compatibility score
- **Vibe Matching** — Collaborator compatibility score + 2-word descriptor

### Frontend
- **Jinja2** — Server-side HTML templating engine
- **Custom CSS** — Dark glassmorphic design system, no Bootstrap dependency
- **Plus Jakarta Sans** — Primary typeface (Google Fonts)
- **Lucide Icons** — SVG icon library (unpkg CDN)
- **HTML5 Canvas** — Live node-network animation on landing page

### Infrastructure
- **Gunicorn** — Production WSGI server
- **Render** — Cloud PaaS deployment
- **Cloudinary** — CDN hosting for background video asset
- **ElevenLabs** — AI voice narration (Eleven Multilingual v2)

---

## 🗂️ Project Structure
zenith/
├── app.py                  # Flask backend — routes, models, AI functions
├── requirements.txt        # Python dependencies
├── Procfile               # Render deployment config
├── static/
│   ├── style.css          # Global dark glassmorphic design system
│   ├── script.js          # Cursor glow, sticker animations
│   ├── narration.mp3      # ElevenLabs AI voice narration
│   └── bg.mp4             # Cinematic background video
└── templates/
├── index.html         # Landing page
├── dashboard.html     # User dashboard with Pulse feed
├── worlds.html        # World directory with AI match scores
├── project_hub.html   # Per-world project browser
├── project_overview.html
├── propose_project.html
├── collaborators.html
├── my_projects.html
├── messages.html      # Pulse activity feed
├── archive.html       # Hall of Fame
├── login.html
├── register.html
├── niche.html         # 4-step onboarding
└── overview.html

---

## 🚀 Local Setup

```bash
# 1. Clone the repo
git clone https://github.com/adi-codeartist001/zenith.git
cd zenith

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set environment variables
export SECRET_KEY="your_secret_key"
export GROQ_API_KEY="your_groq_api_key"

# 5. Add media assets
# Place narration.mp3 and bg.mp4 in static/

# 6. Run
python app.py
# Open http://localhost:5000
```

---

## 🌐 Deployment

Deployed on **Render** via GitHub integration.

| Config | Value |
|---|---|
| Runtime | Python 3 |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `gunicorn app:app` |
| Environment Variables | `SECRET_KEY`, `GROQ_API_KEY` |

---

## 👥 Team

| Name | Role |
|---|---|
| **Aditya Srivastava** | Full-Stack Lead — Backend, AI Integration, Frontend Architecture |
| **Nandini Saraswat** | Frontend Development & UI Design |
| **Shatakshi Shukla** | Database Design & Testing |
| **Shrangika Agnihotri** | Documentation & Research |

*Built at GLA University, Mathura · B.Tech CSE (AI & Data Analytics) · 2025-26*

---

## 📄 License

This project is built for academic purposes at GLA University. All rights reserved © 2026 Team ZENITH.

---

<div align="center">

**[⚡ Launch ZENITH](https://zenith-hca5.onrender.com)**

*Reach Your Zenith.*

</div>
