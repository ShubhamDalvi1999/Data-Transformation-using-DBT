<h2 align="center">
  Welcome to Airflow DBT Project Project!
  <img src="https://media.giphy.com/media/hvRJCLFzcasrR4ia7z/giphy.gif" width="28">
</h2>
<!-- Intro  -->
<h3 align="center">
        <samp>&gt; Hey There!, I am
                <b><a target="_blank" href="https://yourwebsite.com">Shubham Dalvi</a></b>
        </samp>
</h3>

<p align="center"> 
  <samp>
    <br>
    「 I am a data engineer with a passion for big data, distributed computing, cloud solutions, and data visualization 」
    <br>
    <br>
  </samp>
</p>

<div align="center">
<a href="https://git.io/typing-svg"><img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&pause=1000&random=false&width=800&lines=Azure+Databricks+%7C+Delta+Lake+%7C+Key+Vault;ADLS+Gen2+%7C+SQL+Database+%7C+Power+BI;Python+%7C+Snowflake+%7C+Airflow+%7C+DBT;3+yrs+of+Professional+Experience+%7C+Data+Engineer+%40+Accenture;Passionate+Data+Engineer+" alt="Typing SVG" /></a>
</div>


<p align="center">
 <a href="https://www.linkedin.com/in/shubham-dalvi-21603316b" target="_blank">
  <img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="yourprofile"/>
 </a>
</p>
<br />

<!-- About Section -->
# About Me

<p>
 <img align="right" width="350" src="/assets/programmer.gif" alt="Coding gif" />
  
 ✌️ &emsp; Enjoy solving data problems <br/><br/>
 ❤️ &emsp; Passionate about big data technologies, cloud platforms, and data visualizations<br/><br/>
 📧 &emsp; Reach me: shubhamdworkmail@gmail.com<br/><br/>
</p>

<br/>


# Airflow DBT Project

A production-ready data pipeline using Apache Airflow and DBT for processing CFTC reports.

![image](https://github.com/user-attachments/assets/fc4842b6-7634-4514-a886-3eccc6f31022)

## Data Flow

```mermaid
graph TD
    A[External Data Sources] --> B[Data Ingestion Layer]
    B --> C[Raw Data Storage]
    C --> D[Data Transformation Layer]
    D --> E[Analytics Ready Data]

    subgraph External_APIs
        A1[CFTC Trading Reports API] --> A
        A2[EU Agriculture Price API] --> A
    end

    subgraph Ingestion_DAGs
        B1[CFTC Weekly Position Loader] --> B
        B2[Eurostat Price Loader] --> B
    end

    subgraph Raw_Storage
        C1[Raw Trading Positions] --> C
        C2[Raw Wheat Prices] --> C
    end

    subgraph DBT_Transformations
        D1[Refined Trading Report] --> D
        D2[Refined Price Data] --> D
    end

    style A fill:#f9f,stroke:#333,stroke-width:2px
    style B fill:#bbf,stroke:#333,stroke-width:2px
    style C fill:#dfd,stroke:#333,stroke-width:2px
    style D fill:#fdd,stroke:#333,stroke-width:2px
    style E fill:#dff,stroke:#333,stroke-width:2px
```

## Project Overview

This project implements an automated data pipeline that:
1. Ingests CFTC (Commodity Futures Trading Commission) report data
2. Processes and transforms the data using DBT
3. Runs data quality tests
4. Manages the entire workflow using Apache Airflow

## Architecture

- **Apache Airflow**: Orchestrates the entire data pipeline
- **DBT**: Handles data transformation and testing
- **PostgreSQL**: Stores both raw and transformed data
- **Docker**: Containerizes all services for consistent deployment



## Prerequisites

- Docker and Docker Compose
- Python 3.10 or higher
- Git

## Quick Start

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd Docker_Airflow_Postgres-main
   ```

2. Create and configure the `.env` file:
   ```bash
   cp .env.example .env
   # Edit .env with your configurations
   ```

3. Start the services:
   ```bash
   docker-compose up -d
   ```

4. Access Airflow UI:
   - URL: http://localhost:8080
   - Default credentials: airflow/airflow

## Configuration

### Environment Variables

Key environment variables in `.env`:
```
AIRFLOW_UID=50000
AIRFLOW_GID=0
PYTHON_VERSION=3.10
DB_HOST=postgres
DB_USER=airflow
DB_PASSWORD=airflow
DB_PORT=5432
DB_NAME=airflow
DB_SCHEMA=public
```

### Service Configuration

1. **Airflow Webserver**:
   - Optimized Gunicorn settings
   - Health checks enabled
   - Automatic restart on failure

2. **DBT Service**:
   - Custom Dockerfile with required dependencies
   - Git integration for package management
   - Standardized container naming

3. **PostgreSQL**:
   - Configured for optimal performance
   - Proper connection pooling
   - Health monitoring enabled

## Project Structure

```
.
├── Airflow/
│   ├── dags/                 # Airflow DAG definitions
│   └── logs/                 # Airflow logs
├── dsec_dbt/
│   ├── models/              # DBT transformation models
│   ├── tests/               # Data quality tests
│   └── dbt_project.yml      # DBT configuration
├── docker/                   # Docker configuration files
├── docs/                     # Project documentation
├── docker-compose.yml        # Service orchestration
└── README.md                # This file
```

## DAGs

1. **CFTC Report Loader** (`06_CFTC_Rreport_Loader.py`):
   - Ingests CFTC report data
   - Runs DBT transformations
   - Executes data quality tests
   - Scheduled to run weekly

## Logging Structure

The Airflow logs are organized in a hierarchical structure under the `Airflow/logs` directory:

```
Airflow/logs/
├── dag_id=<dag_name>/                    # Specific DAG logs
│   ├── run_id=<run_identifier>/          # Each DAG run
│   │   └── task_id=<task_name>/         # Individual task logs
│   └── ...
├── scheduler/                            # Scheduler logs
│   ├── YYYY-MM-DD/                      # Date-based logs
│   └── ...
├── dag_processor_manager/               # DAG processing logs
└── ...
```

### Log Types

1. **DAG Run Logs**:
   - Located in `dag_id=<dag_name>/run_id=<run_identifier>/`
   - Run IDs include both manual and scheduled runs
   - Format: `manual__YYYY-MM-DDTHHMMSS+0000` or `scheduled__YYYY-MM-DDTHHMMSS+0000`
   - Contains all task execution logs for that specific run

2. **Service Logs**:
   - **Scheduler**: Daily logs of task scheduling and DAG processing
   - **DAG Processor**: Logs related to DAG file processing
   - **Worker**: Task execution and resource usage (in worker container)

3. **Log Retention**:
   - Logs are retained based on configuration
   - Default retention period: 30 days
   - Configurable via environment variables

### Log Generation

1. **Task Execution Logs**:
   - Generated by the Airflow worker when executing tasks
   - Each task instance creates its own log file
   - Captures:
     ```
     - Task start/end times
     - Python stdout/stderr output
     - Custom log messages from task code
     - Error tracebacks
     - Operator-specific information (e.g., SQL queries, DBT output)
     ```

2. **Scheduler Logs**:
   - Generated by the Airflow scheduler process
   - Created in daily rotating files
   - Records:
     ```
     - DAG file processing events
     - Task scheduling decisions
     - Task state transitions
     - Retry attempts
     - Scheduler heartbeat information
     ```

3. **DAG Processor Logs**:
   - Generated when Airflow processes DAG files
   - Captures:
     ```
     - DAG parsing results
     - Import errors
     - DAG validation issues
     - File processing timing
     - Syntax errors in DAG files
     ```

4. **Worker Logs**:
   - Generated by Celery workers (in our case, Docker containers)
   - Contains:
     ```
     - Task execution environment details
     - Resource usage (CPU, memory)
     - Container-specific information
     - Connection pool status
     ```

### Log Generation Settings

Key settings that affect log generation:
```ini
# Logging level for different components
AIRFLOW__LOGGING__LOGGING_LEVEL=INFO          # General logging level
AIRFLOW__CELERY__WORKER_LOG_SERVER_PORT=8793  # Worker log server port

# Log format customization
AIRFLOW__LOGGING__LOG_FORMAT=[%%(asctime)s] {%%(filename)s:%%(lineno)d} %%(levelname)s - %%(message)s
AIRFLOW__LOGGING__SIMPLE_LOG_FORMAT=%%(asctime)s %%(levelname)s - %%(message)s

# Log handlers configuration
AIRFLOW__LOGGING__FAB_LOGGING_LEVEL=WARN      # Flask AppBuilder logging
AIRFLOW__LOGGING__PROCESSOR_LOG_FOLDER=/opt/airflow/logs/dag_processor_manager
```

### Log Handlers

1. **Task Handler**:
   ```python
   # Example from DAG
   @task(task_id='example_task')
   def example_task(**context):
       # Logs are automatically captured
       logging.info("Task started")
       # Task code here
       logging.error("Error occurred")
   ```

2. **Custom Logging**:
   ```python
   # In your DAG file
   from airflow.utils.log.logging_mixin import LoggingMixin

   class CustomOperator(LoggingMixin):
       def execute(self, context):
           self.log.info("Custom message")
           # Your operator code
   ```

### Accessing Logs

1. **Via Airflow UI**:
   - Navigate to DAG > Graph View
   - Click on task
   - Select "View Log"
   - Use log navigation to view different runs

2. **Via Docker Commands**:
   ```bash
   # View DAG task logs
   docker-compose logs airflow-worker
   
   # View scheduler logs
   docker-compose logs airflow-scheduler
   
   # View specific container logs
   docker-compose logs [service-name]
   ```

3. **Direct File Access**:
   ```bash
   # Access logs directory
   docker-compose exec airflow-worker ls -l /opt/airflow/logs/dag_id=<dag_name>
   
   # View specific run logs
   docker-compose exec airflow-worker ls -l /opt/airflow/logs/dag_id=<dag_name>/run_id=<run_id>
   ```

### Log Configuration

Key environment variables for logging:
```ini
AIRFLOW__LOGGING__BASE_LOG_FOLDER=/opt/airflow/logs
AIRFLOW__LOGGING__DAG_FILE_PROCESSOR_LOG_RETENTION_DAYS=30
AIRFLOW__LOGGING__LOGGING_LEVEL=INFO
```

## Troubleshooting

Common issues and solutions are documented in:
- `docs/debugging_steps.md`: Detailed debugging guide
- `docs/docker_commands.md`: Useful Docker commands

## Health Checks

All services include health checks:
- Airflow Webserver: Gunicorn process monitoring
- DBT: Git availability check
- PostgreSQL: Connection verification
- Redis: Ping check

## Best Practices

1. **Container Management**:
   - Use of health checks
   - Proper restart policies
   - Resource limits configured

2. **Network Configuration**:
   - Standardized network setup
   - Internal service discovery
   - Proper DNS resolution

3. **Resource Management**:
   - Memory limits configured
   - CPU allocation optimized
   - Disk space monitoring

4. **Error Handling**:
   - Comprehensive logging
   - Retry mechanisms
   - Proper cleanup procedures

## Contributing

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## License

[Your License Here]

## Support

For issues and questions:
- Check the debugging guide in `docs/debugging_steps.md`
- Review Docker commands in `docs/docker_commands.md`
- Submit an issue in the repository
