# DevOps Apprenticeship: Project Exercise

## Getting started

The project uses a virtual environment to isolate package dependencies. You will need to install `poetry` first. To create the virtual environment and install required packages, run the following from a bash shell terminal:

### On Windows (Using Git Bash), macOS and Linux

```bash
cp -n .env.template .env # copy env file and populate the MONGO_URI manually
poetry install -E linting
```

### Setting up OAuth

- Navigate to https://github.com/settings/applications/new and fill in the form. (You'll need to be logged into a github account)
  - Set "Authorization callback URL" to "http://localhost:5000/auth/authorize"
  - Set "Homepage URL" to "http://localhost:5000/"
  - Name the app something sensible, e.g. "Devops training app (local)"
- Copy the "Client ID" and set the OAUTH_CLIENT_ID to this value in the .env file
- Click on "Generate a new client secret", copy the secret and use it to set the OAUTH_CLIENT_SECRET in .env

### Setting up MongoDb

Run a local mongo db instance by running

```bash
docker run -p 27017:27017 -d mongo
```

### Running the App

After completing the setup, start the Flask app by running:

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
docker-compose -f docker-compose.prod.yml up --build
docker-compose up --build
```

### Running Tests

#### Locally

```python
poetry shell
pytest tests  # run unit and integration tests
pytest tests_e2e  # run e2e tests, requires running mongo locally (e.g. via docker) and setting the connection uri appropriately (e.g. via env variable)
```

#### With Docker

```sh
# unit tests
docker pull j0elwee/devops-trg:python-3.8-slim-buster-with-geckodriver
docker build --build-arg BUILDKIT_INLINE_CACHE=1 --cache-from j0elwee/devops-trg:python-3.8-slim-buster-with-geckodriver -t j0elwee/devops-trg:python-3.8-slim-buster-with-geckodriver -f Dockerfile.test.base .
docker-compose -f docker-compose.test.yml up --exit-code-from tests --build
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

### Azure

The following is done in shell:

#### Initialise DB

```sh
export RG="SoftwirePilot_JoelWee_ProjectExercise"
export DBUSER="joel-cosmodb-user"
export DBNAME="joel-cosmodb"
az cosmosdb create --name $DBUSER --resource-group $RG --kind MongoDB
az cosmosdb mongodb database create --account-name $DBUSER --name $DBNAME --resource-group $RG
az cosmosdb keys list -n $DBUSER -g $RG --type connection-strings
```

#### Create App

```sh
export RG="SoftwirePilot_JoelWee_ProjectExercise"
export APPPLAN="joel-app-plan"
export APPNAME="joel-devops" # http://joel-devops.azurewebsites.net/
export CONTAINER="j0elwee/devops-trg:latest"
az appservice plan create --resource-group $RG -n $APPPLAN --sku B1 --is-linux
az webapp create --resource-group $RG --plan $APPPLAN --name $APPNAME --deployment-container-image-name $CONTAINER

# Configure app settings. Fill in the variables yourself
az webapp config appsettings set -g $RG -n $APPNAME --settings FLASK_APP=$FLASK_APP MONGO_URI=$MONGO_URI OAUTH_CLIENT_ID=$OAUTH_CLIENT_ID  OAUTH_CLIENT_SECRET=$OAUTH_CLIENT_SECRET SECRET_KEY=$SECRET_KEY

az webapp deployment container config --enable-cd true --resource-group $RG --name $APPNAME
curl -dH -X POST $WEBHOOK # Test webhook
travis encrypt --pro AZURE_WEBHOOK=$WEBHOOK
```

#### Secure DB

Take env vars from above as required. This uses IP firewall. Can't seem to do VNets (Tier S1 and above required it seems?)

```sh
az webapp show --resource-group $RG --name $APPNAME --query outboundIpAddresses --output tsv # Call this and add the IPs to the azure portal
```

#### Add

Take env vars from above as required. This uses IP firewall. Can't seem to do VNets (Tier S1 and above required it seems?)

```sh
az webapp show --resource-group $RG --name $APPNAME --query outboundIpAddresses --output tsv # Call this and add the IPs to the azure portal
```

### Terraform

```
terraform apply -var "oauth_client_id=$OAUTH_CLIENT_ID" -var "oauth_client_secret=$OAUTH_CLIENT_SECRET" -var "secret_key=$SECRETKEY"

# webhook
curl -dH -X POST "$(terraform output -raw webhook_url)"
```

#### Set up storage backend

https://docs.microsoft.com/en-us/azure/developer/terraform/store-state-in-azure-storage#configure-storage-account

```sh
export RG="SoftwirePilot_JoelWee_ProjectExercise"
export ACC_NAME="joelweetfstate"
export CONTAINER_NAME="tfstate-container"

# Create storage account
az storage account create --resource-group $RG --name $ACC_NAME --sku Standard_LRS --encryption-services blob

# Get storage account key
export ACCOUNT_KEY=$(az storage account keys list --resource-group $RG --account-name $ACC_NAME --query '[0].value' -o tsv)

# Create blob container
az storage container create --name $CONTAINER_NAME --account-name $ACC_NAME --account-key $ACCOUNT_KEY

echo "storage_account_name: $ACC_NAME"
echo "container_name: $CONTAINER_NAME"
echo "access_key: $ACCOUNT_KEY"
```

#### Run TF with storage backend

```sh
export ARM_ACCESS_KEY=<in .env file>
terraform apply -var "oauth_client_id=$OAUTH_CLIENT_ID" -var "oauth_client_secret=$OAUTH_CLIENT_SECRET" -var "secret_key=$SECRETKEY"

```

#### Link TF with Travis

```sh
az account list # Get sub id
az account set --subscription=$SID
az ad sp create-for-rbac --role="Contributor"  --scopes="/subscriptions/$SID/resourceGroups/$RG" # Run in powershell. Create Service principal and add ARM_CLIENT_ID, ARM_TENANT_ID, ARM_SUBSCRIPTION_ID and ARM_CLIENT_SECRET to travis config

```
