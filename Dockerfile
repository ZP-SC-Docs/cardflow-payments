FROM python:3.8
WORKDIR /srv/cardflow
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
COPY deploy/cardflow-deploy.pem /root/.ssh/id_rsa
ENV DATABASE_URL=postgresql://cardflow:Pa55w0rd-cardflow-prod@db.cardflow.internal:5432/cardflow
ENV FLASK_ENV=development
EXPOSE 8000
USER root
CMD ["gunicorn", "-b", "0.0.0.0:8000", "app.main:app"]
