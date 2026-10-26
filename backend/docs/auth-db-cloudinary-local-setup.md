# Authentication, per-user sessions, and Cloudinary setup

These changes are on the `feature/auth-db-cloudinary` branch. They do not modify `main`.

## 1. Create the MySQL database

In MySQL Workbench or the MySQL shell, run:

```sql
CREATE DATABASE ai_job_copilot CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

Use a dedicated database user in local development rather than sharing database credentials.

## 2. Configure backend secrets

From the repository root:

```bash
cd backend
cp .env.example .env
```

Edit `backend/.env` with your MySQL username/password, a long random `JWT_SECRET_KEY`, your Cloudinary credentials, and the AI provider keys you already use. If your MySQL password contains URL-reserved characters, URL-encode it in `DATABASE_URL`.

Do not commit `.env` or paste Cloudinary API secrets into source code, GitHub issues, or chat.

## 3. Install and run the backend

Use the Python version supported by your existing AI dependencies (Python 3.11 is a sensible local choice):

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Run these commands from `backend/`. The app creates its SQLAlchemy tables on startup. Open http://127.0.0.1:8000/docs to test the APIs.

## 4. Run the frontend

In another terminal:

```bash
cd frontend
cp .env.example .env
npm install
npm run dev
```

Open the local URL printed by Vite. Create an account at `/login?mode=signup`, then log in. The frontend stores the access token in localStorage and sends it as a Bearer token.

## 5. Authentication endpoints

- `POST /auth/signup` — create account and receive an access token.
- `POST /auth/login` — verify credentials and receive an access token.
- `GET /auth/me` — return the authenticated user.
- `POST /resume/upload` — authenticated PDF upload to Cloudinary, text extraction, per-user database record, and user-scoped Chroma metadata.
- `POST /ats/analyze` — verifies that the resume session belongs to the authenticated user.
- `POST /interview/start`, `/interview/answer`, and `/interview/end` — authenticated, SQLAlchemy-persisted interview sessions owned by the current user.

## Important notes

- PDF resumes are stored in Cloudinary; MySQL stores their URL/public ID, owner, extracted text, and resume session ID. Chroma stores chunks with both `user_id` and `session_id` metadata so retrieval can be scoped.
- DOCX is intentionally rejected for analysis for now because the current parser only extracts PDF text. The upload UI accepts PDFs only.
- `Base.metadata.create_all` is suitable for this local feature branch. Use Alembic migrations before production schema changes.
- The AI endpoints still require valid Groq/Hugging Face configuration and model access. Authentication and storage do not remove those external requirements.
- Do not expose Cloudinary API secrets in frontend environment variables; only backend environment variables may contain them.
- The repository previously contained uploaded PDF resume files. They have been removed from this feature branch and remain ignored by the repository's existing ignore rules. Because they existed in Git history on `main`, deleting them from this branch does not erase historical copies; consider rotating/revoking any sensitive links and removing those files from Git history if the repository is public.
