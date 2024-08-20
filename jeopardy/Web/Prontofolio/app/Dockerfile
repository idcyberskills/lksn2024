FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY . /app/

EXPOSE 5000

ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Run the application
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
