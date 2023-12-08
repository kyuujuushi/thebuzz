
FROM python:3.8-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
RUN python create_db.py
EXPOSE 80
ENV NAME project_env
CMD ["python", "app.py"]
