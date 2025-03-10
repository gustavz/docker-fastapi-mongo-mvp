# FastAPI-MongoDB-Docker Template

Minimal working template to run a fast API with a mongo DB using docker compose

### Getting Started

1. `brew install docker-compose` (optional once to install docker-compose)
2. `bash run.sh` to rebuild and start containers
3. `bash run.sh down` same as 1 but first removes all containers, volumes and networks (e.g. necessary if credentials changed)
4. Access running app: http://0.0.0.0:8000/docs