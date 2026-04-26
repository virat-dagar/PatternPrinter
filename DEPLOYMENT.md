# Deploy Pattern Printer

Pattern Printer is deployed as one Render web service. The Python backend serves both:

- the static frontend from `frontend/`
- the API routes under `/api/`

That means you do not need Vercel for this project.

## Render Settings

Use these settings if you create the service manually:

- Service type: Web Service
- Runtime: Python
- Build command: `python3 -m py_compile backend/server.py backend/patterns.py backend/cli.py`
- Start command: `python3 -m backend.server`
- Health check path: `/health`

The included `render.yaml` already contains these settings, so Render can also create the service from the Blueprint.

## Deploy Steps

1. Push this project to GitHub.
2. Open https://dashboard.render.com.
3. Click `New +`.
4. Choose `Blueprint` if you want Render to read `render.yaml`, or choose `Web Service` to enter the settings manually.
5. Connect the GitHub repository.
6. If using a Blueprint, confirm the `pattern-printer` service.
7. If using a Web Service manually, enter the settings listed above.
8. Click `Deploy`.
9. Wait for the deploy log to show the service is live.
10. Open the generated `.onrender.com` URL.

Use that Render URL as the live project link on your resume.

## Local Commands

Run the web app:

```bash
python3 -m backend.server
```

Run the optional CLI:

```bash
python3 -m backend.cli
```
