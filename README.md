Run locally:

1) Create .env with SMTP settings (same keys as server/.env.example)
2) Install deps: `pip install -r requirements.txt`
3) Start: `uvicorn backend.main:app --host 0.0.0.0 --port 3001 --reload`


