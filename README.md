# SagaLabs Web Manager

Written in Flask

## Usage

On both linux and windows login using the az-cli command

```bash
az login
```


**Linux**

```bash
virtualenv venv
. venv/bin/activate
pip install -r requirements.txt
flask init-db
flask run
```

**Windows (PowerShell)**

```ps1
virtualenv venv
./venv/Scripts/activate
pip install -r requirements.txt
flask init-db
flask run
```

Every time the structure of the DB is modified, `flask init-db` must be rerun.
This deletes the current running config of the DB, and creates a new clean DB.

## Docker

Make a file called .env with the variables for a service-principal in the root directory.
The file should set the following variables:

```bash
AZURE_CLIENT_ID=<your-service-principal-client-id>
AZURE_CLIENT_SECRET=<your-service-principal-client-secret>
AZURE_TENANT_ID=<your-azure-tenant-id>
```

```bash
docker-compose up --build
```

The `-it` makes the instance interactive, this means pressing ctrl+C terminates the container.
This can thus be omited, meaning containers are stopped by the `docker stop <container_name>` instead.

- List installed images: `docker images`
- List running containers: `docker ps`.

### TODO
- [x] Remove use case: User
- [ ] BackBone integration
