# ---- build stage: install dependencies into a virtualenv ----
FROM python:3.11-slim AS build
WORKDIR /app
RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ---- runtime stage: small image, non-root user ----
FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/venv/bin:$PATH" \
    PORT=5000
WORKDIR /app
RUN useradd --create-home --uid 10001 appuser
COPY --from=build /venv /venv
COPY app.py .
COPY templates/ templates/
USER appuser
EXPOSE 5000
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request,os; urllib.request.urlopen(f'http://127.0.0.1:{os.environ[\"PORT\"]}/health', timeout=2)" || exit 1
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${PORT} --workers 2 --access-logfile - app:app"]
