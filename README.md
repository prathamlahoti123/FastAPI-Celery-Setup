# FastAPI + Celery + Flower Example with Docker Compose

![Pytest](https://github.com/pypa/hatch/actions/workflows/test.yml/badge.svg)
[![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)
[![Linter Ruff](https://img.shields.io/badge/Linter-Ruff-brightgreen)](https://github.com/charliermarsh/ruff)

This project demonstrates how to integrate **FastAPI** with **Celery** for running background tasks, using **Redis** as both the broker and result backend. The stack also includes **Flower** for monitoring task execution. The entire setup is containerized using the **Docker Compose plugin**.

<p align="center">
  <img src="https://i.ibb.co/6VCXmzc/1.jpg" width="600" height="600" alt="Workflow Diagram" />
</p>


## Technical Stack

* Docker
* Docker Compose (plugin)
* Python 3.12
* FastAPI 0.115
* Celery 5.5
* Flower 2.0
* Redis 6.2

## Project Structure

```bash
# Main app
├── app
│   ├── api
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── routes.py
│   │   ├── schemas.py
│   │   ├── settings.py
│   │   └── tasks.py
│   ├── Dockerfile
│   ├── pyproject.toml # config for Ruff and Mypy
│   ├── requirements.test.txt # base packages + packages for testing
│   ├── requirements.txt
│   ├── .dockerignore
│   ├── .env.example # config template for main app
│   ├── .gitignore
│   └── tests
│       ├── __init__.py
│       ├── conftest.py
│       └── test_routes.py
# Worker app
├── worker
    ├── app
    │   ├── __init__.py
    │   ├── main.py
    │   ├── settings.py
    │   └── tasks.py
    ├── Dockerfile
    ├── pyproject.toml # config for Ruff and Mypy
    ├── requirements.test.txt # base packages + packages for testing
    ├── requirements.txt
    ├── .dockerignore
    ├── .env.example # config template for worker app
    ├── .gitignore
    └── tests
        ├── conftest.py
        ├── __init__.py
        └── test_tasks.py
├── docker-compose.yml
├── .env.example # config for both main and worker apps
└── README.md
```


## Notes

- There must be a global <ins>.env</ins> file that shares configuration for both Both [app](app/) and [worker](worker/) apps. See [.env.example](.env.example)

- Both [app](app/) and [worker](worker/) apps have their own settings that must be set in the <ins>.env</ins> file of the corresponding directory.

- Both [app](app/) and [worker](worker/) apps have their own <ins>requirements.txt</ins> and <ins>requirements.test.txt</ins>.

- Config for [Ruff](https://docs.astral.sh/ruff/) and [Mypy](https://www.mypy-lang.org/) is defined in the <ins>pyproject.toml</ins> file of the corresponding app.


## How to Run the Project

**Step 1**. Clone the repository and navigate to the root project directory.

**Step 2**. Launch services using Docker Compose plugin:
```bash
docker compose --profile app --profile ui up -d
```
---

**Note**: there are 2 profiles of services declared in the [docker-compose.yml](docker-compose.yml) file:
  1. *app* (app, worker, redis);
  2. *ui* (flower).

The purpose of using [profiles](https://docs.docker.com/compose/how-tos/profiles/) in this particular project is to control
which services are needed during development or production stages, CI/CD pipelines etc. For example, Flower might not be a required service to launch or depend on during CI/CD process.

---

Finally, the following services will be stared:

  💻 app: FastAPI application at http://localhost:8000 <br />
  🛠 worker: Celery worker <br />
  🌷 flower: Flower dashboard at http://localhost:5555 <br />
  ✉️ redis: Redis broker and backend

## Usage
Navigate to http://localhost:8000/docs and trigger a background task that will be processed by the [worker](worker/) on the background. You can use the id of the task to monitor state and results of the task. Alternatively, you can open the Flower's dashboard at http://localhost:5555 and monitor execution of background tasks.


## Testing

The project uses:
  * [Pytest](https://docs.pytest.org/en/8.3.x/) for testing the codebase;
  * [Mypy](https://www.mypy-lang.org/) for static type checking;
  * [Ruff](https://docs.astral.sh/ruff/) for code linting and formatting.  

  There are separate Github Actions to run integration tests for [app](.github/workflows/app-ci.yaml) and [worker](.github/workflows/worker-ci.yaml) services and run [End-to-End](.github/workflows/e2e-testing.yaml) tests for the entire infrastructure.

If there's a need to run tests manually, use the following examples:

  * Linting:
```bash
# Run ruff for app
ruff check app/

# Run ruff for worker
ruff check worker/
```

* Type checking:
```bash
# Run mypy for app
mypy app/

# Run mypy for worker
mypy worker/
```

* Testing:
```bash
# Run integration tests for app
pytest -v app/tests

# Run integration tests for worker
pytest -v worker/tests

# Run E2E tests
docker compose --profile app up -d
E2E_MODE_DISABLED=0 pytest -v app/tests
```


## License

This project is licensed under the MIT License.
