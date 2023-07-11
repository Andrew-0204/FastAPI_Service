FROM python:3.10.11
# Switch to root user
USER root
WORKDIR /fastapi-mongo
COPY ./setup.txt /fastapi-mongo/setup.txt
RUN pip install --no-cache-dir --upgrade -r /fastapi-mongo/setup.txt
COPY ./app /fastapi-mongo/app
EXPOSE 5001
CMD ["python", "app/main.py"]
