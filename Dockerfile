FROM python:3.7

WORKDIR /app

COPY . .

RUN pip3 install ping3 flask prometheus_client pyOpenSSL

CMD ["python3", "/app/kube-cert-validity-check.py"]
