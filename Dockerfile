FROM python:3.12
WORKDIR /app
COPY requirements.txt /app
RUN pip3 install -r /app/requirements.txt --no-cache-dir
COPY /api_yamdb /app
COPY entrypoint.sh /app
RUN chmod +x /app/entrypoint.sh
# ENTRYPOINT [ "/app/entrypoint.sh" ]
# CMD ["gunicorn", "api_yamdb.wsgi:application", "--bind", "0:8000"]