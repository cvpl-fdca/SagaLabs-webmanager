# SagaLabs frontend

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


### Authorization

You must be authorized to Azure in the current session (`az login`).

### TODO

- [x] Add multiple VPN urls at once
- [x] create timeout for request
- [x] handle errors from requests
- [x] import API key from Azure
- [ ] Admin panel shows multiple labs (admin panel works)
- [ ] Get IPs from Azure
- [ ] keyvault temorary storage
- [ ] admin secret key from keyvault
