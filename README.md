# SagaLabs Web Manager

Written in Flask

## Usage

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

```bash
docker build --tag sl-frontend:1.0.0 .
docker run -it -p 5000:5000 sl-frontend:1.0.0
```

The `-it` makes the instance interactive, this means pressing ctrl+C terminates the container.
This can thus be omited, meaning containers are stopped by the `docker stop <container_name>` instead.

- List installed images: `docker images`
- List running containers: `docker ps`.

### TODO
- [x] Remove use case: User
- [ ] BackBone integration
