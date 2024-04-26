# YouTube Background Data

This project is a solution to fetch updates from YouTube in the background at 1-minute intervals and store the data. The key components of the solution are as follows:

## Server

The server is built using the following technologies:

- Python
- FastAPI
- SQLAlchemy
- Poetry
- YouTube API

To overcome YouTube API quota limitations, the application utilizes 3 API keys and automatically picks a working key.

## Background Process

A background process has been implemented to check for new data on YouTube every 1 minute.

## Data Storage

All fetched data is stored in an Azure PostgreSQL database for persistence.

## Dashboard

Additionally, a dashboard has been built to display the following information:

- When the API was called
- The status of each API call
- All the data received from YouTube

## Deployment

The server has been hosted on Azure Container Apps using Docker for easy deployment and scalability.

## Repository and Hosted URL

- GitHub Repository: https://github.com/atishayj2202/Youtube-Background-Data
- Hosted Server: https://yt-background.yellowbush-cadc3844.centralindia.azurecontainerapps.io/about

## Directory Structure

- `src`: Contains all Python code
  - `client`: Connection with other services (like YouTube, Database)
  - `db`: Database table and base to handle it
  - `services`: Algorithms to control all data and manipulate it
  - `util`: Contains algorithms and data structures to be used across the project, like parsers, enums, etc.
  - `main.py`: The starting script of the server
- `deploy`: Helps in deployment to Azure Container Apps and handling the database
- `templates`: HTML files for the dashboard

Feel free to explore the repository and the hosted server for more details and further testing.

## environment setup

need a locally installed python version 3.10.12. recommended to use pyenv to install that.

```shell
poetry env use ~/.pyenv/versions/3.10.12/bin/python
poetry install
```

## testing app

1. Run a local instance of cockraoch db using:

```shell
sh deploy/local_test.sh cr-pull  # required only first time
sh deploy/local_test.sh cr-local-start
sh deploy/local_test.sh cr-stop  # when testing is over
```

Now the tests which require this local instance will run. They can be run individually in pycharm or using the command:
```shell
poetry run pytest
```

## linting/formatting
The following commands can be used:

```shell
poetry run sh deploy/local_test.sh check-format
poetry run sh deploy/local_test.sh format
```

## version updates
we use bumpversion to make version updates. The following commands can be used:

```shell
poetry run bumpversion --config-file=./deploy/.bumpversion.cfg <option>
```
The option can be:
- patch: to update the patch version
- minor: to update the minor version
- major: to update the major version
- release: to update the release version
  - also add `--tag` to create a git tag when releasing
