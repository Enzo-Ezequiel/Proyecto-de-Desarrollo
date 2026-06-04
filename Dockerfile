# Python 3.10 o superior
FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Usuario sin privilegios
RUN useradd --create-home --home-dir /home/appuser appuser

# Instalamos dependencias del sistema de forma segura
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl build-essential \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*

USER appuser

# Instalamos uv 
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Subcarpeta exclusiva para tu código
WORKDIR /home/appuser/app

# Actualizamos el PATH para encontrar uv y el entorno virtual
ENV PATH="/home/appuser/.local/bin:/home/appuser/app/.venv/bin:$PATH"

# Copia todo el código a la subcarpeta
COPY --chown=appuser:appuser . .

# Sincronizamos las dependencias
RUN uv sync

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]