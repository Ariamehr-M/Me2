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


📁 Project Structure
pgsql
Copy
Edit
me2/
├── main.py              ← FastAPI app + routes
├── models.py            ← SQLAlchemy models
├── schemas.py           ← Pydantic request / response models
├── questions.json       ← 14 static survey questions
├── templates/           ← Jinja2 HTML files
│   ├── landing.html
│   ├── signup.html
│   ├── survey.html
│   ├── result.html
│   ├── history.html
│   └── admin.html
├── static/              ← optional CSS / images
├── tests/               ← pytest + HTTPX happy‑path tests
├── requirements.txt
└── README.md
🔑 Environment Variables (.env)
Var	Default	Description
SESSION_SECRET	change_me	secret key for session cookies
DATABASE_URL	sqlite:///me2.db	override to Postgres if desired

📚 API Overview
Method & Path	Purpose
POST /auth/register	create user and auto‑login
POST /auth/login , /auth/logout	session management
POST /pairs	create pair + save A answers (transaction)
GET /pairs/{invite_token}	preview invite
POST /responses	save answers (with invite_token or pair_id)
GET /responses/pair/{id}/overlap	show matches (pair members only)
GET /pairs/{id}	status = pending / complete
/admin/*	dashboards (admin flag)

See docs/openapi.json after running server for full schema.

🧪  Running Tests
bash
Copy
Edit
pytest -q
Runs unit + integration tests for happy‑path: register → create pair → second user → match.

🛣️ Roadmap
 OAuth (Google / Apple)

 Email or Telegram notification when match completes

 React SPA front‑end

 Multi‑language survey

Feel free to open issues or PRs!

🤝 Contributing
Fork & clone

Create branch feature/your‑idea

Run black & ruff for formatting

Commit + PR

📜 License
MIT — see LICENSE.
