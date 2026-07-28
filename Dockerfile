# Dockerfile pour l'application Streamlit Gantt
# Utilise Python 3.12 pour éviter les problèmes de compatibilité avec pandas/pillow

FROM python:3.12-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de l'application
COPY requirements.txt .
COPY main.py .
COPY config.py .
COPY gantt.py .
COPY ui.py .
COPY images/ ./images/
COPY old/ ./old/

# Installer les dépendances système nécessaires pour pillow (zlib, etc.)
RUN apt-get update && apt-get install -y \
    zlib1g-dev \
    libjpeg-dev \
    && rm -rf /var/lib/apt/lists/*

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Exposer le port de Streamlit (par défaut 8501)
EXPOSE 8501

# Commande pour lancer l'application
CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
