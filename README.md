## FastAPI + Celery Integration

![Pytest](https://img.shields.io/badge/py-test-blue?logo=pytest)
[![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)
[![Linter Ruff](https://img.shields.io/badge/Linter-Ruff-brightgreen)](https://github.com/charliermarsh/ruff)

This project provides a comprehensive way to use **FastAPI** with **Celery** for running background tasks, using **Redis** as broker and result backend. The stack also includes **Flower** for monitoring task execution. The entire setup is containerized using the **Docker Compose** plugin.

<p align="center">
  <img src="https://i.ibb.co/6VCXmzc/1.jpg" width="600" height="600" alt="Workflow Diagram" />
</p>


## Technical Stack

* Docker + Docker Compose (plugin)
* Python 3.12
* FastAPI 0.129
* Celery 5.6
* Flower 2.0
* Redis 7.2


## Project Structure

```bash
# FastAPI application
├── app
   ├── ...
# Celery worker
├── worker
   ├── ...
├── docker-compose.yml
├── .env.example # config template for the entire stack
└── README.md
```


## Configuration

* There's a global <ins>.env</ins> file in the root project directory that provides general configuration for both [app](app/) and [worker](worker/) applications. It contains the following parameters:

| Variable | Default | Description |
| --- | --- | --- |
| CELERY_BROKER_URL | *redis://redis:6379/1* | URL for the Celery broker |
| CELERY_RESULT_BACKEND | *redis://redis:6379/2* | URL for the Celery result backend |

It can be generated from the [template](.env.example) like this:
```bash
cp .env.example .env
```

* [app](app/) requires a separate <ins>.env</ins> with the following parameters:

| Variable | Default | Description |
| --- | --- | --- |
| TITLE | *FastAPI + Celery API* | title of the API |
| DESCRIPTION | *Example API of using FastAPI and Celery* | description of the API |
| VERSION | *0.0.1* | version of the API |
| DEBUG | *0* | Enable or disable debug mode |

It can be generated from the [template](app/.env.example) like this:
```bash
cp app/.env.example app/.env
```

* [worker](worker/) also requires a separate <ins>.env</ins> file with the following configuration:

| Variable | Default | Description |
| --- | --- | --- |
| CELERY_RETRY_DELAY | *1* | delay in seconds before retrying a failed task |
| CELERY_MAX_RETRIES | *3* | maximum number of retries for a failed task |

You can generate it from the [template](worker/.env.example) like this:
```bash
cp worker/.env.example worker/.env
```

Once all configuration files are generated and filled with the required values, the stack is ready to be run.


## Installation

Step 1: clone the repository and navigate to the project directory:

```bash
git clone git@github.com:prathamlahoti123/FastAPI-Celery-Flower-example.git
cd FastAPI-Celery-Flower-example/
```

Step 2: generate configuration files in the root project directory (see [template](.env.example)) and for the [app](app/) application (see [template](app/.env.example)).

Now, the stack is ready to be run.


## Running
In order to run all services use the following command:

```bash
docker compose --profile main up -d
```

As a result it will start 4 services:
- 💻 *api* - main FastAPI application (available at http://localhost:8000)
- 🛠 *worker* -  application for running Celery tasks
- ✉️ *redis* for scheduling tasks and storing task results
- 🌷 *flower* - UI to monitor tasks (available at http://localhost:5555)

**Note**: Docker Compose [profiles](https://docs.docker.com/compose/how-tos/profiles/) are used to control which services to run during development or production stages, CI/CD pipelines etc. For example, *flower* service might not be a required service to launch during CI/CD process.


## Usage
Once the stack is up and running navigate to http://localhost:8000/docs and trigger a background task that will be processed by the [worker](worker/) application on the background. You can use the id of the task to monitor state and results of the task. Alternatively, you can open the Flower's dashboard at http://localhost:5555 and monitor execution of background tasks.


## Notes

- [app](app/) and [worker](worker/) are 2 separate applications with their own functionality, dependencies and configuration. They interact with each other via Redis broker;

- [worker](worker/) runs under [watchmedo](https://github.com/gorakhargosh/watchdog) to ensure reloading of the worker on code-changes.


## References
- [FastAPI](https://github.com/fastapi/fastapi)
- [Celery](https://github.com/celery/celery)
- [Flower](https://github.com/mher/flower)


## License

This project is licensed under the MIT License.
