FROM python:3.10-alpine
LABEL maintainer="Hayk Davtyan <hayk@parosly.io>"
ENV TZ=UTC
WORKDIR /app
COPY . .
RUN python -m pip install --no-cache-dir -r requirements.txt
EXPOSE 5000
ENTRYPOINT ["python", "main.py"]