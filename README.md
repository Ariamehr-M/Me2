# Me2
Me-Too is a FastAPI/Tailwind app that lets two people privately see if they both want to advance their relationship. Research-based survey, double-consent reveal, magic-link auth, FastAPI backend, PostgreSQL DB,and admin stats. 

# Me2 — Risk‑Free Mutual Match Survey 💬✅

*“Too shy to ask? Me2 shows if it’s mutual—no risk.”*

Me2 is a web app that lets **two people** privately answer a short survey about their relationship.  
Only the answers they **both share** are revealed (e.g., *“Yes, let’s date”*), so nobody risks an awkward first move.

---

## ✨  Key Features
| Flow | What happens |
|------|--------------|
| **Answer** | User A fills 7 “Current Status” questions + optional 7 “Future Wishes”. |
| **Send link** | Backend creates a *Pair* (`invite_token`) and stores A’s answers in one transaction. |
| **Friend clicks** | Link `/survey?invite=TOKEN` takes User B to the same survey (sign‑up if needed). |
| **See match** | When B submits, Me2 compares answers and shows only the overlaps to both users. |

*Everything else (non‑matching answers) stays hidden forever.*

---

## ⚙️  Tech Stack
| Layer | Library |
|-------|---------|
| Backend | **FastAPI** + SQLAlchemy 2 |
| Auth    | Session cookie via `starlette.middleware.sessions`<br>`passlib[bcrypt]` password hashing |
| DB      | SQLite (easy to switch to Postgres) |
| Front‑end | Jinja2 templates, Tailwind CDN, glassmorphism UI |
| Dev / Tests | HTTPX, pytest |

---

## 🚀  Quick Start

```bash
# 1. clone
git clone https://github.com/<your‑user>/me2.git
cd me2

# 2. create venv
python -m venv venv && source venv/bin/activate   # on Windows: venv\Scripts\activate

# 3. install deps
pip install -r requirements.txt

# 4. copy env vars
cp .env.example .env            # then put your own SESSION_SECRET

# 5. run dev server
uvicorn main:app --reload

# open http://127.0.0.1:8000
