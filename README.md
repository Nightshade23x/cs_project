# Django Web Security Lab

An intentionally insecure Django notes application used to demonstrate common web security mistakes and their mitigations, based on the OWASP Top 10. The repository includes a written report (`Essay.md`) documenting vulnerabilities, impacts and suggested corrections.

> **Security warning:** The application deliberately contains exploitable vulnerabilities. Run it only in an isolated local environment using dummy data. Do **not** deploy it to the internet or use real credentials.

## Vulnerabilities demonstrated

- Broken object-level access control when retrieving notes.
- SQL injection through dynamically interpolated search queries.
- Authentication bypass due to missing password validation.
- Exposure of application settings and secret material via a debug route.
- Incorrect password storage during user registration.

The report also discusses authorization and design risks around administrative functionality. See [Essay.md](Essay.md) for the original explanations and example fixes.

## Tech stack

Python, Django, SQLite and Django templates.

## Local setup

```powershell
git clone https://github.com/Nightshade23x/cs_project.git
cd cs_project
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

The insecure notes routes are under `http://127.0.0.1:8000/notes/`.

## Structure

- `notes/views.py` — deliberately vulnerable endpoints and commented secure alternatives.
- `notes/urls.py` — note, search, login, registration and debug routes.
- `cs_project/` — Django settings and configuration.
- `screenshots/` — before/after examples.
- `Essay.md` — detailed security analysis.

## Reminder

Fixing an individual example does not make the entire application production-ready. The repository is intended for controlled security education.
