ARG PYTHON_VERSION
FROM python:${PYTHON_VERSION}

# Install system dependencies including git
RUN apt-get update && apt-get install -y \
    curl \
    git \
    libpq-dev \
    gcc \
    && pip install psycopg2 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Verify git installation immediately after installation
RUN git --version

WORKDIR /dsec_dbt
COPY . /dsec_dbt
RUN pip install -r requirements.txt

# Final verification of git installation
RUN git --version && echo "Git is successfully installed"

ENTRYPOINT ["dbt"]