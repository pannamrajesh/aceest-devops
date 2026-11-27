# ACEest Fitness - Flask app with CI/CD

[![CI](https://github.com/pannamrajesh/aceest-devops/actions/workflows/main.yml/badge.svg)](https://github.com/pannamrajesh/aceest-devops/actions/workflows/main.yml)
[![CodeQL](https://github.com/pannamrajesh/aceest-devops/actions/workflows/codeql.yml/badge.svg)](https://github.com/pannamrajesh/aceest-devops/actions/workflows/codeql.yml)

A small Flask API for gym programs and calorie targets. I mainly use it to practise a full DevOps setup around a simple app:
lint, tests, Docker, GitHub Actions, Jenkins and Kubernetes.

## API

| Method | Path | What it does |
|---|---|---|
| GET | `/` | dashboard page |
| GET | `/health` | health check (used by Docker, k8s probes and the smoke test) |
| GET | `/programs` | list of programs |
| GET | `/program/<name>` | workout + diet for one program |
| POST | `/calories` | `{"weight": 70, "program": "Fat Loss (FL)"}` -> daily calories |

`/calories` returns 400 for a missing/invalid body, an unknown program, or a weight that isn't a number between 0 and 500.

## Run locally

```bash
python -m venv .venv
.venv\Scripts\activate            # Linux/macOS: source .venv/bin/activate
pip install -r requirements-dev.txt
pytest
FLASK_DEBUG=1 python app.py       # http://127.0.0.1:5000
```

With Docker:

```bash
docker compose up --build         # http://localhost:5000
sh scripts/smoke_test.sh          # in another terminal
```

There's also a `Makefile` with the same commands (`make test`, `make docker-build`, `make smoke`).

## Pipelines

**GitHub Actions** (`.github/workflows/`)
- `main.yml`: flake8 -> pytest on Python 3.10/3.11/3.12 with a 90% coverage gate -> Docker build -> smoke test against the running container -> Trivy image scan
- `codeql.yml`: CodeQL security scan on push, PRs and weekly
- `release.yml`: pushing a tag like `v1.0.0` builds and publishes the image to `ghcr.io/pannamrajesh/aceest-devops`
- Dependabot keeps pip, Docker and Actions versions up to date

**Jenkins** (`Jenkinsfile`, written for a Windows agent)
- checkout -> venv setup -> lint -> tests (JUnit + coverage reports) -> Docker build tagged with the build number -> smoke test on port 5055 -> cleanup

## Docker image

- multi-stage build, `python:3.11-slim`
- runs as a non-root user with gunicorn (not the Flask dev server)
- built-in `HEALTHCHECK` on `/health`

## Kubernetes

```bash
kubectl apply -f k8s/deployment.yaml
kubectl port-forward svc/aceest-fitness 8080:80
```

2 replicas, readiness/liveness probes on `/health`, CPU/memory limits, non-root, read-only root filesystem.

## Project layout

```
app.py                  Flask app
templates/index.html    dashboard
tests/                  pytest suite
Dockerfile, .dockerignore, docker-compose.yml
Jenkinsfile
.github/workflows/      CI, CodeQL, release
k8s/                    deployment + service
scripts/smoke_test.sh   post-deploy checks
```

The `The code versions for DevOps Assignment/` folder keeps the earlier Tkinter versions of the app for reference.
