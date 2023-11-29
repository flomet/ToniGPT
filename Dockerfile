# From a shell in the folder where this Dockerfile is stored: 
# Build Container: 
# docker build -t tonigpt .

# Run Container: 
#docker run -p 5000:5000 -v /root/ToniGPT_Stories:/app/stories -d tonigpt
# Synology 
#sudo docker run -p 5320:5000 -v /volume1/share/docker/ToniGPT_Stories:/app/stories -d tonigpt

# Verwende das offizielle Python-Image als Basis
FROM python:3.10.13-bookworm

# Setze das Arbeitsverzeichnis innerhalb des Containers
WORKDIR /app

# Create a directory within the container
RUN mkdir -p /app/stories

# Mount a host directory to /app/stories
VOLUME /app/stories

# Kopiere die Anforderungen (requirements.txt) in das Arbeitsverzeichnis
COPY requirements.txt .

# Installiere die Python-Abhängigkeiten
RUN pip install -r requirements.txt

# Kopiere den gesamten Code in das Arbeitsverzeichnis des Containers
COPY . .

# Exponiere den Port, den deine Flask-Anwendung verwendet (Standardport 5000)
EXPOSE 5000

# Definiere eine Umgebungsvariable für das Verzeichnis mit den Geschichten
ENV STORIES_DIR="/app/stories"

# configure the container to run in an executed manner
ENTRYPOINT [ "python" ]

CMD ["tonigpt_app.py" ]
