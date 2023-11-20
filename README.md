# parma-analytics

[![Chore](https://github.com/la-famiglia-jst2324/parma-analytics/actions/workflows/chore.yml/badge.svg?branch=main)](https://github.com/la-famiglia-jst2324/parma-analytics/actions/workflows/chore.yml)
[![CI](https://github.com/la-famiglia-jst2324/parma-analytics/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/la-famiglia-jst2324/parma-analytics/actions/workflows/ci.yml)
[![Deploy](https://github.com/la-famiglia-jst2324/parma-analytics/actions/workflows/release.yml/badge.svg)](https://github.com/la-famiglia-jst2324/parma-analytics/actions/workflows/release.yml)
[![Major Tag](https://github.com/la-famiglia-jst2324/parma-analytics/actions/workflows/tag-major.yml/badge.svg)](https://github.com/la-famiglia-jst2324/parma-analytics/actions/workflows/tag-major.yml)

ParmaAI analytics repository providing data processing and inference.

## `parma-ai` architecture

### System's architecture

#### Overall Architecture

```mermaid
graph TD

        %% Subgraphs

    subgraph FrontendContainer[FRONTEND]
        Frontend[("Next.js<br>TypeScript")]
    end

    subgraph ApiBackendContainer[API BACKEND]
        ApiRestBackend[("Next.js<br>Node.js<br>TypeScript")]
        AuthUser(("Authentication<br>User Management"))
    end

    subgraph WebLayer[Web Layer]
        FrontendContainer
        ApiBackendContainer
    end

    subgraph DatabaseLayer[Database Layer]
        AnalyticsDatabase[("Analytics Database")]
        ProductionDatabase[("Production Database")]
        CrawlingDatabase[("Crawling Database")]
    end

    subgraph AnalyticsLayer[Analytics Layer]
        AnalyticsBackendContainer
    end

    subgraph AnalyticsBackendContainer[Analytics Backend]
        AnalyticsRestBackend[("Python Backend")]
        NotificationContainer
    end

    subgraph NotificationContainer[Notification Module]
        Slack
        Email
    end

    subgraph DataSourcingLayer[Data Sourcing Layer]
        DataSourcingContainer
        DataRetrievalModules
    end

    subgraph DataSourcingContainer[Data Sourcing Backend]
        DataRetrievalController[("Data Retrieval Controller")]
        NormalizationService[("Normalization Service")]
        MonitoringAndLoggingSystem[("Monitoring and Logging System")]
    end

    subgraph DataRetrievalModules[Data Retrieval Modules]
        Module1[("E.G. Hackernews Module")]
        Module2[("Linkedin Module")]
        Module3[("Reddit Module (Apify)")]
        ModuleN[("Nth Module")]
    end


        %% Links
    Users --> FrontendContainer
    FrontendContainer -->|REST| ApiRestBackend
    ApiRestBackend -->|SQL Framework| ProductionDatabase
    ProductionDatabase -->|Replicate| AnalyticsDatabase
    AnalyticsDev["Analytics<br>(Developers)"] --> AnalyticsDatabase
    AnalyticsRestBackend -->|SQL Framework| ProductionDatabase
    AnalyticsRestBackend --> NotificationContainer
    NotificationContainer --> ExternalNotificationProvider["External Notification Provider"]
    DataRetrievalController -->|SQL Framework| CrawlingDatabase
    ApiRestBackend -->|Trigger Run - REST| DataRetrievalController
    AnalyticsRestBackend -->|Trigger Run - REST| DataRetrievalController
    DataRetrievalController -->|Initiate| DataRetrievalModules
    DataRetrievalModules -->|Raw Data| DataRetrievalController
    DataRetrievalController -->|Raw Data| NormalizationService
    NormalizationService -->|Send Normalized Data - REST| AnalyticsRestBackend
    DataRetrievalModules --> MonitoringAndLoggingSystem
    MonitoringAndLoggingSystem -->|Send Monitoring Data - REST| AnalyticsRestBackend

        %% Link Styles
    linkStyle default stroke:#9E9D91,stroke-width:2px;
    %%linkStyle 5 stroke:#black,stroke-width:3px;
    %%linkStyle 9 stroke:#black,stroke-width:3px;
    %%linkStyle 10 stroke:#black,stroke-width:3px;
```

#### Process Flows

The parma ai backend consists of the following process flow:

```mermaid
graph LR
    subgraph parma-mining
        A[Data Mining] --> B[Data Preprocessing]
    end
    subgraph parma-mining-db
        B --> C[NoSQL Mining Database]
    end
    subgraph parma-analytics
        C --> D[Data Processing]
        D --> F[Data Analytics]
        F --> G[Data Inference]
        D --> H[Data Visualization]
        D --> I[Data Reporting / Alerting]
        H --> I
    end
    subgraph parma-prod-db
        D --> E[Data Storage]
        G --> E
    end
    subgraph parma-web
        E --> J[REST API]
        J --> K[Frontend]
    end

```

### `parma-analytics` architecture

```mermaid
graph LR
    subgraph parma_analytics
        subgraph .
            subgraph api
                models
                routes
            end
            subgraph db.mining
            end
            subgraph etl
            end
            subgraph analytics
                subgraph inference
                end
                subgraph visualization
                end
            end
            subgraph reporting
                subgraph slack
                end
                subgraph gmail
                end
            end
            subgraph db.prod
            end
            api -.-> db.mining
            db.mining -.-> etl
            etl -.-> analytics
            analytics -.-> reporting
            analytics -.-> db.prod
        end
        bl[bl=business logic] <--> api
        bl <--> db.mining
        bl <--> etl
        bl <--> analytics
        bl <--> reporting
        bl <--> db.prod
    end
```

### `parma-analytics` data model

```mermaid
erDiagram
    BUCKET ||--o{ COMPANY_BUCKET_MEMBERSHIP : ""
    BUCKET ||--o{ BUCKET_ACCESS : ""
    COMPANY ||--o{ COMPANY_BUCKET_MEMBERSHIP : ""
    COMPANY ||--o{ NOTIFICATION_SUBSCRIPTION : "has"
    COMPANY ||--o{ REPORT_SUBSCRIPTION : ""
    COMPANY ||--o{ COMPANY_ATTACHMENT : "has"
    COMPANY ||--o{ NOTIFICATION : ""
    COMPANY ||--o{ COMPANY_DATA_SOURCE : ""
    COMPANY ||--|| DATA_SOURCE_MEASUREMENT_NEWS_SUBSCRIPTION :""
    DATA_SOURCE ||--o{ COMPANY_DATA_SOURCE : ""
    DATA_SOURCE ||--o{ SOURCE_MEASUREMENT : ""
    DATA_SOURCE ||--o{ NOTIFICATION : ""
    DATA_SOURCE ||--|| USER_IMPORTANT_MEASUREMENT_PREFERENCE : ""
    NOTIFICATION_SUBSCRIPTION ||--o{ NOTIFICATION_CHANNEL : ""
    REPORT ||--o{ COMPANY : "contains"
    REPORT_SUBSCRIPTION ||--o{ NOTIFICATION_CHANNEL : ""
    USER ||--o{ USER_IMPORTANT_MEASUREMENT_PREFERENCE : "chooses"
    USER ||--o{ NOTIFICATION_SUBSCRIPTION : ""
    USER ||--|| REPORT_SUBSCRIPTION : ""
    USER ||--o{ COMPANY : "subscribes"
    USER ||--o{ BUCKET_ACCESS : "has"
    USER ||--|| DATA_SOURCE_MEASUREMENT_NEWS_SUBSCRIPTION :""
    USER ||--o{ COMPANY_ATTACHMENT : "attaches"
    SOURCE_MEASUREMENT ||--o{ MEASUREMENT_TEXT_VALUE : ""
    SOURCE_MEASUREMENT ||--o{ MEASUREMENT_INT_VALUE : ""
    BUCKET {
        uuid id PK
        string title
        string description
        boolean is_public
        uuid owner_id FK
        string created_at
    }
    BUCKET_ACCESS{
        uuid id PK,FK
        uuid invitee_id PK,FK
        tbd  permission
    }
    COMPANY {
        uuid id PK
        string name
        string description
        uuid added_by FK
    }
    COMPANY_ATTACHMENT {
        uuid id PK
        uuid company_id FK
        string file_type
        string file_url
        uuid user_id FK
        string title
        date created_at
    }
    COMPANY_BUCKET_MEMBERSHIP{
        uuid bucket_id PK,FK
        uuid company_id PK,FK
    }
    COMPANY_DATA_SOURCE {
        uuid data_source_id PK, FK
        uuid company_id PK, FK
        string frequency
        boolean is_data_source_active
        string health_status
    }
    DATA_SOURCE {
        uuid source_module_id PK
        string source_name
        boolean is_active
        string default_frequency
        string health_status
    }
    DATA_SOURCE_MEASUREMENT_NEWS_SUBSCRIPTION{
        uuid id PK
        uuid user_id FK
        uuid company_id FK
    }
    NOTIFICATION {
        uuid id PK
        string message
        uuid company_id FK
        uuid data_source_id FK
        date timestamp
    }
    NOTIFICATION_CHANNEL {
        uuid channel_id PK, FK
        uuid entity_id FK
        string entity_type
        string channel_type
        string destination
    }
    NOTIFICATION_SUBSCRIPTION {
        uuid user_id FK, PK
        uuid company_id FK, PK
        uuid channel_id FK, PK
    }
    REPORT{
        uuid id PK
        string name
        date timestamp
        blob content
        uuid company_id FK
    }
    REPORT_SUBSCRIPTION {
        uuid user_id FK, PK
        uuid company_id FK, PK
        uuid channel_id FK, PK
    }
    SOURCE_MEASUREMENT {
        uuid source_measurement_id PK
        uuid source_module_id FK
        string type
        string measurement_name
    }
    USER {
        uuid id PK
        string name
        string role
    }
    USER_IMPORTANT_MEASUREMENT_PREFERENCE {
        uuid data_source_id PK, FK
        uuid user_id PK, FK
        string important_field_name
    }
    MEASUREMENT_TEXT_VALUE {
        id measurement_value_id PK
        id source_measurement_id FK
        timestamp timestamp
        string value
    }
    MEASUREMENT_INT_VALUE {
        id measurement_value_id PK
        id source_measurement_id FK
        timestamp timestamp
        int value
    }
```

## Getting Started

The following steps will get you started with the project.

> **NOTE**: Although the general steps should also work on a Windows, we highly recommend to use a Linux based machine for development. WSL is also an option. Use Windows at your own risk.

1. Pre-requisites: to be able to contribute to JST in this repository, make sure to comply with the following prerequisites.

   - Configure GitHub via an ssh key. Key based authenticated is highly encouraged. See [GitHub Docs](https://docs.github.com/en/github/authenticating-to-github/connecting-to-github-with-ssh) for more information.
   - Please make sure to have an GPG key configured for GitHub. See [GitHub Docs](https://docs.github.com/en/authentication/managing-commit-signature-verification/adding-a-gpg-key-to-your-github-account) for more information.
   - Install **micromamba**, a conda environment management package manager, as described [here](https://mamba.readthedocs.io/en/latest/micromamba-installation.html). Alternatively conda or mamba installations should also work, but are highly discouraged because of their slow performance.
   - Install docker and docker-compose. See [Docker Docs](https://docs.docker.com/get-docker/) for more information.

2. **Clone the repository**

   ```bash
   git@github.com:la-famiglia-jst2324/parma-analytics.git
   ```

3. **Precommit & environment setup**:

   ```bash
   # spinning up the database container for local development
   docker-compose up -d

   make install
   ```

4. Activating the environment:

   ```bash
    # Activate the new environment (do this every time you start a new terminal)
    # fyi. there are IDE extensions to automatically activate the environment
    micromamba activate parma-analytics

    # do the following only once
    pip install -e . # Install the project in editable mode
    pre-commit install
   ```

5. Export environment variables for the database:

   ```bash
   # fyi. there are IDE extensions to automatically load
   # environment variables from a .env file
   export POSTGRES_HOST=localhost
   export POSTGRES_PORT=9000
   export POSTGRES_USER=parma-prod-db
   export POSTGRES_PASSWORD=parma-prod-db
   export POSTGRES_DB=parma-prod-db
   ```

6. **Start the api server**:

   ```bash
   make dev
   ```

   **Open [http://localhost:8000](http://localhost:8000) with your browser to see the result.**

   FastApi will provide you with an interactive documentation of the api. You can also use the swagger ui at [http://localhost:8000/docs](http://localhost:8000/docs) or the redoc ui at [http://localhost:8000/redoc](http://localhost:8000/redoc).

7. Optional: Running the pre-commit pipeline manually

   ```bash
   pre-commit run --all
   ```

8. Test your code:

   ```bash
   make test
   ```

## PR workflow

1. **Create a new branch**
   [linear.app](linear.app) offers a button to copy branch names from tickets.
   In case there is no ticket, please use feel free to use an arbitrary name or create a ticket.
   GitHub CI doesn't care about the branch name, only the PR title matters.

   ```bash
   # format: e.g. robinholzingr/meta-1-create-archtecture-drafts-diagrams-list-of-key-priorities
   git checkout -b <branch-name>
   ```

2. Open a PR and use a [conventional commit](https://www.conventionalcommits.org/en/v1.0.0/) PR title.

3. Wait for CI pipeline to pass and if you are happy with your changes request a review.

4. Merge the PR (using the "Squash and merge" option) and delete the branch.
   Pay attention to include co-authors if anyone else contributed to the PR.

5. If you want to release a new version to production, create a new release on GitHub.
   The release version will be automatically derived from the PR titles
   (breaking changes yield new major versions, new features yield new minor versions).

### Directory structure

```bash
.
├── parma_analytics: Main package for analytics backend
│   ├── analytics: subpackage for main analytical tasks
│   │   ├── inference: subpackage for custom models and inference
│   │   └── visualization
│   ├── api
│   │   ├── README.md: Guidelines for api design
│   │   ├── main.py: Api entrypoint for fastapi
│   │   ├── models: pydantic models for api
│   │   │   ├── README.md: Guidelines for pydantic models
│   │   │   └── dummy.py: Example pydantic models
│   │   └── routes: api routes for fastapi
│   │       └── dummy.py: Example api routes
│   ├── bl: Business logic for analytics backend
│   ├── db: Database subpackage
│   │   ├── mining: subpackage for mining database
│   │   └── prod: subpackage for production database
│   │       ├── README.md
│   │       ├── dummy.py: Example database connectors
│   │       ├── engine.py: Database engine utility
│   │       ├── models: Database models
│   │       │   ├── README.md: Guidelines for database models
│   │       │   ├── base.py: Base database model
│   │       │   └── dummy.py: Example database models
│   │       └── utils: Database utilities
│   │           └── paginate.py: Pagination utility
│   ├── etl: Data processing subpackage
│   └── reporting: Reporting subpackage
│       ├── gmail: subpackage for gmail reporting
│       └── slack: subpackage for slack reporting
├─ tests:
│   ├── analytics
│   │   ├── inference
│   │   └── visualization
│   ├── api
│   ├── db
│   ├── etl
│   ├── reporting
│   │   ├── gmail
│   │   └── slack
│   └── test_dummy.py
├── Makefile: Recipes for easy simplified setup and local development
├── README.md
├── docker-compose.yml: Docker compose file for local database
├── environment.yml: conda environment file
├── pyproject.toml: Python project configuration file
```

## Tech Stack

Core libraries that this project uses:

- [FastAPI](https://fastapi.tiangolo.com/): FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python type hints.
- [SQLAlchemy](https://www.sqlalchemy.org/): SQLAlchemy is the Python SQL toolkit and Object Relational Mapper that gives application developers the full power and flexibility of SQL.
- [Alembic](https://alembic.sqlalchemy.org/en/latest/): Alembic is a lightweight database migration tool for usage with the SQLAlchemy Database Toolkit for Python.
- [Pydantic](https://pydantic-docs.helpmanual.io/): Data validation and settings management using python type annotations.
- [Typer](https://typer.tiangolo.com/): Typer is a library for building CLI applications that users will love using and developers will love creating.
- [Polars](https://pola.rs): Polars is a blazingly fast data processing library written in Rust. It has a DataFrame API that is similar to Pandas and a Series API that is similar to NumPy.
- [Pytest](https://docs.pytest.org/en/6.2.x/): The pytest framework makes it easy to write small tests, yet scales to support complex functional testing for applications and libraries.
- **ML**: For potential ML tasks we will start off with sklearn and lightgbm. If we need more complex models we will switch to pytorch or tensorflow.

## Deployment

No deployment pipeline has been set up yet.

Currently we are considering several backend frameworks like `Firebase`, `Supabase` or `AWS Amplify`.

## Disclaimer

In case there are any issues with the initial setup or important architectural decisions/integrations missing, please contact the meta team or @robinholzi directly.
