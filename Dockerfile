# Basis-Image mit Python 3.11
FROM python:3.11-slim

# Arbeitsverzeichnis festlegen
WORKDIR /app

# PYTHONPATH setzen
ENV PYTHONPATH=/app

# Kopiere requirements.txt und installiere Abhängigkeiten
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Kopiere den gesamten Code in das Image
COPY . .

# Starte die Anwendung
CMD ["python", "main.py"]
