FROM apache/airflow:2.9.2

USER root
RUN groupadd -g 999 docker \
    && usermod -aG docker airflow

USER airflow
COPY requirements.txt .
RUN pip install -r requirements.txt