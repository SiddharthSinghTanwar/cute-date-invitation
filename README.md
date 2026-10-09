# Cute Date Invitation 💗 — Railway deployment

## What this project includes
- Five-step invitation flow with kitten photos.
- Django Admin-managed date ideas.
- Persistent completed response history in `DateResponse`.
- WhatsApp prefilled message; the visitor still taps Send.
- Downloadable `.ics` calendar invite.
- PostgreSQL support through `DATABASE_URL`, plus SQLite fallback for local development.

## Deploy to Railway
1. Push this folder to a GitHub repository. Do not commit secrets or a real `.env` file.
2. Create a Railway account at https://railway.com/ and create a new project from the GitHub repository.
3. Add a PostgreSQL database in the Railway project. Railway exposes a `DATABASE_URL` variable to services when you reference/link the Postgres service; verify it appears in the web service's Variables tab.
4. Set these variables for the Django web service:
   - `DJANGO_SECRET_KEY`: a long random secret value
   - `DEBUG`: `False`
   - `ALLOWED_HOSTS`: `your-app-domain.up.railway.app` (replace with the generated domain)
   - `CSRF_TRUSTED_ORIGINS`: `https://your-app-domain.up.railway.app` (replace with the generated domain)
   - `WHATSAPP_PHONE` is currently configured in `date_invite/config.py`; edit that file if needed before pushing.
5. In Railway, generate a public domain for the web service.
6. Wait for deployment. The start command automatically runs migrations, collects static assets, and starts Gunicorn.
7. Create the admin account from the Railway service shell using `python manage.py createsuperuser` (or use Railway's command/shell feature). Then open `/admin/` on your public domain.
8. Test all five pages, the WhatsApp draft, calendar download, and Admin's **Completed date responses** list.

## Local development
```powershell
python -m venv .venv
.venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
For local development, the app uses SQLite unless `DATABASE_URL` is set.

## Important
- Do not use a free sleeping web instance if you want it to feel consistently fast. Railway Hobby currently starts at $5/month with included usage credits; actual usage can exceed that, so check current pricing and set a usage limit if available.
- A public site is accessible to anyone with the URL. Keep `/admin/` protected by a strong password and do not expose the Django secret key.
- Response history persists in PostgreSQL only when `DATABASE_URL` points to the Railway Postgres service. Do not rely on SQLite files in an ephemeral deployment.
- The WhatsApp number and inviter sign-off are configured in `date_invite/config.py`.
