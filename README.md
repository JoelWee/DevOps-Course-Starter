# DevOps Apprenticeship: Project Exercise

## Getting started

The project uses a virtual environment to isolate package dependencies.  You will need to install `poetry` first. To create the virtual environment and install required packages, run the following from a bash shell terminal:

### On Windows (Using Git Bash), macOS and Linux
```bash
cp -n .env.template .env
```

Once the setup script has completed and all packages have been installed, start the Flask app by running:
```bash
poetry run flask run
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
docker-compose up -f docker-compose.prod.yml --build
docker-compose up --build
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
docker build --tag todo-app .
docker run --env-file .env -v "$(pwd)":/app todo-app test_watch
```

## Deployment to Heroku

### Manual
```sh
heroku login
heroku container:login
docker pull j0elwee/devops-trg
docker build --cache-from j0elwee/devops-trg -t registry.heroku.com/devops-trg/web --target production .
docker push registry.heroku.com/devops-trg/web
heroku container:release web -a devops-trg
```
