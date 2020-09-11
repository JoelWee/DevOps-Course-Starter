# DevOps Apprenticeship: Project Exercise

## Getting started

The project uses a virtual environment to isolate package dependencies.  You will need to install `poetry` first. To create the virtual environment and install required packages, run the following from a bash shell terminal:

### On Windows (Using Git Bash), macOS and Linux
```bash
$ source setup.sh
```

Once the setup script has completed and all packages have been installed, start the Flask app by running:
```bash
$ poetry run flask run
```

You should see output similar to the following:
```bash
 * Serving Flask app "app" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with fsevents reloader
 * Debugger is active!
 * Debugger PIN: 226-556-590
```
Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.


### Run with docker
```sh
docker build --target production --tag todo-app:prod
docker run --env-file .env -p 5000:5000 todo-app:prod
docker build --target development --tag todo-app:dev
docker run --env-file .env -p 5000:5000 -v "$(pwd)":/app todo-app:dev
```

### Running Tests
#### Locally
```python
poetry shell
pytest tests  # run unit and integration tests
pytest tests_e2e  # run e2e tests
```

Note that running `pytest` doesn't work because of different .env files used

#### With Docker
```sh
# unit tests
docker build --tag todo-app:test -f Dockerfile.test .
docker run --env-file .env todo-app:test 
```